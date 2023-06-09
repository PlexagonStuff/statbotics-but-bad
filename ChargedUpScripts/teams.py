import numpy as np
from APIRequests import statbotics,tba
from ChargedUpScripts import events
import json
import collections

async def createTeam(team:str):
    bannedEvents = ["2023micmp","2023cmptx","2023txcmp","2023nccmp","2023necmp","2023oncmp","2023chcmp","2023pncmp","2023mrcmp","2023iscmp","2023incmp","2023gacmp"]
    eventList = await tba.getTeamEvents(team,2023)
    jsonString = {}
    testDict = {}
    for event in eventList:
        if collections.Counter(bannedEvents)[event] == 0 and not(await tba.getEventMatches(event) == []):
            teamList = await tba.getEventTeams(event)
            invMatrix = await events.createTeamFrequencyTable(event)
            oprMatrix = await events.createScoreMatrix(event)
            autoHighMatrix = await events.createAutoHighMatrix(event)
            autoMidMatrix = await events.createAutoMidMatrix(event)
            autoLowMatrix = await events.createAutoLowMatrix(event)
            teleHighMatrix = await events.createTeleHighMatrix(event)
            teleMidMatrix = await events.createTeleMidMatrix(event)
            teleLowMatrix = await events.createTeleLowMatrix(event)

            teamIndex = teamList.index(team)

            opr = np.dot(invMatrix,oprMatrix)[teamIndex]
            autoHigh = np.dot(invMatrix,autoHighMatrix)[teamIndex]
            autoLow = np.dot(invMatrix,autoLowMatrix)[teamIndex]
            autoMid = np.dot(invMatrix,autoMidMatrix)[teamIndex]
            teleHigh = np.dot(invMatrix,teleHighMatrix)[teamIndex]
            teleMid = np.dot(invMatrix,teleMidMatrix)[teamIndex]
            teleLow = np.dot(invMatrix,teleLowMatrix)[teamIndex]

            #Keys: autoClimb, teleClimb, mobility
            otherData = await events.processTeamMatches(team,event)

            totalPieces = autoHigh + autoLow + autoMid + teleHigh + teleMid + teleLow
            linkPoints = (totalPieces/3.0) * 5.0

            contribution = (autoHigh * 6.0) + (autoMid * 4.0) + (autoLow * 3.0) + (teleHigh * 5.0) + (teleMid * 3.0) + (teleLow * 2.0) + otherData["autoClimb"]  + otherData["teleClimb"] + otherData["mobility"] + linkPoints
            epa = await statbotics.getTeamEPA(team, event)
            jsonString[event]={"autoHigh":autoHigh, "autoMid":autoMid, "autoLow":autoLow, "teleHigh":teleHigh, "teleMid":teleMid, "teleLow":teleLow, "autoClimb":otherData["autoClimb"],"teleClimb":otherData["teleClimb"],"mobility":otherData["mobility"],"contribution":contribution,"opr":opr,"epa":epa}
    return jsonString


async def createTeamSingleEvent(team:str,event:str):
    bannedEvents = ["2023micmp","2023cmptx","2023txcmp","2023nccmp","2023necmp","2023oncmp","2023chcmp","2023pncmp","2023mrcmp","2023iscmp","2023incmp","2023gacmp"]
    if collections.Counter(bannedEvents)[event] == 0 and not(await tba.getEventMatches(event) == []):
        teamList = await tba.getEventTeams(event)
        invMatrix = await events.createTeamFrequencyTable(event)
        oprMatrix = await events.createScoreMatrix(event)
        autoHighMatrix = await events.createAutoHighMatrix(event)
        autoMidMatrix = await events.createAutoMidMatrix(event)
        autoLowMatrix = await events.createAutoLowMatrix(event)
        teleHighMatrix = await events.createTeleHighMatrix(event)
        teleMidMatrix = await events.createTeleMidMatrix(event)
        teleLowMatrix = await events.createTeleLowMatrix(event)

        teamIndex = teamList.index(team)

        opr = np.dot(invMatrix,oprMatrix)[teamIndex]
        autoHigh = np.dot(invMatrix,autoHighMatrix)[teamIndex]
        autoLow = np.dot(invMatrix,autoLowMatrix)[teamIndex]
        autoMid = np.dot(invMatrix,autoMidMatrix)[teamIndex]
        teleHigh = np.dot(invMatrix,teleHighMatrix)[teamIndex]
        teleMid = np.dot(invMatrix,teleMidMatrix)[teamIndex]
        teleLow = np.dot(invMatrix,teleLowMatrix)[teamIndex]

        #Keys: autoClimb, teleClimb, mobility
        otherData = await events.processTeamMatches(team,event)

        totalPieces = autoHigh + autoLow + autoMid + teleHigh + teleMid + teleLow
        linkPoints = (totalPieces/3.0) * 5.0

        contribution = (autoHigh * 6.0) + (autoMid * 4.0) + (autoLow * 3.0) + (teleHigh * 5.0) + (teleMid * 3.0) + (teleLow * 2.0) + otherData["autoClimb"]  + otherData["teleClimb"] + otherData["mobility"] + linkPoints
        epa = await statbotics.getTeamEPA(team, event)
        return {"eventKey":event,"autoHigh":autoHigh, "autoMid":autoMid, "autoLow":autoLow, "teleHigh":teleHigh, "teleMid":teleMid, "teleLow":teleLow, "autoClimb":otherData["autoClimb"],"teleClimb":otherData["teleClimb"],"mobility":otherData["mobility"],"contribution":contribution,"opr":opr,"epa":epa}
    else:
        return {"error":"Event has not played matches yet"}

