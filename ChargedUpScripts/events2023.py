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

async def createAutoHighConesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["T"])["Cone"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["T"])["Cone"]               
    return matrix

async def createAutoHighCubesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["T"])["Cube"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["T"])["Cube"]               
    return matrix

async def createAutoMidConesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["M"])["Cone"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["M"])["Cone"]              
    return matrix

async def createAutoMidCubesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["M"])["Cube"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["M"])["Cube"]               
    return matrix

async def createAutoLowConesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["B"])["Cone"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["B"])["Cone"]
    return matrix

async def createAutoLowCubesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["B"])["Cube"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["autoCommunity"]["B"])["Cube"]               
    return matrix
#Note to Nick tomorrow, finish creating cone and cube parts plz thx


async def createTeleHighConesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["T"])["Cone"]-(collections.Counter(allianceScoring["autoCommunity"]["T"])["Cone"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["T"])["Cone"]-(collections.Counter(allianceScoring["autoCommunity"]["T"])["Cone"])               
    return matrix

async def createTeleHighCubesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["T"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["T"])["Cube"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["T"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["T"])["Cube"])               
    return matrix

async def createTeleMidConesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["M"])["Cone"]-(collections.Counter(allianceScoring["autoCommunity"]["M"])["Cone"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["M"])["Cone"]-(collections.Counter(allianceScoring["autoCommunity"]["M"])["Cone"])               
    return matrix

async def createTeleMidCubesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["M"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["M"])["Cube"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["M"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["M"])["Cube"])               
    return matrix


async def createTeleLowConesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["B"])["Cone"]-(collections.Counter(allianceScoring["autoCommunity"]["B"])["Cone"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["B"])["Cone"]-(collections.Counter(allianceScoring["autoCommunity"]["B"])["Cone"])               
    return matrix

async def createTeleLowCubesMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["B"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["B"])["Cube"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += collections.Counter(allianceScoring["teleopCommunity"]["B"])["Cube"]-(collections.Counter(allianceScoring["autoCommunity"]["B"])["Cube"])               
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


async def createEvent(event:str):
     if not(await tba.getEventType(event) == "Offseason" or await tba.getEventType(event) == "Preseason"):
          freqTable = await createTeamFrequencyTable(event)
          oprMatrix = await createScoreMatrix(event)
          autoHighConeMatrix = await createAutoHighConesMatrix(event)
          autoHighCubeMatrix = await createAutoHighCubesMatrix(event)
          autoMidConeMatrix = await createAutoMidConesMatrix(event)
          autoMidCubeMatrix = await createAutoMidCubesMatrix(event)
          autoLowConeMatrix = await createAutoMidConesMatrix(event)
          autoLowCubeMatrix = await createAutoMidCubesMatrix(event)
          teleHighConeMatrix = await createTeleHighConesMatrix(event)
          teleHighCubeMatrix = await createTeleHighCubesMatrix(event)
          teleMidConeMatrix = await createTeleMidConesMatrix(event)
          teleMidCubeMatrix = await createTeleMidCubesMatrix(event)
          teleLowConeMatrix = await createTeleLowConesMatrix(event)
          teleLowCubeMatrix = await createTeleLowCubesMatrix(event)

          oprTable = np.dot(freqTable,oprMatrix).tolist()
          autoHighConeTable = np.dot(freqTable,autoHighConeMatrix).tolist()
          autoHighCubeTable = np.dot(freqTable,autoHighCubeMatrix).tolist()
          autoMidConeTable = np.dot(freqTable,autoMidConeMatrix).tolist()
          autoMidCubeTable = np.dot(freqTable,autoMidCubeMatrix).tolist()
          autoLowConeTable = np.dot(freqTable,autoLowConeMatrix).tolist()
          autoLowCubeTable = np.dot(freqTable,autoLowCubeMatrix).tolist()
          teleHighConeTable = np.dot(freqTable,teleHighConeMatrix).tolist()
          teleHighCubeTable = np.dot(freqTable,teleHighCubeMatrix).tolist()
          teleMidConeTable = np.dot(freqTable,teleMidConeMatrix).tolist()
          teleMidCubeTable = np.dot(freqTable,teleMidCubeMatrix).tolist()
          teleLowConeTable = np.dot(freqTable,teleLowConeMatrix).tolist()
          teleLowCubeTable = np.dot(freqTable,teleLowCubeMatrix).tolist()

          return {
               "eventKey":event,
               "oprs":oprTable,
               "autoHighCones":autoHighConeTable,
               "autoHighCubes":autoHighCubeTable,
               "autoMidCones":autoMidConeTable,
               "autoMidCubes":autoMidCubeTable,
               "autoLowCones":autoLowConeTable,
               "autoLowCubes":autoLowCubeTable,
               "teleHighCones":teleHighConeTable,
               "teleHighCubes":teleHighCubeTable,
               "teleMidCones":teleMidConeTable,
               "teleMidCubes":teleMidCubeTable,
               "teleLowCones":teleLowConeTable,
               "teleLowCubes":teleLowCubeTable
          }
     else:
          return {"error":"This is an offseason or preseason event, and I do not care because something will break."}








async def processTeamMatches(team:str,event:str):
     print(team)
     matchData = await tba.getTeamMatches(team,event)
     averageAutoClimbPoints = 0.0
     averageTeleClimbPoints = 0.0
     averageMobilityPoints = 0.0

     for match in matchData:
          #print(match)
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
