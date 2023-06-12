import json
from ChargedUpScripts import events
from APIRequests import tba,statbotics
import collections
import numpy as np

bannedEvents = ["2023micmp","2023cmptx","2023txcmp","2023nccmp","2023necmp","2023oncmp","2023chcmp","2023pncmp","2023mrcmp","2023iscmp","2023incmp","2023gacmp"]
async def getAllEvents():
    eventList = await tba.getEventsInYear(2023)
    print(eventList)
    jsonString = {}
    for event in eventList:
        if collections.Counter(bannedEvents)[event] == 0 and not await tba.getEventMatches(event) == []:
            eventData = await tba.getEventMatches(event)
            print(eventData)
            jsonString.update({event:
            eventData})
            print(event)
    with open("eventMatches2023.json", "w") as outfile:
        json.dump(jsonString, outfile)
    return "Bet this didn't work lol"


            


