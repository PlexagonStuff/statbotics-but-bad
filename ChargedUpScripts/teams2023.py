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
        if collections.Counter(bannedEvents)[event] == 0 and not(await tba.getEventMatches(event) == []) and not(await tba.getEventType(event) == "Offseason" or await tba.getEventType(event) == "Preseason"):
            jsonString[event]=await createTeamSingleEvent(team,event)
    return jsonString


async def createTeamSingleEvent(team:str,event:str):
    bannedEvents = ["2023micmp","2023cmptx","2023txcmp","2023nccmp","2023necmp","2023oncmp","2023chcmp","2023pncmp","2023mrcmp","2023iscmp","2023incmp","2023gacmp"]
    if collections.Counter(bannedEvents)[event] == 0 and not(await tba.getEventMatches(event) == []) and not(await tba.getEventType(event) == "Offseason" or await tba.getEventType(event) == "Preseason"):
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


async def getOverallMatchRecord(team):
    bannedEvents = ["2023micmp","2023cmptx","2023txcmp","2023nccmp","2023necmp","2023oncmp","2023chcmp","2023pncmp","2023mrcmp","2023iscmp","2023incmp","2023gacmp"]
    eventList = await tba.getTeamEvents(team,2023)
    wins = 0
    losses = 0
    ties = 0
    for event in eventList:
        if not(await tba.getEventMatches(event) == []) and not(await tba.getEventType(event) == "Offseason" or await tba.getEventType(event) == "Preseason"):
            matchListSimple = await tba.getTeamMatchesSimple(team,event)
            for match in matchListSimple:
               if match["actual_time"] != None: # I hate Granite State, why did there have to be a snow storm smh. I am so lucky a well-known team got stuck in this mess.
                alliance = "idk"
                if collections.Counter(match["alliances"]["blue"]["team_keys"])[team] == 0:
                    alliance = "red"
                else:
                    alliance = "blue"
                winningAlliance = match["winning_alliance"]
                if winningAlliance == "":
                    ties += 1
                elif winningAlliance == alliance:
                    wins += 1
                else:
                    losses += 1
    return {"wins":wins,"losses":losses,"ties":ties}
                   
