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
        if collections.Counter(bannedEvents)[event] == 0:
            frequencyTable = await events.createTeamFrequencyTable(event)
            print(frequencyTable)
            scoreMatrix = await events.createScoreMatrix(event)
            print(scoreMatrix)
            autoHighMatrix = await events.createAutoHighMatrix(event)
            print(autoHighMatrix)
            autoMidMatrix = await events.createAutoMidMatrix(event)
            autoLowMatrix = await events.createAutoLowMatrix(event)
            teleHighMatrix = await events.createTeleHighMatrix(event)
            teleMidMatrix = await events.createTeleMidMatrix(event)
            teleLowMatrix = await events.createTeleLowMatrix(event)

            oprTable = np.multiply(frequencyTable,scoreMatrix)
            autoHighTable = np.multiply(frequencyTable,autoHighMatrix)
            autoMidTable = np.multiply(frequencyTable,autoMidMatrix)
            autoLowTable = np.multiply(frequencyTable,autoLowMatrix)
            teleHighTable = np.multiply(frequencyTable,teleHighMatrix)
            teleMidTable = np.multiply(frequencyTable,teleMidMatrix)
            teleLowTable = np.multiply(frequencyTable,teleLowMatrix)

            jsonString.update({event:{
                "frequencyTable":frequencyTable.tolist(),
                "oprTable":oprTable.tolist(),
                "autoHighTable":autoHighTable.tolist(),
                "autoMidTable":autoMidTable.tolist(),
                "autoLowTable":autoLowTable.tolist(),
                "teleHighTable":teleHighTable.tolist(),
                "teleMidTable":teleMidTable.tolist(),
                "teleLowTable":teleLowTable.tolist()
            }})
            print(event)
    with open("events2023.json", "w") as outfile:
        json.dump(jsonString, outfile)
    return "Bet this didn't work lol"


            


