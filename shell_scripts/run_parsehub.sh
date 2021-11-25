#!/bin/bash

# SECRETS
source /config/shell_scripts/shell_secrets.txt

# SCRIPT CONST
JSON_PATH="/config/rest_json"
TEMP_PATH="/config/shell_scripts/temp"

# If param 3 is set, execute this before update
if [ -n "$2" ]; then
    OVERRIDE="{\"$2\": \"$3\"}"
    # Start RUN with value_override
    RESULT=$(curl "https://www.parsehub.com/api/v2/projects/$1/run" -X POST -d api_key=$PARSEHUB_API_TOKEN --data-urlencode "start_value_override=$OVERRIDE")
else
    # Start Update RUN
    RESULT=$(curl "https://www.parsehub.com/api/v2/projects/$1/run" -X POST -d api_key=$PARSEHUB_API_TOKEN)
fi