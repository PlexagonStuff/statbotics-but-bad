import requests



async def getTeamEPA(teamKey:str,event:str):
    teamNumber = teamKey[3:]
    r = requests.get("https://api.statbotics.io/v2/team_event/"+teamNumber+"/"+event)
    return r.json()["epa_end"]