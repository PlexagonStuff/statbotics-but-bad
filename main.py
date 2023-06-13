from fastapi import FastAPI
import numpy as np
import requests as requests
import json as json
from APIRequests import statbotics,tba,tbacache
from ChargedUpScripts import events,teams
import getAllEvents
import getAllMatches
app = FastAPI(title="Statbotics but Bad API",description="The REST API for Statbotics but Bad, please HTTP GET Request responsibly",version="2.33.7",)

# with open("sample.json", "w") as outfile:
#        json.dump({"message":"hello world"}, outfile)
#    with open('sample.json', 'r') as openfile:
#        json_object = json.load(openfile)






@app.get("/")
async def root():
    return "Hello!"
    #mpu.io.write("hello.json",{"Hello":"World"})
    #return await getAllEvents.getAllEvents()
@app.get("/test")
async def test():
    teamList = await tba.getEventTeams("2023midet")
    teamIndex = teamList.index("frc2337")
    table = await events.createTeamFrequencyTable("2023midet")
    totalmatrix = await events.createTotalMatchPiecesMatrix("2023midet")
    automatrix = await events.createAutoMatchPiecesMatrix("2023midet")
    return {"totalpieces":np.dot(table,totalmatrix)[teamIndex],
            "autopieces":np.dot(table,automatrix)[teamIndex],
            "total+auto pieces":np.dot(table,automatrix)[teamIndex]+np.dot(table,totalmatrix)[teamIndex]}
@app.get("/team/{teamKey}",
         description='Get a team object featuring each event that the team played, featuring EPA, Contribution("my stat") and Component OPRs. Use team key "frc+teamNumber"',
         response_description="Returns said team object as a json. Reference each event as a key to get data for that event",)
async def getTeam(teamKey:str):
    #mpu.io.write("hello.json",{"Hello":"World"})
    return await teams.createTeam(teamKey)

@app.get("/team/{teamKey}/{event}",
         description='Get a team object featuring EPA, Contribution("my stat") and Component OPRs. Use team key "frc+teamNumber". Use event key found on TBA',
         response_description="Returns said team object as a json.")
async def getTeamAtEvent(teamKey:str,event:str):
    #mpu.io.write("hello.json",{"Hello":"World"})
    return await teams.createTeamSingleEvent(teamKey,event)


@app.get("/event/{event}",
         description='Get an event object with all sorts of fun tables',
         response_description="Returns said event object as a json. Values are sorted matching the index to the index of teams provided by the team list grabbed from TBA")
async def getEvent(event:str):
    with open('events2023.json', 'r') as openfile:
                json_object = json.load(openfile)
    eventData = json_object[event]
    eventData.update({"eventKey":event})
    return eventData
    