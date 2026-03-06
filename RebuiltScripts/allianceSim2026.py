import math
import numpy as np
from APIRequests import statbotics,tba
import json
from RebuiltScripts import events2026, teams2026
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
    team1Data = await teams2026.createTeam(team1)
    team2Data = await teams2026.createTeam(team2)
    team3Data = await teams2026.createTeam(team3)
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
    autoBalls = (team1BestEvent["autoBalls"] + team2BestEvent["autoBalls"] + team3BestEvent["autoBalls"])
    teleBalls = (team1BestEvent["teleBalls"] + team2BestEvent["teleBalls"] + team3BestEvent["teleBalls"])
    transitionBalls = (team1BestEvent["transitionBalls"] + team2BestEvent["transitionBalls"] + team3BestEvent["transitionBalls"])
    autoPoints = autoBalls + team1BestEvent["autoTower"] + team2BestEvent["autoTower"] + team3BestEvent["autoTower"] + team1BestEvent["endGameTower"] + team2BestEvent["endGameTower"] + team3BestEvent["endGameTower"]
    #Tele L4 Calc, include runoff
    teleopPoints = teleBalls + transitionBalls 
    endGamePoints = team1BestEvent["endGameTower"] + team2BestEvent["endGameTower"] + team3BestEvent["endGameTower"]
    totalScore = autoPoints + teleopPoints + endGamePoints
    return {
        "alliance": [team1, team2, team3],
        "totalScore": auto_round(totalScore),
        "autoScore": auto_round(autoPoints),
        "teleopScore": auto_round(teleopPoints),
        "endGameScore": auto_round(endGamePoints),
        "teleBalls": auto_round(teleBalls),
        "autoBalls": auto_round(autoBalls),
        "transitionBalls": auto_round(transitionBalls)
    }

async def predictMatchScoreGivenEvent(team1:str, team2:str, team3:str, event:str):
    team1Data = await teams2026.createTeam(team1)
    team2Data = await teams2026.createTeam(team2)
    team3Data = await teams2026.createTeam(team3)
    #Grab the best performing event for each alliance member, this is fantasy land!
    team1BestEvent = team1Data[event]
    team2BestEvent = team2Data[event]
    team3BestEvent = team3Data[event]
    autoBalls = (team1BestEvent["autoBalls"] + team2BestEvent["autoBalls"] + team3BestEvent["autoBalls"])
    teleBalls = (team1BestEvent["teleBalls"] + team2BestEvent["teleBalls"] + team3BestEvent["teleBalls"])
    transitionBalls = (team1BestEvent["transitionBalls"] + team2BestEvent["transitionBalls"] + team3BestEvent["transitionBalls"])
    autoPoints = autoBalls + team1BestEvent["autoTower"] + team2BestEvent["autoTower"] + team3BestEvent["autoTower"] + team1BestEvent["endGameTower"] + team2BestEvent["endGameTower"] + team3BestEvent["endGameTower"]
    #Tele L4 Calc, include runoff
    teleopPoints = teleBalls + transitionBalls 
    endGamePoints = team1BestEvent["endGameTower"] + team2BestEvent["endGameTower"] + team3BestEvent["endGameTower"]
    totalScore = autoPoints + teleopPoints + endGamePoints
    return {
        "alliance": [team1, team2, team3],
        "totalScore": auto_round(totalScore),
        "autoScore": auto_round(autoPoints),
        "teleopScore": auto_round(teleopPoints),
        "endGameScore": auto_round(endGamePoints),
        "teleBalls": auto_round(teleBalls),
        "autoBalls": auto_round(autoBalls),
        "transitionBalls": auto_round(transitionBalls)
    }


