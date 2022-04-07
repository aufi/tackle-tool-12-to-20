import argparse
import copy
import json
import os
import requests

###############################################################################

parser = argparse.ArgumentParser(description='Migrate data from Tackle 1.2 to Tackle 2.')
parser.add_argument('steps', type=str, nargs='*',
                    help='One or more steps of migration that should be executed (dump and upload by default), options: dump  upload')
args = parser.parse_args()

###############################################################################

def ensureDataDir(dataDir):
    if os.path.isdir(dataDir):
        pass
        # print("Data directory already exists, using %s" % dataDir)
    else:
      # print("Creating data directories at %s" % dataDir)
      os.mkdir(dataDir)

def checkConfig(expected_vars):
    for varKey in expected_vars:
        if os.environ.get(varKey) is None:
            print("ERROR: Missing required environment variable %s, define it first." % varKey)
            exit(1)

def apiJSON(url, token, data=None): # TODO: currently is specific to Tackle1 API only
    if data:
        r = requests.post(url, json.dumps(data), data, headers={"Authorization": "Bearer %s" % token, "Content-Type": "text/json"}, verify=False)
    else:
        r = requests.get(url, headers={"Authorization": "Bearer %s" % token, "Content-Type": "text/json"}, verify=False)  # add pagination?
    if not r.ok:
        print("ERROR: API request failed with status %d for %s" % (r.status_code, url))
        exit(1)
    return json.loads(r.text)['_embedded'][url.rsplit('/')[-1]] # unwrap Tackle1 JSON response (e.g. _embedded -> application -> [{...}])

def loadDump(path):
    data = open(path)
    return json.load(data)

def saveJSON(path, jsonData):
    dumpFile = open(path + ".json", 'w')
    dumpFile.write(json.dumps(jsonData, indent=4, default=vars))
    dumpFile.close()

def cmdWanted(args, step):
    if not args.steps or step in args.steps:
        return True
    else:
        return False

###############################################################################

class Tackle12Import:
    # TYPES order matters for import/upload to Tackle2
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
                tag             = Tackle2Object(tag1)
                tag.name        = tag1['name']
                self.add('tags', tag)
                tags.append(tag)
            # Prepare Application
            app             = Tackle2Object(app1)
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
                shg             = Tackle2Object(shg)
                shg.name        = shg1['name']
                shg.description = shg1['description']
                # +Stakeholders arr/refs?
                self.add('stakeholdergroups', shg)
                shgs.append(shg)
            # Prepare StakeHolder
            sh            = Tackle2Object(sh1)
            sh.name       = sh1['displayName']
            sh.email      = sh1['email']
            # sh.businessServices = []
            sh.groups     = shgs
            # sh.jobFunction = {}
            self.add('stakeholders', sh)
        
        ### STAKEHOLDER GROUPS ###
        collection = apiJSON(self.tackle1Url + "/api/controls/stakeholder-group", self.tackle1Token)
        for shg1 in collection:
            # Prepare StakeholderGroup
            shg             = Tackle2Object(shg1)
            shg.name        = shg1['name']
            shg.description = shg1['description']
            # +Stakeholders arr/refs?
            self.add('stakeholdergroups', shg)

        ### JOB FUNCTION ###
        collection = apiJSON(self.tackle1Url + "/api/controls/job-function", self.tackle1Token)
        for jf1 in collection:
            # Temp holder for stakeholders
            shs = []
            # Prepare JobFunction's Stakeholders
            for sh1 in jf1['stakeholders']:
                sh             = Tackle2Object(sh1)
                sh.name        = sh1['displayName']
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
            bs              = Tackle2Object(bs1)
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
                tag             = Tackle2Object(tag1)
                tag.name        = tag1['name']
                # TagType is injected from tagType processing few lines below
                self.add('tags', tag)
                tags.append(tag)
            # Prepare TagType
            tt            = Tackle2Object(tt1)
            tt.name       = tt1['name']
            tt.colour     = tt1['colour']
            tt.rank       = tt1['rank']
            tt.username   = tt1['createUser'] # Is there another relevant user?
            for tag in tags:
                tag.tagType = copy.deepcopy(tt)
            tt.tags = tags
            self.add('tagtypes', tt)

    def add(self, type, item):
        for existingItem in self.data[type]:
            if item.id == existingItem.id:
                # The item is already present, skipping
                return
        self.data[type].append(item)

    def store(self):
        ensureDataDir(self.dataDir)
        for t in self.TYPES:
            saveJSON(os.path.join(self.dataDir, t), self.data[t])

    def load(self):
        for t in self.TYPES:
            dictCollection = loadDump(os.path.join(self.dataDir, t + '.json'))
            for dictObj in dictCollection:
                obj = Tackle2Object(dictObj)
                self.add(obj)

class Tackle2Object:
    def __init__(self, initAttrs = {}):
        if initAttrs:
            self.id         = initAttrs['id']
            self.createUser = initAttrs['createUser']
            self.updateUser = initAttrs['updateUser']

###############################################################################

dataDir = "./mig-data"

print("Starting Tackle 1.2 -> 2 data migration tool")

# Tackle 2.0 objects to be imported
tackle12import = Tackle12Import(dataDir, os.environ.get('TACKLE1_URL'), os.environ.get('TACKLE1_TOKEN'))

# Dump steps
if cmdWanted(args, "dump"):
    print("Dumping Tackle1.2 objects..")
    tackle12import.dumpTackle1ApplicationInventory()
    tackle12import.dumpTackle1Controls()
    print("Writing JSON data files into %s.." % dataDir)
    tackle12import.store()


# Upload steps
if cmdWanted(args, "upload"):
    print("Loading JSON data files from %s.." % dataDir)
    tackle12import.load()
    print("Uploading data to Tackle2..")
    # tackle12import.uploadTackle2()

print("Done.")

###############################################################################

