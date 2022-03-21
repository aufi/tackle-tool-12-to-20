# tackle-tool-12-to-20

A tool migrating Konveyor Tackle 1.2 data into Tackle 2.0. For more details about Tackle, see https://github.com/konveyor/tackle-documentation

Under initial development

## Migration process

1. Dump Tackle 1.2 resources from its API (needed to provide API URL and secret token)
2. Load local dump of Tackle 1.2 objects and transform it to the Tackle2 Hub API format
3. Push transformed data into Tackle2 Hub API (needed to provide API URL and secret token)

## Notes

jinja templates with variables to push data to Tackle 2 API, makefile&bash seems to be too messy, trying ansible to provide some level of structure of the project and open-ness for customizations and debugging
