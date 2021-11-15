#!/bin/bash

# SECRETS
source /config/shell_scripts/shell_secrets.txt

# SCRIPT CONST
JSON_PATH="/config/rest_json"
TEMP_PATH="/config/shell_scripts/temp"

# If param 3 is set, execute this before update
if [ -n "$3" ]; then
    OVERRIDE="{\"$3\": \"$4\"}"
    # Start RUN with value_override
    RESULT=$(curl "https://www.parsehub.com/api/v2/projects/$1/run" -X POST -d api_key=$PARSEHUB_API_TOKEN --data-urlencode "start_value_override=$OVERRIDE")
    RUN_TOKEN=$(echo $RESULT | jq '.run_token')
    echo $(echo $RESULT | jq '.start_value')
    RUN_TOKEN=${RUN_TOKEN:1:12}

    # Await run to finish
    RUN=$(curl "https://www.parsehub.com/api/v2/runs/$RUN_TOKEN?api_key=$PARSEHUB_API_TOKEN")
    STATUS=$(echo $RUN | jq '.status' | cut -d "\"" -f 2)

    while [ $STATUS != "complete" ]; do
        sleep 1s
        RUN=$(curl "https://www.parsehub.com/api/v2/runs/$RUN_TOKEN?api_key=$PARSEHUB_API_TOKEN")
        STATUS=$(echo $RUN | jq '.status' | cut -d "\"" -f 2)
    done
fi

# Start Update RUN
RESULT=$(curl "https://www.parsehub.com/api/v2/projects/$1/run" -X POST -d api_key=$PARSEHUB_API_TOKEN)
RUN_TOKEN=$(echo $RESULT | jq '.run_token')
RUN_TOKEN=${RUN_TOKEN:1:12}

# Await run to finish
RUN=$(curl "https://www.parsehub.com/api/v2/runs/$RUN_TOKEN?api_key=$PARSEHUB_API_TOKEN")
STATUS=$(echo $RUN | jq '.status' | cut -d "\"" -f 2)

while [ $STATUS != "complete" ]; do
    sleep 1s
    RUN=$(curl "https://www.parsehub.com/api/v2/runs/$RUN_TOKEN?api_key=$PARSEHUB_API_TOKEN")
    STATUS=$(echo $RUN | jq '.status' | cut -d "\"" -f 2)
done

# Get result
curl "https://www.parsehub.com/api/v2/projects/$1/last_ready_run/data?api_key=$PARSEHUB_API_TOKEN" | gunzip > "$TEMP_PATH/$2"

# Remove linebreak and copy to prod path
cat "$TEMP_PATH/$2" | tr -d \\n > "$JSON_PATH/$2"

# Remove temporary file
rm "$TEMP_PATH/$2"