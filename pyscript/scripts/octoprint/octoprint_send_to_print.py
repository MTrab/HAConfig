import aiohttp
import asyncio
import re

@service
def octoprint_send_to_print(url, key, entity_id, origin="local"):
    """yaml
name: octoprint_send_to_print
description: Send file to print
fields:
  entity_id:
     description: input_select representing the selected file
     example: input_select.octoprint_filelist
     required: true
     selector:
       text:
  url:
     description: API URL to the file section
     example: 'http://1.2.3.4/api/files'
     required: true
     selector:
       text:
  key:
     description: API KEY to the server
     example: DLKJGFHLIDFSTGKDJF
     required: true
     selector:
       text:
  origin:
     description: Location for files, valid options are local or sdcard
     example: local
     default: local
     selector:
        select:
            options:
                - local
                - sdcard
"""
    if entity_id is not None:
        headers = { 'X-Api-Key': key, 'Content-Type': 'application/json' }
        data = ""
        json = '{"command": "select", "print": true}'
        log.debug(json)
        printFile = state.get(entity_id)
        printFile = re.sub(r'([ \(\)0-9:]{5,15})$', '', printFile)
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url + "/" + origin + "/" + printFile, data=json) as r:
                data = r
                log.debug(data)