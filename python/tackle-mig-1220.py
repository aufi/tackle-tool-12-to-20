import argparse
import json
import os
import requests

###############################################################################

dataDir = "./mig-data"
expectedDirs = ["dump", "dump/application-inventory", "transformed", "transformed/application-inventory"]
apiObjects = ["application-inventory/application"]

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
      for dirName in expectedDirs:
          os.mkdir(os.path.join(dataDir, dirName))

def checkConfig(expected_vars):
    for varKey in expected_vars:
        if os.environ.get(varKey) is None:
            print("ERROR: Missing required environment variable %s, define it first." % varKey)
            exit(1)

def apiGetJSON(url, token):
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
        jsonData = apiGetJSON(os.environ.get('TACKLE1_URL') + "/api/" + path, os.environ.get('TACKLE1_TOKEN'))
        saveJSON(os.path.join(dataDir, "dump", path), jsonData['_embedded'][path.rsplit('/')[-1]])  # get rid of object type name from jsonData

def transformApplications():
    print("Transforming Applications")
    apps1 = loadDump(os.path.join(dataDir, "dump", "application-inventory", "application.json"))
    apps2 = []
    for app1 in apps1:
        # Prepare transformed application dict
        app2 = {}
        app2['name'] = app1['name']
        app2['description'] = app1['description']
        apps2.append(app2)
    saveJSON(os.path.join(dataDir, "transformed", "application-inventory", "application"), apps2)

def uploadTackle2():
    pass

###############################################################################

print("Starting Tackle 1.2 -> 2 data migration tool")

# Dump steps
if cmdWanted(args, "dump"):
    dumpTackle1()

# Transformation steps
if cmdWanted(args, "transform"):
    transformApplications()

# Upload steps
if cmdWanted(args, "upload"):
    uploadTackle2()

print("Done.")