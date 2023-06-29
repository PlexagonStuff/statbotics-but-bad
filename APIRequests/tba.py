import requests
from requests_cache import CachedSession
import json
from datetime import timedelta

import os
from dotenv import load_dotenv
load_dotenv()

headers = {"X-TBA-Auth-Key":os.getenv("TBA")}

session = CachedSession(stale_while_revalidate=True,backend="memory")

async def getTeamInformation(teamKey:str,paramName:str):
     r = session.get("https://www.thebluealliance.com/api/v3/team/"+teamKey,headers=headers,expire_after=timedelta(days=12))
     #r = requests.get("https://www.thebluealliance.com/api/v3/team/"+teamKey,headers=headers)
     return r.json()[paramName]

async def getTeamEvents(teamKey:str,year:int):
     r = session.get("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/events/"+str(year)+"/keys",headers=headers,expire_after=timedelta(days=12))
     #r = requests.get("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/events/"+str(year)+"/keys",headers=headers)
     return r.json()

async def getTeamMatches(teamKey:str,event:str):
     r = session.get("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/"+event+"/matches",headers=headers,expire_after=timedelta(minutes=5))
     #r = requests.get("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/"+event+"/matches",headers=headers)
     return r.json()


async def getTeamMatchesSimple(teamKey:str,event:str):
     r = session.get("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/"+event+"/matches/simple",headers=headers,expire_after=timedelta(minutes=5))
     #r = requests.get("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/"+event+"/matches",headers=headers)
     return r.json()


#Event Information

async def getEventMatches(event:str):
     r = session.get("https://www.thebluealliance.com/api/v3/event/"+event+"/matches",headers=headers,expire_after=timedelta(minutes=5))
     #r = requests.get("https://www.thebluealliance.com/api/v3/event/"+event+"/matches",headers=headers)
     return r.json()

async def getEventTeams(event:str):
     r = session.get("https://www.thebluealliance.com/api/v3/event/"+event+"/teams/keys",headers=headers,expire_after=timedelta(days=1))
     #r = requests.get("https://www.thebluealliance.com/api/v3/event/"+event+"/teams/keys",headers=headers)
     return r.json()

async def getEventOPRs(event:str):
     r = session.get("https://www.thebluealliance.com/api/v3/event/"+event+"/oprs",headers=headers,expire_after=timedelta(days=1))
     #r = requests.get("https://www.thebluealliance.com/api/v3/event/"+event+"/teams/keys",headers=headers)
     return r.json()

async def getEventsInYear(year:int):
     r = session.get("https://www.thebluealliance.com/api/v3/events/"+str(year)+"/keys",headers=headers,expire_after=timedelta(days=5))
     #r = requests.get("https://www.thebluealliance.com/api/v3/events/"+str(year)+"/keys",headers=headers)
     return r.json()

async def getEventType(event:str):
     r = session.get("https://www.thebluealliance.com/api/v3/event/"+event,headers=headers,expire_after=timedelta(days=5))
     #r = requests.get("https://www.thebluealliance.com/api/v3/events/"+str(year)+"/keys",headers=headers)
     return r.json()["event_type_string"]

async def getAllTeams(pageNum:int):
     r = requests.get("https://www.thebluealliance.com/api/v3/teams/"+str(pageNum)+"/keys",headers=headers)
     return r.json()