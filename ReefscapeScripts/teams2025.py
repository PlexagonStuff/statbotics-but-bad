import numpy as np
from APIRequests import statbotics,tba
from ReefscapeScripts import events2025
import json
import collections

async def createTeam(team:str):
    eventList = await tba.getTeamEvents(team,2025)
    jsonString = {}
    testDict = {}
    for event in eventList:
        if not(await tba.getEventMatches(event) == []) and not(await tba.getEventOPRs(event) == {}) and not(await tba.getEventType(event) == "Offseason" or await tba.getEventType(event) == "Preseason"):
            jsonString[event]=await createTeamSingleEvent(team,event)
    return jsonString


async def createTeamSingleEvent(team:str,event:str):
    if not(await tba.getEventMatches(event) == []) and not(await tba.getEventOPRs(event) == {}) and not(await tba.getEventType(event) == "Offseason" or await tba.getEventType(event) == "Preseason"):
        teamList = await tba.getEventTeams(event)
        teamIndex = teamList.index(team)
        eventData = await events2025.createEvent(event)
        opr = eventData["oprs"][teamIndex]
        dpr = (await tba.getEventOPRs(event))["dprs"][team]
        autoL4 = eventData["autoL4"][teamIndex]
        autoL3 = eventData["autoL3"][teamIndex]
        autoL2 = eventData["autoL2"][teamIndex]
        autoL1 = eventData["autoL1"][teamIndex]
        teleL4 = eventData["teleL4"][teamIndex]
        teleL3 = eventData["teleL3"][teamIndex]
        teleL2 = eventData["teleL2"][teamIndex]
        teleL1 = eventData["teleL1"][teamIndex]
        processor = eventData["processor"][teamIndex]
        netAlgae = eventData["netAlgae"][teamIndex]
        #Keys: barge, mobility
        otherData = await events2025.processTeamMatches(team,event)

        totalPieces = autoL4 + autoL3 + autoL2 + autoL1 + teleL4 + teleL3 + teleL2 + teleL1

        contribution = (autoL4 * 7.0) + (autoL3 * 6.0) + (autoL2* 4.0) + (autoL1 * 3.0) + (teleL4 * 5.0) + (teleL3* 4.0) + (teleL2* 3.0) + (teleL1 * 2.0) + (processor * 6.0) + (netAlgae * 4.0) + otherData["barge"] + otherData["mobility"]
        epa = await statbotics.getTeamEPA(team, event)
        print(totalPieces)
        return {
            "autoL4Count": autoL4,
            "autoL3Count": autoL3,
            "autoL2Count": autoL2,
            "autoL1Count": autoL1,
            "teleL4Count": teleL4,
            "teleL3Count": teleL3,
            "teleL2Count": teleL2,
            "teleL1Count": teleL1,
            "processorCount": processor,
            "netAlgaeCount": netAlgae,
            "barge": otherData["barge"],
            "mobility": otherData["mobility"],
            "contribution": contribution,
            "epa": epa,
            "opr": opr,
            "dpr": dpr
        }
    else:
        return {"error":"Event has not played matches yet"}


async def getOverallMatchRecord(team):
    bannedEvents = ["2023micmp","2023cmptx","2023txcmp","2023nccmp","2023necmp","2023oncmp","2023chcmp","2023pncmp","2023mrcmp","2023iscmp","2023incmp","2023gacmp"]
    eventList = await tba.getTeamEvents(team,2025)
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

async def getTeamAwards(team):
    teamAwards = await tba.getTeamAwards(team,2025)
    blueBanner = 0
    awards = 0
    for award in teamAwards:
        if (not(await tba.getEventType(award["event_key"]) == "Offseason" or await tba.getEventType(award["event_key"]) == "Preseason")):
            awards += 1
            if (award["award_type"] == 0 or award["award_type"] == 1):
                blueBanner += 1
    return {"awards":awards,"blueBanners":blueBanner}
                   
