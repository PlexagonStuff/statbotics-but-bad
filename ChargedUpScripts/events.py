import numpy as np
from APIRequests import statbotics,tba
import json
import collections

async def createTeamFrequencyTable(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros((numOfTeams,numOfTeams))
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm" and not(match["score_breakdown"] is None):
               for team1 in match["alliances"]["blue"]["team_keys"]:
                   for team2 in match["alliances"]["blue"]["team_keys"]:
                       matrix[teamList.index(team1)][teamList.index(team2)] +=1
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team1 in match["alliances"]["red"]["team_keys"]:
                   for team2 in match["alliances"]["red"]["team_keys"]:
                       matrix[teamList.index(team1)][teamList.index(team2)] +=1
    return np.linalg.pinv(matrix)

async def createScoreMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    matrix[teamList.index(team)] += match["alliances"]["blue"]["score"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    matrix[teamList.index(team)] += match["alliances"]["red"]["score"]
    return matrix

async def createAutoHighMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["T"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["T"])["Cube"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["T"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["T"])["Cube"]               
    return matrix

async def createAutoMidMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["M"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["M"])["Cube"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["M"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["M"])["Cube"]               
    return matrix

async def createAutoLowMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["B"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["B"])["Cube"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["B"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["B"])["Cube"]               
    return matrix

async def createTeleHighMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["T"])["Cone"] + collections.Counter(allianceScoring["teleopCommunity"]["T"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["T"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["T"])["Cube"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["T"])["Cone"] + collections.Counter(allianceScoring["teleopCommunity"]["T"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["T"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["T"])["Cube"])               
    return matrix

async def createTeleMidMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["M"])["Cone"] + collections.Counter(allianceScoring["teleopCommunity"]["M"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["M"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["M"])["Cube"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["M"])["Cone"] + collections.Counter(allianceScoring["teleopCommunity"]["M"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["M"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["M"])["Cube"])               
    return matrix


async def createTeleLowMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["B"])["Cone"] + collections.Counter(allianceScoring["teleopCommunity"]["B"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["B"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["B"])["Cube"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["B"])["Cone"] + collections.Counter(allianceScoring["teleopCommunity"]["B"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["B"])["Cone"] + collections.Counter(allianceScoring["autoCommunity"]["B"])["Cube"])               
    return matrix

async def createTotalMatchPiecesMatrix(event:str):
     teamList = await tba.getEventTeams(event)
     numOfTeams = len(teamList)
     matrix = np.zeros(numOfTeams)
     eventMatches = await tba.getEventMatches(event)
     for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += allianceScoring["teleopGamePieceCount"]
     for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += allianceScoring["teleopGamePieceCount"]
     return matrix


async def createAutoMatchPiecesMatrix(event:str):
     teamList = await tba.getEventTeams(event)
     numOfTeams = len(teamList)
     matrix = np.zeros(numOfTeams)
     eventMatches = await tba.getEventMatches(event)
     for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += allianceScoring["autoGamePieceCount"]
     for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += allianceScoring["autoGamePieceCount"]
     return matrix

async def processTeamMatches(team:str,event:str):
     print(team)
     matchData = await tba.getTeamMatches(team,event)
     averageAutoClimbPoints = 0.0
     averageTeleClimbPoints = 0.0
     averageMobilityPoints = 0.0

     for match in matchData:
          print(match)
          if not(match["score_breakdown"] is None):
               alliance = "idk"
               robotNumber = "robot0"
               if collections.Counter(match["alliances"]["blue"]["team_keys"])[team] == 0:
                    alliance = "red"
                    robotIndex = match["alliances"][alliance]["team_keys"].index(team) + 1
                    robotNumber = "Robot"+str(robotIndex)
               else:
                    alliance = "blue"
                    robotIndex = match["alliances"][alliance]["team_keys"].index(team) + 1
                    robotNumber = "Robot"+str(robotIndex)
               allianceScoring = match["score_breakdown"][alliance]
               autoBridgeState = allianceScoring["autoBridgeState"]
               autoChargeStationPoints = allianceScoring["autoChargeStation"+robotNumber]
               if (autoChargeStationPoints == "Docked"):
                 if (autoBridgeState == "Level"):
                    averageAutoClimbPoints += 12
               
                 else:
                    averageAutoClimbPoints += 8
               else:
                 averageAutoClimbPoints += 0

               teleBridgeState = allianceScoring["endGameBridgeState"]
               teleChargeStationPoints = allianceScoring["endGameChargeStation"+robotNumber]
               if (teleChargeStationPoints == "Docked"):
                if (teleBridgeState == "Level"):
                     averageTeleClimbPoints += 10
                else :
                    averageAutoClimbPoints += 6
               elif (teleChargeStationPoints == "Park"):
                averageTeleClimbPoints += 2
               else:
                averageTeleClimbPoints += 0
               if allianceScoring["mobility"+robotNumber] == "Yes":
                averageMobilityPoints += 3
               else:
                averageMobilityPoints += 0
     averageAutoClimbPoints /= len(matchData)
     averageTeleClimbPoints /= len(matchData)
     averageMobilityPoints /= len(matchData)
     return {"autoClimb":averageAutoClimbPoints,"teleClimb":averageTeleClimbPoints,"mobility":averageMobilityPoints}
