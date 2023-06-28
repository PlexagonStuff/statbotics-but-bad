import requests
from requests_cache import CachedSession
from datetime import timedelta
import os

from PIL import Image
from io import BytesIO
import base64

from colorthief import ColorThief
from colormath.color_objects import sRGBColor,LabColor
from FixedColorMatch import color_match
from colormath.color_conversions import convert_color
from dotenv import load_dotenv
load_dotenv()

session = CachedSession(stale_while_revalidate=True,backend="memory")

headers={"Authorization":os.getenv("FIRSTAPI")}

async def getTeamAvatarEncoded(teamKey:str,year:int):
    teamNumber = teamKey[3:]
    r = session.get("https://frc-api.firstinspires.org/v3.0/"+str(year)+"/avatars?teamNumber="+teamNumber,expire_after=timedelta(days=12),headers=headers)
    #r = requests.get("https://api.statbotics.io/v2/team_event/"+teamNumber+"/"+event)
    return r.json()["teams"][0]["encodedAvatar"]


async def getTeamIconPrimaryColor(teamKey,year):

    #http://zschuessler.github.io/DeltaE/learn/
    encodedData = await getTeamAvatarEncoded(teamKey,year)
    #print(encodedData)
    image_data = base64.b64decode(encodedData)

    # Create a PIL Image object from the image data
    image = Image.open(BytesIO(image_data))

    # Save the image to the filesystem
    image.save("icon.png")
    color_thief = ColorThief("icon.png")
    # get the dominant color,
    try:
        dominant_color = color_thief.get_palette(color_count=2, quality=1)
    except:
        dominant_color = [[255,255,255]]
    real_color = [255,255,255]
    #print(dominant_color)
    for color in dominant_color:
         print(color)
         new_color = sRGBColor(color[0],color[1],color[2],True)
         new_color_lab = convert_color(new_color,LabColor)
         compare_color = sRGBColor(0,0,0,False)
         compare_color_lab = convert_color(compare_color,LabColor)
         delta_e = color_match.delta_e_cie1976(new_color_lab,compare_color_lab)
         print(delta_e)
         if (delta_e > 49):
            real_color = color
            break
    hexcode = '#%02x%02x%02x' % (real_color[0], real_color[1], real_color[2])
    return hexcode
