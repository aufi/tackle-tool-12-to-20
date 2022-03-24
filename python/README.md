# tackle-tool-12-to-20 (python)

A tool migrating Konveyor Tackle 1.2 data into Tackle 2.0. For more details about Tackle, see https://github.com/konveyor/tackle-documentation

Under initial development

## Usage

```
$ python tackle-mig-1220.py --help
usage: tackle-mig-1220.py [-h] [steps ...]

Migrate data from Tackle 1.2 to Tackle 2.

positional arguments:
  steps       Steps of migration that should be executed (all by default), options: dump transform upload

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

Sample migration data directory is [mig-data](mig-data)
