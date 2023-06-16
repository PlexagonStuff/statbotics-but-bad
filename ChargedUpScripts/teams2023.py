import numpy as np
from APIRequests import statbotics,tba
from ChargedUpScripts import events2023
import json
import collections

async def createTeam(team:str):
    bannedEvents = ["2023micmp","2023cmptx","2023txcmp","2023nccmp","2023necmp","2023oncmp","2023chcmp","2023pncmp","2023mrcmp","2023iscmp","2023incmp","2023gacmp"]
    eventList = await tba.getTeamEvents(team,2023)
    jsonString = {}
    testDict = {}
    for event in eventList:
        if collections.Counter(bannedEvents)[event] == 0 and not(await tba.getEventMatches(event) == []):
            jsonString[event]=await createTeamSingleEvent(team,event)
    return jsonString


async def createTeamSingleEvent(team:str,event:str):
    bannedEvents = ["2023micmp","2023cmptx","2023txcmp","2023nccmp","2023necmp","2023oncmp","2023chcmp","2023pncmp","2023mrcmp","2023iscmp","2023incmp","2023gacmp"]
    if collections.Counter(bannedEvents)[event] == 0 and not(await tba.getEventMatches(event) == []):
        teamList = await tba.getEventTeams(event)
        teamIndex = teamList.index(team)
        eventData = await events2023.createEvent(event)
        opr = eventData["oprs"][teamIndex]
        dpr = (await tba.getEventOPRs(event))["dprs"][team]
        autoHighCones = eventData["autoHighCones"][teamIndex]
        autoHighCubes = eventData["autoHighCubes"][teamIndex]
        autoMidCones = eventData["autoMidCones"][teamIndex]
        autoMidCubes = eventData["autoMidCubes"][teamIndex]
        autoLowCones = eventData["autoLowCones"][teamIndex]
        autoLowCubes = eventData["autoLowCubes"][teamIndex]
        teleHighCones = eventData["teleHighCones"][teamIndex]
        teleHighCubes = eventData["teleHighCubes"][teamIndex]
        teleMidCones = eventData["teleMidCones"][teamIndex]
        teleMidCubes = eventData["teleMidCubes"][teamIndex]
        teleLowCones = eventData["teleLowCones"][teamIndex]
        teleLowCubes = eventData["teleLowCubes"][teamIndex]
        #Keys: autoClimb, teleClimb, mobility
        otherData = await events2023.processTeamMatches(team,event)
        
        autoHigh = autoHighCones + autoHighCubes
        autoMid = autoMidCones + autoMidCubes
        autoLow = autoLowCones + autoLowCubes
        teleHigh = teleHighCones + teleHighCubes
        teleMid = teleMidCones + teleMidCubes
        teleLow = teleLowCones + teleLowCubes

        totalPieces = autoHighCones + autoHighCubes + autoMidCones + autoMidCubes + autoLowCones + autoLowCubes + teleHighCones + teleHighCubes+ teleMidCones+teleMidCubes+teleLowCones+teleLowCubes
        linkPoints = (totalPieces/3.0) * 5.0

        contribution = (autoHigh * 6.0) + (autoMid * 4.0) + (autoLow * 3.0) + (teleHigh * 5.0) + (teleMid * 3.0) + (teleLow * 2.0) + otherData["autoClimb"]  + otherData["teleClimb"] + otherData["mobility"] + linkPoints
        epa = await statbotics.getTeamEPA(team, event)
        table = (await events2023.createTeamFrequencyTable(event))
        matri = (await events2023.createTotalMatchPiecesMatrix(event))
        print(np.dot(table,matri)[teamIndex])
        print(totalPieces)
        return {"autoHighCones":autoHighCones,"autoHighCubes":autoHighCubes,"autoMidCones":autoMidCones,"autoMidCubes":autoMidCubes,"autoLowCones":autoLowCones,"autoLowCubes":autoLowCubes,"teleHighCones":teleHighCones,"teleHighCubes":teleHighCubes,"teleMidCones":teleMidCones,"teleMidCubes":teleMidCubes,"teleLowCones":teleLowCones,"teleLowCubes":teleLowCubes,"autoClimb":otherData["autoClimb"],"teleClimb":otherData["teleClimb"],"mobility":otherData["mobility"],"contribution":contribution,"opr":opr,"dpr":dpr,"epa":epa}
    else:
        return {"error":"Event has not played matches yet"}

