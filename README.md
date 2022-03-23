# tackle-tool-12-to-20

A tool migrating Konveyor Tackle 1.2 data into Tackle 2.0. For more details about Tackle, see https://github.com/konveyor/tackle-documentation

Under initial development

## Migration process

1. Dump Tackle 1.2 resources from its API (needed to provide API URL and secret token)
2. Load local dump of Tackle 1.2 objects and transform it to the Tackle2 Hub API format
3. Push transformed data into Tackle2 Hub API (needed to provide API URL and secret token)
4. ? (If needed create local mapping of new object IDs allowing keep relations without 1.2 IDs in 2.0 API) and upload objects to tackle 2.0 in phases


## Development roadmap

- Initial development&PoC
  - <del>Dump single object type from Tackle 1.2 (Application)</del>
  - <del>Transform dumped object into minimal valid format to be created in Tackle 2.0 (Application)</del>
  - Upload transformed object into Tackle 2.0 (Application)
- Extending to support real objects from Tackle 1.2
  - Full capability to migrate Application
  - Cover objects from all three Tackle 1.2 components
    - application-inventory
    - controls
    - reports / pathfinder

Open questions
- 1.2 vs 2.0 objects mapping ("multisteps" creating objects storing their IDs?)
- Longer time valid Tackle 1.2 token?

## Notes

jinja templates with variables to push data to Tackle 2 API, makefile&bash seems to be too messy, trying ansible to provide some level of structure of the project and open-ness for customizations and debugging
