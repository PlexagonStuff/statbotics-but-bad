import requests
import json
with open('authentication.json', 'r') as openfile:
     json_object = json.load(openfile)
headers = {"X-TBA-Auth-Key":json_object["tbakey"]}


async def getTeamInformation(teamKey:str,paramName:str):
     r = requests.get("https://www.thebluealliance.com/api/v3/team/"+teamKey,headers=headers)
     return r.json()[paramName]

async def getTeamEvents(teamKey:str,year:int):
     r = requests.get("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/events/"+str(year)+"/keys",headers=headers)
     return r.json()

async def getTeamMatches(teamKey:str,event:str):
     r = requests.get("https://www.thebluealliance.com/api/v3/team/"+teamKey+"/event/"+event+"/matches",headers=headers)
     return r.json()

#Event Information

async def getEventMatches(event:str):
     r = requests.get("https://www.thebluealliance.com/api/v3/event/"+event+"/matches",headers=headers)
     return r.json()

async def getEventTeams(event:str):
     r = requests.get("https://www.thebluealliance.com/api/v3/event/"+event+"/teams/keys",headers=headers)
     return r.json()

async def getEventsInYear(year:int):
     r = requests.get("https://www.thebluealliance.com/api/v3/events/"+str(year)+"/keys",headers=headers)
     return r.json()

async def getEventType(event:str):
     r = requests.get("https://www.thebluealliance.com/api/v3/event/"+event,headers=headers)
     return r.json()["event_type_string"]
