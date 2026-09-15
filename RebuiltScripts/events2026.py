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

async def createAlgaeFrequencyTable(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros((numOfTeams,numOfTeams))
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if not(match["score_breakdown"] is None):
               for team1 in match["alliances"]["blue"]["team_keys"]:
                   for team2 in match["alliances"]["blue"]["team_keys"]:
                       matrix[teamList.index(team1)][teamList.index(team2)] +=1
    for match in eventMatches:
          if not(match["score_breakdown"] is None):
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

async def createAutoBallsMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    matrix[teamList.index(team)] += match["score_breakdown"]["blue"]["hubScore"]["autoCount"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    matrix[teamList.index(team)] += match["score_breakdown"]["red"]["hubScore"]["autoCount"]
    return matrix

async def createTeleBallsMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    matrix[teamList.index(team)] += match["score_breakdown"]["blue"]["hubScore"]["teleopCount"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    matrix[teamList.index(team)] += match["score_breakdown"]["red"]["hubScore"]["teleopCount"]
    return matrix

async def createTransitionBallsMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    matrix[teamList.index(team)] += match["score_breakdown"]["blue"]["hubScore"]["transitionCount"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    matrix[teamList.index(team)] += match["score_breakdown"]["red"]["hubScore"]["transitionCount"]
    return matrix

async def createEvent(event:str):
     if not(await tba.getEventType(event) == "Offseason" or await tba.getEventType(event) == "Preseason"):
          freqTable = await createTeamFrequencyTable(event)
          algFreqTable = await createAlgaeFrequencyTable(event)
          oprMatrix = await createScoreMatrix(event)
          autoBallMatrix = await createAutoBallsMatrix(event)
          teleBallMatrix = await createTeleBallsMatrix(event)
          transitionBallMatrix = await createTransitionBallsMatrix(event)

          oprTable = np.dot(freqTable,oprMatrix).tolist()

          return {
               "eventKey":event,
               "oprs":oprTable,
               "autoBalls":np.dot(freqTable,autoBallMatrix).tolist(),
               "teleBalls":np.dot(freqTable,teleBallMatrix).tolist(),
               "transitionBalls":np.dot(freqTable,transitionBallMatrix).tolist()
          }
     else:
          return {"error":"This is an offseason or preseason event, and I do not care because something will break."}








async def processTeamMatches(team:str,event:str):
     print(team)
     matchData = await tba.getTeamMatches(team,event)
     averageAutoTowerPoints = 0.0
     averageEndGameTowerPoints = 0.0
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
               endGameTowerStatus = allianceScoring["endGameTower"+robotNumber]
               autoTowerStatus = allianceScoring["autoTower"+robotNumber]
               if (autoTowerStatus == "Level1"):
                    averageAutoTowerPoints += 15
               if (endGameTowerStatus == "Level1"):
                    averageEndGameTowerPoints += 10
               elif (endGameTowerStatus == "Level2"):
                    averageEndGameTowerPoints == 20
               elif (endGameTowerStatus == "Level3"):
                    averageEndGameTowerPoints += 30
               elif (endGameTowerStatus == "None"):
                    averageEndGameTowerPoints += 0
     averageAutoTowerPoints /= len(matchData)
     averageEndGameTowerPoints /= len(matchData)
     return {"autoTower":averageAutoTowerPoints,"endGameTower":averageEndGameTowerPoints}
