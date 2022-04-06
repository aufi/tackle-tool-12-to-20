# tackle-tool-12-to-20 (python)

A tool migrating Konveyor Tackle 1.2 data into Tackle 2.0. For more details about Tackle, see https://github.com/konveyor/tackle-documentation

Under initial development

## Usage

```
$ python tackle-mig-1220.py --help
usage: tackle-mig-1220.py [-h] [steps ...]

Migrate data from Tackle 1.2 to Tackle 2.

positional arguments:
  steps       One or more steps of migration that should be executed (dump and upload by default), options: dump upload

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
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe.rhcloud.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn(
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe.rhcloud.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn(
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe.rhcloud.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn(
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe.rhcloud.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn(
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe.rhcloud.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn(
/usr/lib/python3.10/site-packages/urllib3/connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS request is being made to host 'tackle-mta.apps.mta02.cnv-qe.rhcloud.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
  warnings.warn(
Writing JSON data files into ./mig-data..
Done.
```

Sample migration JSON dump files are available in [mig-data directory](mig-data).
