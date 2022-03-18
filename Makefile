TACKLE_12_URL ?= 
TACKLE_12_TOKEN ?= 
TACKLE_20_URL ?=
TACKLE_20_TOKEN ?= 

DATA_DIR ?= .tackle_mig_data
SERVICES ?= array


dump: prepare-data-dir dump-application-inventory


dump-application-inventory: 
	resource = "application-inventory/application"
	curl -H "Content-Type: application/json" -H "Authorization: Bearer ${TACKLE_12_TOKEN}" ${TACKLE_12_URL}/api/${resource} > ${DATA_DIR}/${resource}

prepare-data-dir:
	mkdir -p ${DATA_DIR}
	mkdir -p ${DATA_DIR}/application-inventory
	#for svc in application-inventory pathfinder controls ; do \
	#	mkdir -p ${DATA_DIR}/${svc}; \
	#done
