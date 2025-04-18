import math
import numpy as np
from APIRequests import statbotics,tba
import json
from ReefscapeScripts import events2025, teams2025
import collections


def auto_round(number):
    """
    Automatically chooses to round up or down based on the decimal value.
    Rounds up if the decimal is >= 0.5, otherwise rounds down.
    """
    if number - math.floor(number) >= 0.5:
        return math.ceil(number)
    else:
        return math.floor(number)

async def predictMatchScore(team1:str, team2:str, team3:str):
    team1Data = await teams2025.createTeam(team1)
    team2Data = await teams2025.createTeam(team2)
    team3Data = await teams2025.createTeam(team3)
    #Grab the best performing event for each alliance member, this is fantasy land!
    team1BestEvent = list(team1Data.values())[0]
    team2BestEvent = list(team2Data.values())[0]
    team3BestEvent = list(team3Data.values())[0]
    for k in team1Data:
        if team1Data[k]["contribution"] > team1BestEvent["contribution"]:
            team1BestEvent = team1Data[k]
    for k in team2Data:
        if team2Data[k]["contribution"] > team2BestEvent["contribution"]:
            team2BestEvent = team2Data[k]
    for k in team3Data:
        if team3Data[k]["contribution"] > team3BestEvent["contribution"]:
            team3BestEvent = team3Data[k]
    print(team1BestEvent)
    print(team2BestEvent)
    print(team3BestEvent)
    totalL4 = 0.0
    totalL3 = 0.0
    totalL2 = 0.0
    totalL1 = 0.0
    autoL4 = (team1BestEvent["autoL4Count"] + team2BestEvent["autoL4Count"] + team3BestEvent["autoL4Count"])
    autoL3 = (team1BestEvent["autoL3Count"] + team2BestEvent["autoL3Count"] + team3BestEvent["autoL3Count"])
    autoL2 = (team1BestEvent["autoL2Count"] + team2BestEvent["autoL2Count"] + team3BestEvent["autoL2Count"])
    autoL1 = (team1BestEvent["autoL1Count"] + team2BestEvent["autoL1Count"] + team3BestEvent["autoL1Count"])
    totalL4 += autoL4
    totalL3 += autoL3
    totalL2 += autoL2
    totalL1 += autoL1
    autoL4Points = totalL4 * 7.0
    autoL3Points = totalL3 * 6.0
    autoL2Points = totalL2 * 4.0
    autoL1Points = totalL1 * 1.0
    autoPoints = team1BestEvent["mobility"] + team2BestEvent["mobility"] + team3BestEvent["mobility"] + autoL4Points + autoL3Points + autoL2Points + autoL1Points
    #Tele L4 Calc, include runoff
    teleL4 = team1BestEvent["teleL4Count"] + team2BestEvent["teleL4Count"] + team3BestEvent["teleL4Count"]
    totalL4 += teleL4
    teleL4Points = 0
    L4Remainder = (totalL4 % 12) if ((totalL4 % 12) != totalL4) else 0
    if L4Remainder == 0:
        teleL4Points = teleL4 * 5.0
    else:
        teleL4Points = (12 - autoL4) * 5.0
    #Tele L3 Calc, include runoff
    teleL3 = L4Remainder + team1BestEvent["teleL3Count"] + team2BestEvent["teleL3Count"] + team3BestEvent["teleL3Count"]
    totalL3 += teleL3
    teleL3Points = 0
    L3Remainder = (totalL3 % 12) if ((totalL3 % 12) != totalL3) else 0
    if L3Remainder == 0:
        teleL3Points = teleL3 * 4.0
    else:
        teleL3Points = (12 - autoL3) * 4.0
    #Tele L2 Calc, include runoff
    teleL2 = L3Remainder + team1BestEvent["teleL2Count"] + team2BestEvent["teleL2Count"] + team3BestEvent["teleL2Count"]
    totalL2 += teleL2
    teleL2Points = 0
    L2Remainder = (totalL2 % 12) if ((totalL2 % 12) != totalL2) else 0
    if L2Remainder == 0:
        teleL2Points = teleL2 * 3.0
    else:
        teleL2Points = (12 - autoL2) * 3.0
    #Tele L1 Calc, include some runoff because not all teams are designed to score L1, let's say 15% runoff for no reason
    teleL1 = (L2Remainder * 0.15) + team1BestEvent["teleL1Count"] + team2BestEvent["teleL1Count"] + team3BestEvent["teleL1Count"]
    totalL1 += teleL1
    teleL1Points = teleL1 * 2.0
    processorCount = team1BestEvent["processorCount"] + team2BestEvent["processorCount"] + team3BestEvent["processorCount"]
    processorPoints = processorCount * 6.0
    netAlgaeCount = team1BestEvent["netAlgaeCount"] + team2BestEvent["netAlgaeCount"] + team3BestEvent["netAlgaeCount"]
    netAlgaePoints = netAlgaeCount * 4.0
    teleopPoints = teleL4Points + teleL3Points + teleL2Points + teleL1Points + processorPoints + netAlgaePoints
    endGamePoints = team1BestEvent["barge"] + team2BestEvent["barge"] + team3BestEvent["barge"]
    totalScore = autoPoints + teleopPoints + endGamePoints
    return {
        "alliance": [team1, team2, team3],
        "totalScore": auto_round(totalScore),
        "autoScore": auto_round(autoPoints),
        "teleopScore": auto_round(teleopPoints),
        "bargeScore": auto_round(endGamePoints),
        "autoL4": auto_round(autoL4),
        "autoL3":auto_round(autoL3),
        "autoL2": auto_round(autoL2),
        "autoL1": auto_round(autoL1),
        "totalL4": auto_round(min(totalL4,12)),
        "totalL3": auto_round(min(totalL3,12)),
        "totalL2": auto_round(min(totalL2,12)),
        "totalL1": auto_round(totalL1),
        "processorCount": auto_round(processorCount),
        "netAlgaeCount": auto_round(netAlgaeCount)
    }

async def predictMatchScoreGivenEvent(team1:str, team2:str, team3:str, event:str):
    team1Data = await teams2025.createTeam(team1)
    team2Data = await teams2025.createTeam(team2)
    team3Data = await teams2025.createTeam(team3)
    #Grab the best performing event for each alliance member, this is fantasy land!
    team1BestEvent = team1Data[event]
    team2BestEvent = team2Data[event]
    team3BestEvent = team3Data[event]
    print(team1BestEvent)
    print(team2BestEvent)
    print(team3BestEvent)
    totalL4 = 0.0
    totalL3 = 0.0
    totalL2 = 0.0
    totalL1 = 0.0
    autoL4 = (team1BestEvent["autoL4Count"] + team2BestEvent["autoL4Count"] + team3BestEvent["autoL4Count"])
    autoL3 = (team1BestEvent["autoL3Count"] + team2BestEvent["autoL3Count"] + team3BestEvent["autoL3Count"])
    autoL2 = (team1BestEvent["autoL2Count"] + team2BestEvent["autoL2Count"] + team3BestEvent["autoL2Count"])
    autoL1 = (team1BestEvent["autoL1Count"] + team2BestEvent["autoL1Count"] + team3BestEvent["autoL1Count"])
    totalL4 += autoL4
    totalL3 += autoL3
    totalL2 += autoL2
    totalL1 += autoL1
    autoL4Points = totalL4 * 7.0
    autoL3Points = totalL3 * 6.0
    autoL2Points = totalL2 * 4.0
    autoL1Points = totalL1 * 1.0
    autoPoints = team1BestEvent["mobility"] + team2BestEvent["mobility"] + team3BestEvent["mobility"] + autoL4Points + autoL3Points + autoL2Points + autoL1Points
    #Tele L4 Calc, include runoff
    teleL4 = team1BestEvent["teleL4Count"] + team2BestEvent["teleL4Count"] + team3BestEvent["teleL4Count"]
    totalL4 += teleL4
    teleL4Points = 0
    L4Remainder = (totalL4 % 12) if ((totalL4 % 12) != totalL4) else 0
    if L4Remainder == 0:
        teleL4Points = teleL4 * 5.0
    else:
        teleL4Points = (12 - autoL4) * 5.0
    #Tele L3 Calc, include runoff
    teleL3 = L4Remainder + team1BestEvent["teleL3Count"] + team2BestEvent["teleL3Count"] + team3BestEvent["teleL3Count"]
    totalL3 += teleL3
    teleL3Points = 0
    L3Remainder = (totalL3 % 12) if ((totalL3 % 12) != totalL3) else 0
    if L3Remainder == 0:
        teleL3Points = teleL3 * 4.0
    else:
        teleL3Points = (12 - autoL3) * 4.0
    #Tele L2 Calc, include runoff
    teleL2 = L3Remainder + team1BestEvent["teleL2Count"] + team2BestEvent["teleL2Count"] + team3BestEvent["teleL2Count"]
    totalL2 += teleL2
    teleL2Points = 0
    L2Remainder = (totalL2 % 12) if ((totalL2 % 12) != totalL2) else 0
    if L2Remainder == 0:
        teleL2Points = teleL2 * 3.0
    else:
        teleL2Points = (12 - autoL2) * 3.0
    #Tele L1 Calc, include some runoff because not all teams are designed to score L1, let's say 15% runoff for no reason
    teleL1 = (L2Remainder * 0.15) + team1BestEvent["teleL1Count"] + team2BestEvent["teleL1Count"] + team3BestEvent["teleL1Count"]
    totalL1 += teleL1
    teleL1Points = teleL1 * 2.0
    processorCount = team1BestEvent["processorCount"] + team2BestEvent["processorCount"] + team3BestEvent["processorCount"]
    processorPoints = processorCount * 6.0
    netAlgaeCount = team1BestEvent["netAlgaeCount"] + team2BestEvent["netAlgaeCount"] + team3BestEvent["netAlgaeCount"]
    netAlgaePoints = netAlgaeCount * 4.0
    teleopPoints = teleL4Points + teleL3Points + teleL2Points + teleL1Points + processorPoints + netAlgaePoints
    endGamePoints = team1BestEvent["barge"] + team2BestEvent["barge"] + team3BestEvent["barge"]
    totalScore = autoPoints + teleopPoints + endGamePoints
    return {
        "alliance": [team1, team2, team3],
        "totalScore": auto_round(totalScore),
        "autoScore": auto_round(autoPoints),
        "teleopScore": auto_round(teleopPoints),
        "bargeScore": auto_round(endGamePoints),
        "autoL4": auto_round(autoL4),
        "autoL3":auto_round(autoL3),
        "autoL2": auto_round(autoL2),
        "autoL1": auto_round(autoL1),
        "totalL4": auto_round(min(totalL4,12)),
        "totalL3": auto_round(min(totalL3,12)),
        "totalL2": auto_round(min(totalL2,12)),
        "totalL1": auto_round(totalL1),
        "processorCount": auto_round(processorCount),
        "netAlgaeCount": auto_round(netAlgaeCount)
    }

