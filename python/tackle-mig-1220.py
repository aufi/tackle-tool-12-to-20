import argparse
import json
import os
import requests

###############################################################################

dataDir = "./mig-data"
expectedDirs = ["dump", "dump/application-inventory", "dump/controls", "dump/pathfinder", "transformed", "transformed/application-inventory", "transformed/controls", "transformed/pathfinder"]
apiObjects = ["application-inventory/application", "controls/stakeholder", "controls/business-service"] #], "pathfinder/assessments/confidence"]

class Application:
    pass

class Assessment:
    pass

class AssessmentRisk:
    pass

class Stakeholder:
    pass

applications = []



###############################################################################

parser = argparse.ArgumentParser(description='Migrate data from Tackle 1.2 to Tackle 2.')
parser.add_argument('steps', type=str, nargs='*',
                    help='Steps of migration that should be executed (all by default), options: dump transform upload')
args = parser.parse_args()

###############################################################################

def prepareDirs():
    if os.path.isdir(dataDir):
        print("Data directory already exists, using %s" % dataDir)
    else:
      print("Creating data directories at %s" % dataDir)
      os.mkdir(dataDir)
      for dirName in expectedDirs:
          os.mkdir(os.path.join(dataDir, dirName))

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

def transformControls():
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
    pass

###############################################################################

print("Starting Tackle 1.2 -> 2 data migration tool")

# Dump steps
if cmdWanted(args, "dump"):
    dumpTackle1()
    transformApplications()
    transformControls()


# Upload steps
if cmdWanted(args, "upload"):
    uploadTackle2()

print("Done.")

###############################################################################

