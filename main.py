from fastapi import FastAPI
import numpy as np
import requests as requests
import json as json
from APIRequests import statbotics,tba
from ChargedUpScripts import events,teams
import getAllEvents
app = FastAPI(title="Statbotics but Bad API",description="The REST API for Statbotics but Bad, please HTTP GET Request responsibly",version="2.33.7",)

# with open("sample.json", "w") as outfile:
#        json.dump({"message":"hello world"}, outfile)
#    with open('sample.json', 'r') as openfile:
#        json_object = json.load(openfile)






@app.get("/")
async def root():
    #mpu.io.write("hello.json",{"Hello":"World"})
    return "hello!"


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
async def getTeamAtEvent(event:str):
    invMatrix = await events.createTeamFrequencyTable(event)
    oprMatrix = await events.createScoreMatrix(event)
    autoHighMatrix = await events.createAutoHighMatrix(event)
    autoMidMatrix = await events.createAutoMidMatrix(event)
    autoLowMatrix = await events.createAutoLowMatrix(event)
    teleHighMatrix = await events.createTeleHighMatrix(event)
    teleMidMatrix = await events.createTeleMidMatrix(event)
    teleLowMatrix = await events.createTeleLowMatrix(event)
    opr = np.dot(invMatrix,oprMatrix).tolist()
    autoHigh = np.dot(invMatrix,autoHighMatrix).tolist()
    autoLow = np.dot(invMatrix,autoLowMatrix).tolist()
    autoMid = np.dot(invMatrix,autoMidMatrix).tolist()
    teleHigh = np.dot(invMatrix,teleHighMatrix).tolist()
    teleMid = np.dot(invMatrix,teleMidMatrix).tolist()
    teleLow = np.dot(invMatrix,teleLowMatrix).tolist()
    return {"eventKey":event,"oprtable":opr,"autohightable":autoHigh,"automidtable":autoMid,"autolowtable":autoLow,"telehightable":teleHigh,"telemidtable":teleMid,"telelowtable":teleLow}
    