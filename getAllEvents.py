import json
from ChargedUpScripts import events2023
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
            invMatrix = await events2023.createTeamFrequencyTable(event)
            oprMatrix = await events2023.createScoreMatrix(event)
            autoHighMatrix = await events2023.createAutoHighMatrix(event)
            autoMidMatrix = await events2023.createAutoMidMatrix(event)
            autoLowMatrix = await events2023.createAutoLowMatrix(event)
            teleHighMatrix = await events2023.createTeleHighMatrix(event)
            teleMidMatrix = await events2023.createTeleMidMatrix(event)
            teleLowMatrix = await events2023.createTeleLowMatrix(event)
            opr = np.dot(invMatrix,oprMatrix).tolist()
            autoHigh = np.dot(invMatrix,autoHighMatrix).tolist()
            autoLow = np.dot(invMatrix,autoLowMatrix).tolist()
            autoMid = np.dot(invMatrix,autoMidMatrix).tolist()
            teleHigh = np.dot(invMatrix,teleHighMatrix).tolist()
            teleMid = np.dot(invMatrix,teleMidMatrix).tolist()
            teleLow = np.dot(invMatrix,teleLowMatrix).tolist()

            jsonString.update({event:{
            "oprtable":opr,"autohightable":autoHigh,"automidtable":autoMid,"autolowtable":autoLow,"telehightable":teleHigh,"telemidtable":teleMid,"telelowtable":teleLow}})
            print(event)
    with open("events2023.json", "w") as outfile:
        json.dump(jsonString, outfile)
    return "Bet this didn't work lol"


            


