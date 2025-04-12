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

async def createAutoL4Matrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += allianceScoring["autoReef"]["tba_topRowCount"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += allianceScoring["autoReef"]["tba_topRowCount"]              
    return matrix

async def createAutoL3Matrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += allianceScoring["autoReef"]["tba_midRowCount"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += allianceScoring["autoReef"]["tba_midRowCount"]              
    return matrix

async def createAutoL2Matrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += allianceScoring["autoReef"]["tba_botRowCount"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += allianceScoring["autoReef"]["tba_botRowCount"]              
    return matrix

async def createAutoL1Matrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += allianceScoring["autoReef"]["trough"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += allianceScoring["autoReef"]["trough"]              
    return matrix

async def createTeleL4Matrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += (allianceScoring["teleopReef"]["tba_topRowCount"] - allianceScoring["autoReef"]["tba_topRowCount"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += (allianceScoring["teleopReef"]["tba_topRowCount"] - allianceScoring["autoReef"]["tba_topRowCount"])             
    return matrix

async def createTeleL3Matrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += (allianceScoring["teleopReef"]["tba_midRowCount"] - allianceScoring["autoReef"]["tba_midRowCount"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += (allianceScoring["teleopReef"]["tba_midRowCount"] - allianceScoring["autoReef"]["tba_midRowCount"])             
    return matrix

async def createTeleL2Matrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += (allianceScoring["teleopReef"]["tba_botRowCount"] - allianceScoring["autoReef"]["tba_botRowCount"])
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += (allianceScoring["teleopReef"]["tba_botRowCount"] - allianceScoring["autoReef"]["tba_botRowCount"])             
    return matrix

#For some reason the telop and auto troughs are somehow seperated but the other coral are not, idk :)
async def createTeleL1Matrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += allianceScoring["teleopReef"]["trough"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += allianceScoring["teleopReef"]["trough"]             
    return matrix

async def createProcessorMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += allianceScoring["wallAlgaeCount"]
    for match in eventMatches:
          if match["comp_level"] == "qm"and not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += allianceScoring["wallAlgaeCount"]           
    return matrix

#Net algae is interesting since a large amount can be created by scoring from the opponents processor so this can be mitigated 
#by subtracting by a factor of the algae that the opponent scored for you via your human player, giving the human player an accuracy of 
#90%, since they really did not seem to miss much from my personal experience. That parameter could easily be adjusted.
#For fun, I am changing the algae to not be just qualification match bound, as elims is where algae seemed to really pick up in terms of true 
#capabilties
async def createNetAlgaeMatrix(event:str):
    teamList = await tba.getEventTeams(event)
    numOfTeams = len(teamList)
    matrix = np.zeros(numOfTeams)
    eventMatches = await tba.getEventMatches(event)
    for match in eventMatches:
          if not(match["score_breakdown"] is None):
               for team in match["alliances"]["blue"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["blue"]
                    otherAllianceScoring = match["score_breakdown"]["red"]
                    matrix[teamList.index(team)] += (allianceScoring["netAlgaeCount"] - (otherAllianceScoring["wallAlgaeCount"] * 0.90))
    for match in eventMatches:
          if not(match["score_breakdown"] is None):
               for team in match["alliances"]["red"]["team_keys"]:
                    allianceScoring = match["score_breakdown"]["red"]
                    otherAllianceScoring = match["score_breakdown"]["blue"]
                    matrix[teamList.index(team)] += (allianceScoring["netAlgaeCount"] - (otherAllianceScoring["wallAlgaeCount"] * 0.90))        
    return matrix



async def createEvent(event:str):
     if not(await tba.getEventType(event) == "Offseason" or await tba.getEventType(event) == "Preseason"):
          freqTable = await createTeamFrequencyTable(event)
          algFreqTable = await createAlgaeFrequencyTable(event)
          oprMatrix = await createScoreMatrix(event)
          autoL4Matrix = await createAutoL4Matrix(event)
          autoL3Matrix = await createAutoL3Matrix(event)
          autoL2Matrix = await createAutoL2Matrix(event)
          autoL1Matrix = await createAutoL1Matrix(event)
          teleL4Matrix = await createTeleL4Matrix(event)
          teleL3Matrix = await createTeleL3Matrix(event)
          teleL2Matrix = await createTeleL2Matrix(event)
          teleL1Matrix = await createTeleL1Matrix(event)
          processorMatrix = await createProcessorMatrix(event)
          netAlgaeMatrix = await createNetAlgaeMatrix(event)

          oprTable = np.dot(freqTable,oprMatrix).tolist()

          return {
               "eventKey":event,
               "oprs":oprTable,
               "autoL4":np.dot(freqTable,autoL4Matrix).tolist(),
               "autoL3":np.dot(freqTable,autoL3Matrix).tolist(),
               "autoL2":np.dot(freqTable,autoL2Matrix).tolist(),
               "autoL1":np.dot(freqTable,autoL1Matrix).tolist(),
               "teleL4":np.dot(freqTable,teleL4Matrix).tolist(),
               "teleL3":np.dot(freqTable,teleL3Matrix).tolist(),
               "teleL2":np.dot(freqTable,teleL2Matrix).tolist(),
               "teleL1":np.dot(freqTable,teleL1Matrix).tolist(),
               "processor":np.dot(freqTable,processorMatrix).tolist(),
               "netAlgae":np.dot(algFreqTable,netAlgaeMatrix).tolist()
          }
     else:
          return {"error":"This is an offseason or preseason event, and I do not care because something will break."}








async def processTeamMatches(team:str,event:str):
     print(team)
     matchData = await tba.getTeamMatches(team,event)
     averageBargePoints = 0.0
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
               bargeStatus = allianceScoring["endGame"+robotNumber]
               if (bargeStatus == "DeepCage"):
                    averageBargePoints += 12
               elif (bargeStatus == "Parked"):
                    averageBargePoints += 2
               elif (bargeStatus == "None"):
                    averageBargePoints += 0
               else:
                    averageBargePoints += 6
               if allianceScoring["autoLine"+robotNumber] == "Yes":
                averageMobilityPoints += 3
               else:
                averageMobilityPoints += 0
     averageBargePoints /= len(matchData)
     averageMobilityPoints /= len(matchData)
     return {"barge":averageBargePoints,"mobility":averageMobilityPoints}
