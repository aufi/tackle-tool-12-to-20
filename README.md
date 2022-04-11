# tackle-tool-12-to-20

A tool migrating Konveyor Tackle 1.2 data into Tackle 2.0 written as a Python script. For more details about Tackle, see https://github.com/konveyor/tackle-documentation

## Usage

Supported actions
- ```dump``` exports Tackle 1.2 API objects into local JSON files
- ```upload``` creates objects in Tackle 2 from local JSON files
- ```clean``` deletes objects uploaded to Tackle 2 from local JSON files

```
$ python tackle-mig-1220.py --help
usage: tackle-mig-1220.py [-h] [steps ...]

Migrate data from Tackle 1.2 to Tackle 2.

positional arguments:
  steps       One or more steps of migration that should be executed (dump and upload by default), options: dump upload clean

options:
  -h, --help  show this help message and exit
```

API endpoints and tokens should be set in the environment or source an env file.

```
export TACKLE1_URL=https://tackle-tackle.apps.mta01.cluster.local
export TACKLE1_TOKEN=eyJhbGciOiJSUzI1Ni...
export TACKLE2_URL=https://tackle-konveyor-tackle.apps.cluster.local
export TACKLE2_TOKEN=axJsbDcxLisdWDWfca...
```

### Sample command output

```
$ . config-vars && python tackle-mig-1220.py dump
Starting Tackle 1.2 -> 2 data migration tool
Dumping Tackle1.2 objects..
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  wa
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  wa
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  wa
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  wa
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  wa
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  wa
Writing JSON data files into ./mig-data..
Done.
```

Sample migration JSON dump files are available in [mig-data directory](mig-data).

Unverified HTTPS warnings from Python could be hidden by ```export PYTHONWARNINGS="ignore:Unverified HTTPS request"```.
