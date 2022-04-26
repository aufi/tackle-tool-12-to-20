# tackle-tool-12-to-20

A tool migrating Konveyor Tackle 1.2 data into Tackle 2.0 written as a Python script. For more details about Tackle, see [Tackle2-Hub README](../../) or https://github.com/konveyor/tackle-documentation.

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

API endpoints and credentials should be set in the environment or source an env file.

```
export TACKLE1_URL=https://tackle-tackle.apps.mta01.cluster.local
export TACKLE1_USERNAME=tackle
export TACKLE1_PASSWORD=...
export TACKLE2_URL=https://tackle-konveyor-tackle.apps.cluster.local
export TACKLE2_USERNAME=admin
export TACKLE2_PASSWORD=...
```

### Sample command output

```
$ . config-vars && python tackle-mig-1220.py dump
Starting Tackle 1.2 -> 2 data migration tool
Dumping Tackle1.2 objects..
Writing JSON data files into ./mig-data..
Done.
```

Sample migration JSON dump files are available in [mig-data directory](mig-data).

Unverified HTTPS warnings from Python could be hidden by ```export PYTHONWARNINGS="ignore:Unverified HTTPS request"```.
