# author: Marie Jossé

# Python script

###############################
## Trends Earth productivity ##
###############################

##### Packages : trends_earth_algorithms
# trends_earth_schemas


##### Load arguments

import sys
import json
import productivity
import logging
import te_algorithms
import ee

args = sys.argv

##### Import data

if len(args) < 3:
    raise ValueError("This tool needs at least 1 argument")
else:
    input_data_file = args[1]
    print(input_data_file)
    with open(input_data_file) as f:
        input_data = json.load(f)


credentials = ee.ServiceAccountCredentials("galaxy-te@ee-giulianolangella.iam.gserviceaccout.com",args[2])
ee.Initialize(credentials)


#############################################################
#                                                           #
#               Loading and running data                    #
#                                                           #
#############################################################
logger = logging.getLogger("example_logger")
logger.setLevel(logging.DEBUG)
send_progress = "test"
logger.debug("Ceci est un message de débogage", extra={'param': send_progress})

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

output_data = productivity.run(params=input_data, logger = logger)

with open("productivity.json", "w") as f:
    json.dump(output_data, f)

