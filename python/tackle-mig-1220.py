import argparse
import json
import os
import requests

###############################################################################

dataDir = "./mig-data"
#expectedDirs = ["dump", "dump/application-inventory", "dump/controls", "dump/pathfinder", "transformed", "transformed/application-inventory", "transformed/controls", "transformed/pathfinder"]
#apiObjects = ["application-inventory/application", "controls/stakeholder", "controls/business-service"] #], "pathfinder/assessments/confidence"]

###############################################################################

parser = argparse.ArgumentParser(description='Migrate data from Tackle 1.2 to Tackle 2.')
parser.add_argument('steps', type=str, nargs='*',
                    help='Steps of migration that should be executed (all by default), options: dump transform upload')
args = parser.parse_args()

###############################################################################

def ensureDataDir(dataDir):
    if os.path.isdir(dataDir):
        print("Data directory already exists, using %s" % dataDir)
    else:
      print("Creating data directories at %s" % dataDir)
      os.mkdir(dataDir)

def checkConfig(expected_vars):
    for varKey in expected_vars:
        if os.environ.get(varKey) is None:
            print("ERROR: Missing required environment variable %s, define it first." % varKey)
            exit(1)

def apiJSON(url, token, data=None):
    if data:
        r = requests.post(url, json.dumps(data), data, headers={"Authorization": "Bearer %s" % token, "Content-Type": "text/json"}, verify=False)
    else:
        r = requests.get(url, headers={"Authorization": "Bearer %s" % token, "Content-Type": "text/json"}, verify=False)  # add pagination?
    if not r.ok:
        print("ERROR: API request failed with status %d for %s" % (r.status_code, url))
        exit(1)
    return json.loads(r.text)

def loadDump(path):
    data = open(path)
    return json.load(data)

def saveJSON(path, jsonData):
    dumpFile = open(path + ".json", 'w')
    dumpFile.write(json.dumps(jsonData, indent=4))
    dumpFile.close()

def cmdWanted(args, step):
    if not args.steps or step in args.steps:
        return True
    else:
        return False

###############################################################################

class Tackle12Import:
    TYPES = ['tags', 'tagtypes', 'identities', 'jobfunctions', 'stakeholdergroups', 'stakeholders', 'businessservices', 'applications', 'reviews']  # buckets, proxies

    def __init__(self, dataDir, tackle1Url, tackle1Token):
        self.dataDir      = dataDir
        self.tackle1Url   = tackle1Url
        self.tackle1Token = tackle1Token
        self.data         = dict()
        for t in self.TYPES:
            self.data[t] = []

    # Reach Tackle 1.2 API and gather all application-inventory related objects
    def dumpTackle1ApplicationInventory(self):
        collection = apiJSON(self.tackle1Url + "/api/application-inventory/application", self.tackle1Token)
        for app1 in collection:
            # Temp holder for tags
            tags = []
            # Prepare Tags
            for tag1 in app1['tags']:
                tag             = Tackle2Object()
                tag.id          = tag1['id']
                #shg.createUser  = shg1['createUser']
                #shg.updateUser  = shg1['updateUser']
                tag.name        = tag1['name']
                self.add('tags', tag)
                tags.append(tag)
            # Prepare Application
            app             = Tackle2Object()
            app.id          = app1['id']
            app.createUser  = app1['createUser']
            app.updateUser  = app1['updateUser']
            app.name        = app1['name']
            app.description = app1['description']
            # app.businessService = {}
            app.tags        = tags
            self.add('applications', app)

    # Reach Tackle 1.2 API and gather all control related objects
    def dumpTackle1Controls(self):
        ### STAKEHOLDER ###
        collection = apiJSON(self.tackle1Url + "/api/controls/stakeholder", self.tackle1Token)
        for sh1 in collection:
            # Temp holder for stakeholder's groups
            shgs = []
            # Prepare StakeholderGroups
            for shg1 in sh1['stakeholderGroups']:
                shg             = Tackle2Object()
                shg.id          = shg1['id']
                shg.createUser  = shg1['createUser']
                shg.updateUser  = shg1['updateUser']
                shg.name        = shg1['name']
                shg.description = shg1['description']
                # +Stakeholders arr/refs?
                self.add('stakeholdergroups', shg)
                shgs.append(shg)
            # Prepare StakeHolder
            sh            = Tackle2Object()
            sh.id         = sh1['id']
            sh.createUser = sh1['createUser']
            sh.updateUser = sh1['updateUser']
            sh.name       = sh1['name']
            sh.email      = sh1['email']
            # sh.businessServices = []
            sh.groups     = shgs
            # sh.jobFunction = {}
            self.add('stakeholders', sh)

        ### JOB FUNCTION ###
        collection = apiJSON(self.tackle1Url + "/api/controls/job-function", self.tackle1Token)
        for jf1 in collection:
            # Temp holder for stakeholders
            shs = []
            # Prepare JobFunction's Stakeholders
            for sh1 in jf1['stakeholders']:
                sh             = Tackle2Object()
                sh.id          = sh1['id']
                sh.createUser  = sh1['createUser']
                sh.updateUser  = sh1['updateUser']
                sh.name        = sh1['name']
                sh.email       = sh1['email']
                self.add('stakeholders', sh)
                shs.append(sh)
            # Prepare JobFunction
            jf              = Tackle2Object()
            jf.id           = jf1['id']
            jf.createUser   = jf1['createUser']
            jf.updateUser   = jf1['updateUser']
            jf.name         = jf1['role']
            jf.stakeholders = shs
            self.add('jobfunctions', jf)

        ### BUSINESS SERVICE ###
        collection = apiJSON(self.tackle1Url + "/api/controls/business-service", self.tackle1Token)
        for bs1 in collection:
            # Prepare JobFunction
            bs              = Tackle2Object()
            bs.id           = bs1['id']
            bs.createUser   = bs1['createUser']
            bs.updateUser   = bs1['updateUser']
            bs.name         = bs1['name']
            bs.description  = bs1['description']
            # bs.owner        = bs1['owner'] + foreign key object
            self.add('businessservices', bs)

        ### TAG TYPES & TAGS ###
        collection = apiJSON(self.tackle1Url + "/api/controls/tag-type", self.tackle1Token)
        for tt1 in collection:
            # Temp holder for tags
            tags = []
            # Prepare TagTypes's Tags
            for tag1 in tt1['tags']:
                tag             = Tackle2Object()
                tag.id          = tag1['id']
                tag.createUser  = tag1['createUser']
                tag.updateUser  = tag1['updateUser']
                tag.name        = tag1['name']
                # TagType is injected from tagType processing few lines below
                self.add('tags', sh)
                tags.append(tag)
            # Prepare TagType
            tt            = Tackle2Object()
            tt.id         = tt1['id']
            tt.createUser = tt1['createUser']
            tt.updateUser = tt1['updateUser']
            tt.name       = tt1['name']
            tt.colour     = tt1['colour']
            tt.rank       = tt1['rank']
            tt.username   = tt1['createUser'] # Is there another user relevant?
            for tag in tags:
                tag.tagType = tt
            tt.tags = tags
            self.add('tagtypes', tt)

    def add(self, type, item):
        # TODO: skip if is already present
        self.data[type].append(item)

    def store(self):
        ensureDataDir(self.dataDir)
        for t in self.TYPES:
            saveJSON(os.path.join(self.dataDir, t), self.data[t])

    def load(self):
        for t in self.TYPES:
            dictCollection = loadDump(os.path.join(self.dataDir, t + '.json'))
            for obj in dictCollection:
                self.add()

class Tackle2Object:
    pass

###############################################################################

def dumpTackle1():
    print("Dumping Tackle 1.2 objects")
    prepareDirs()
    checkConfig(["TACKLE1_URL", "TACKLE1_TOKEN"])
    for path in apiObjects:
        jsonData = apiJSON(os.environ.get('TACKLE1_URL') + "/api/" + path, os.environ.get('TACKLE1_TOKEN'))
        saveJSON(os.path.join(dataDir, "dump", path), jsonData['_embedded'][path.rsplit('/')[-1]])  # get rid of object type name from jsonData

def transformApplications():
    print("Transforming Applications")
    apps1 = loadDump(os.path.join(dataDir, "dump", "application-inventory", "application.json"))
    apps2 = []
    for app1 in apps1:
        # Application object
        app2 = Application()
        app2.id = app1['id']
        app2.name = app1['name']
        app2.description = app1['description']
        apps2.append(app2)
        # Application-related objects - assessment-risk
        appFilter = dict()
        appFilter['applicationId'] = app2.id
        assessmentRisk = apiJSON(os.environ.get('TACKLE1_URL') + "/api/pathfinder/assessments/assessment-risk", os.environ.get('TACKLE1_TOKEN'), appFilter)
        # tady načítat další související věci a rovnou z nich dělat data pro import
    saveJSON(os.path.join(dataDir, "transformed", "application-inventory", "application"), apps2)
    #saveJSON(os.path.join(dataDir, "transformed", "application-inventory", "assessment-risk.json"), assessmentRisk)

def dumpControls():
    print("Transforming Controls stakeholders")
    stakeholders1 = loadDump(os.path.join(dataDir, "dump", "controls", "stakeholder.json"))
    stakeholders2 = []
    for sh1 in stakeholders1:
        sh2 = Application()
        sh2.id = sh1['id']
        sh2.name = sh1['displayName']
        sh2.email = sh1['email']
        stakeholders2.append(sh1)
        
    saveJSON(os.path.join(dataDir, "transformed", "controls", "stakeholder.json"), stakeholders2)


def uploadTackle2():
    print("Uploading Applications")
    apps = loadDump(os.path.join(dataDir, "dump", "application-inventory", "application.json"))
    for app in apps:
        apiJSON(os.environ.get('TACKLE2_URL') + "/api/application", os.environ.get('TACKLE2_TOKEN'), app)

###############################################################################

print("Starting Tackle 1.2 -> 2 data migration tool")

# Tackle 2.0 objects to be imported
tackle12import = Tackle12Import(dataDir, os.environ.get('TACKLE1_URL'), os.environ.get('TACKLE1_TOKEN'))

# Dump steps
if cmdWanted(args, "dump"):
    tackle12import.dumpTackle1Controls()
    tackle12import.store()


# Upload steps
if cmdWanted(args, "upload"):
    tackle12import.load()
    # tackle12import.uploadTackle2()

print("Done.")

###############################################################################
