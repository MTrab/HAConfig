#!/bin/bash

# SECRETS
source /config/shell_scripts/shell_secrets.txt

# SCRIPT CONST
JSON_PATH="/config/rest_json"
TEMP_PATH="/config/shell_scripts/temp"

# Get result
curl "https://www.parsehub.com/api/v2/projects/$1/last_ready_run/data?api_key=$PARSEHUB_API_TOKEN" | gunzip > "$TEMP_PATH/$2"

# Remove linebreak and copy to prod path
cat "$TEMP_PATH/$2" | tr -d \\n > "$JSON_PATH/$2"

# Remove temporary file
rm "$TEMP_PATH/$2"