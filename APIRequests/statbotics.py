import requests
from requests_cache import CachedSession
from datetime import timedelta

session = CachedSession(stale_while_revalidate=True)


async def getTeamEPA(teamKey:str,event:str):
    teamNumber = teamKey[3:]
    r = session.get("https://api.statbotics.io/v2/team_event/"+teamNumber+"/"+event,expire_after=timedelta(hours=4))
    #r = requests.get("https://api.statbotics.io/v2/team_event/"+teamNumber+"/"+event)
    return r.json()["epa_end"]