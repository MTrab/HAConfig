import aiohttp
import asyncio

@service
def octoprint_get_files(url, key, entity_id, origin="local"):
    """yaml
name: octoprint_get_files
description: Get file list from Octoprint server
fields:
  entity_id:
     description: input_select to populate with the file list
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
        input_select.set_options(entity_id=entity_id, options=["Vent - indlæser ..."])

        headers = { 'X-Api-Key': key }
        data = ""
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url + "?recursive=true") as r:
                data = r.json()

        options = []
        options = options + findRecursive(data, origin)
        options.sort()

        if not options:
            options.append("Ingen")

        input_select.set_options(entity_id=entity_id, options=options)

def findRecursive(data, origin = "local", subprocess = False):
    options = []
    if subprocess:
        src = "children"
        path = data['path']
    else:
        src = "files"
        path = ""

    for file in data[src]:
        if file['origin'] == origin:
            if file['type'] == "machinecode":
                fileStr = ""
                if path != file['name'] and path != "":

                    fileStr = "/" + path + "/" + file['name']
                else:
                    fileStr = file['name']

                if 'gcodeAnalysis' in file:
                    if 'estimatedPrintTime' in file["gcodeAnalysis"]:
                        time = file["gcodeAnalysis"]["estimatedPrintTime"]
                        hour = time // 3600
                        time %= 3600
                        minutes = time // 60
                        time %= 60
                        seconds = time

                        if len(str(int(hour))) == 1:
                            strHour = "0" + str(int(hour))
                        else:
                            strHour = str(int(hour))

                        if len(str(int(minutes))) == 1:
                            strMinute = "0" + str(int(minutes))
                        else:
                            strMinute = str(int(minutes))

                        if len(str(int(seconds))) == 1:
                            strSecond = "0" + str(int(seconds))
                        else:
                            strSecond = str(int(seconds))

                        timeStr = strHour + ":" + strMinute + ":" + strSecond
                        fileStr = fileStr + " (" + timeStr + ")"

                options.append(fileStr)
            elif file['type'] == "folder":
                options = options + findRecursive(file, origin, True)

    return options