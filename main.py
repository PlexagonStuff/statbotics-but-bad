from fastapi import FastAPI
import numpy as np
import requests as requests
import json as json

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from APIRequests import statbotics,tba,firstevents
from ChargedUpScripts import events2023,teams2023

import os
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import getAllEvents
import getAllMatches




tags_metadata = [{"name": "teams"},{"name": "events"}]





app = FastAPI(title="Statbotics but Bad API",description="The REST API for Statbotics but Bad, please HTTP GET Request responsibly",version="2.33.7",openapi_tags=tags_metadata)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
    #return await firstevents.getTeamIconPrimaryColor("frc2337",2023)
    # teamList = await tba.getEventTeams("2023midet")
    # teamIndex = teamList.index("frc2337")
    # table = await events2023.createTeamFrequencyTable("2023midet")
    # totalmatrix = await events2023.createTotalMatchPiecesMatrix("2023midet")
    # automatrix = await events2023.createAutoMatchPiecesMatrix("2023midet")
    # return {"totalpieces":np.dot(table,totalmatrix)[teamIndex],
    #         "autopieces":np.dot(table,automatrix)[teamIndex],
    #         "total+auto pieces":np.dot(table,automatrix)[teamIndex]+np.dot(table,totalmatrix)[teamIndex]}
    # array = []
    # for x in range(20):
    #     teams = await tba.getAllTeams(x)
    #     for team in teams:
    #         teamNumber = team[3:]
    #         nickname = await tba.getTeamInformation(team,"nickname")
    #         array.append(teamNumber + "-" + nickname)
    #         print(teamNumber + "-" + nickname)
    # return array
    return await getTeamOverallRecord("frc118",2023)


@app.get("/team/{teamKey}/year/{year}/record",
        description='Get a teams record for the year as wins/losses/ties',
         response_description="Returns said record as a json object",
         tags=["teams"])
async def getTeamOverallRecord(teamKey:str,year:int):
    #mpu.io.write("hello.json",{"Hello":"World"})
    if year == 2023:
        return await teams2023.getOverallMatchRecord(teamKey)
@app.get("/team/{teamKey}/year/{year}/awards",
        description='Get a teams award list in terms of overall awards, as well as number of blue banners (wins + impact)',
         response_description="Returns said award list as json",
         tags=["teams"])
async def getTeamAwards(teamKey:str,year:int):
    if year == 2023:
        return await teams2023.getTeamAwards(teamKey)


@app.get("/team/{teamKey}/year/{year}",
         description='Get a team object featuring each event that the team played, featuring EPA, Contribution("my stat") and Component OPRs. Use team key "frc+teamNumber"',
         response_description="Returns said team object as a json. Reference each event as a key to get data for that event",
         tags=["teams"])
async def getTeam(teamKey:str,year:int):
    #mpu.io.write("hello.json",{"Hello":"World"})
    if year == 2023:
        return await teams2023.createTeam(teamKey)

@app.get("/team/{teamKey}/year/{year}/icon/color",
         description='Get a hexcode representing the primary color of a team\'s avatar. Use team key "frc+teamNumber". This ignores all black-adjacant colors as many avatars use black as a background, so some dark logos might not be properly represented. If a color cannot be identified (too dark), the default color is white #ffffff',
         response_description="Returns a hexcode (string)",
         tags=["teams"])
async def getTeamIconPrimaryColor(teamKey:str,year:int):
    color = await firstevents.getTeamIconPrimaryColor(teamKey,year)
    if os.path.exists("icon.png"):
         os.remove("icon.png")
    return {"color":color}

@app.get("/team/{teamKey}/year/{year}/{event}",
         description='Get a team object featuring EPA, Contribution("my stat") and Component OPRs. Use team key "frc+teamNumber". Use event key found on TBA',
         response_description="Returns said team object as a json.",
         tags=["teams"])
async def getTeamAtEvent(teamKey:str,event:str,year:int):
    #mpu.io.write("hello.json",{"Hello":"World"})
    if year == 2023:
        return await teams2023.createTeamSingleEvent(teamKey,event)




@app.get("/year/{year}/event/{event}",
         description='Get an event object with all sorts of fun tables',
         response_description="Returns said event object as a json. Values are sorted matching the index to the index of teams provided by the team list grabbed from TBA",
         tags=["events"])
async def getEvent(event:str,year:int):
    if year == 2023:
        return await events2023.createEvent(event)
    