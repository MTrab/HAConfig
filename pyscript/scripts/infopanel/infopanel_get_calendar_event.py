from datetime import datetime
from zoneinfo import ZoneInfo

@service
def infopanel_get_calendar_event(count=0):
    """yaml
name: infopanel_get_calendar_event
description: Get event from calendar.
fields:
  count:
     description: Number of events to fetch
     example: 3
     required: false
     selector:
       number:
         min: 1
         max: 10
         mode: box
"""
    log.debug("Got request for %i events from infopanel", count)
    num = 1
    events = ""

    now = datetime.now(tz=ZoneInfo("Europe/Copenhagen"))

    for i in range(10):
      if num > int(count):
        log.debug("Reached max count - breaking loop")
        break

      cal = state.getattr("sensor.ical_all_events_event_" + str(i))
      description = cal["summary"].replace("#heat","").replace("#dnd","")

      if not "Arbejder hjemme" in description:
        allday = cal["all_day"]

        event_text = ""

        log.debug(cal["start"])
        if allday:
          start = cal["start"].strftime('%d/%m')
          event_text = start + ": " + description
        elif cal["end"] > now:
          start = cal["start"].strftime('%d/%m %H.%M')
          event_text = start + ": " + description

        #log.debug("Sending event %i with text '%s'", num, event_text)
        #service.call("esphome", "infopanel_update_events", blocking=False, limit=10, event_id=num, text=event_text)
        if events != "": 
          events += "#"
        events += event_text

        num += 1
        
      state.set("sensor.infopanel_calendar_events", events)