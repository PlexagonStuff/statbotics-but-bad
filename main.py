from fastapi import FastAPI
import numpy as np
import requests as requests
import json as json

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from APIRequests import statbotics,tba,firstevents
from ChargedUpScripts import events2023,teams2023

import os


from dotenv import load_dotenv
import getAllEvents
import getAllMatches
app = FastAPI(title="Statbotics but Bad API",description="The REST API for Statbotics but Bad, please HTTP GET Request responsibly",version="2.33.7",)

# with open("sample.json", "w") as outfile:
#        json.dump({"message":"hello world"}, outfile)
#    with open('sample.json', 'r') as openfile:
#        json_object = json.load(openfile)
load_dotenv()





@app.get("/")
async def root():
    return "Hello!"
    #mpu.io.write("hello.json",{"Hello":"World"})
    #return await getAllEvents.getAllEvents()
@app.get("/test")
async def test():
      return await firstevents.getTeamIconPrimaryColor("frc2337",2023)
    # teamList = await tba.getEventTeams("2023midet")
    # teamIndex = teamList.index("frc2337")
    # table = await events2023.createTeamFrequencyTable("2023midet")
    # totalmatrix = await events2023.createTotalMatchPiecesMatrix("2023midet")
    # automatrix = await events2023.createAutoMatchPiecesMatrix("2023midet")
    # return {"totalpieces":np.dot(table,totalmatrix)[teamIndex],
    #         "autopieces":np.dot(table,automatrix)[teamIndex],
    #         "total+auto pieces":np.dot(table,automatrix)[teamIndex]+np.dot(table,totalmatrix)[teamIndex]}
@app.get("/team/{teamKey}",
         description='Get a team object featuring each event that the team played, featuring EPA, Contribution("my stat") and Component OPRs. Use team key "frc+teamNumber"',
         response_description="Returns said team object as a json. Reference each event as a key to get data for that event",)
async def getTeam(teamKey:str):
    #mpu.io.write("hello.json",{"Hello":"World"})
    return await teams2023.createTeam(teamKey)

@app.get("/team/{teamKey}/icon/color",
         description='Get a hexcode representing the primary color of a team\'s avatar. Use team key "frc+teamNumber". This ignores all black-adjacant colors as many avatars use black as a background, so some dark logos might not be properly represented. If a color cannot be identified (too dark), the default color is white #ffffff',
         response_description="Returns a hexcode (string)",)
async def getTeamIconPrimaryColor(teamKey:str):
    color = await firstevents.getTeamIconPrimaryColor(teamKey,2023)
    if os.path.exists("icon.png"):
         os.remove("icon.png")
    return color

@app.get("/team/{teamKey}/{event}",
         description='Get a team object featuring EPA, Contribution("my stat") and Component OPRs. Use team key "frc+teamNumber". Use event key found on TBA',
         response_description="Returns said team object as a json.")
async def getTeamAtEvent(teamKey:str,event:str):
    #mpu.io.write("hello.json",{"Hello":"World"})
    return await teams2023.createTeamSingleEvent(teamKey,event)


@app.get("/event/{event}",
         description='Get an event object with all sorts of fun tables',
         response_description="Returns said event object as a json. Values are sorted matching the index to the index of teams provided by the team list grabbed from TBA")
async def getEvent(event:str):
    return await events2023.createEvent(event)
    