# Thanks To The Creator Of Autopic This Script Was Made from Snippets From
# That Script

# Usage avengersdp Im Not Responsible For Any Ban caused By This

import asyncio
import os
import random
import re
import urllib

import requests
from telethon.tl import functions

from userbot.utils import admin_cmd

COLLECTION_STRING = [
    "avengers-logo-wallpaper",
    "avengers-hd-wallpapers-1080p",
    "avengers-iphone-wallpaper",
    "iron-man-wallpaper-1920x1080",
    "iron-man-wallpapers",
]

IS_ACTIVATED = False


async def animepp():
    os.system("rm -rf donot.jpg")
    rnd = random.randint(0, len(COLLECTION_STRING) - 1)
    pack = COLLECTION_STRING[rnd]
    pc = requests.get("http://getwallpapers.com/collection/" + pack).text
    f = re.compile(r"/\w+/full.+.jpg")
    f = f.findall(pc)
    fy = "http://getwallpapers.com" + random.choice(f)
    print(fy)
    if not os.path.exists("f.ttf"):
        urllib.request.urlretrieve(
            "https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf",
            "f.ttf",
        )
    urllib.request.urlretrieve(fy, "donottouch.jpg")


@borg.on(admin_cmd(pattern="avdp ?(.*)"))
async def main(event):
    global IS_ACTIVATED
    await event.edit("**Starting Avengers Profile Pic...\n\nDone !!! Check Your DP **")
    IS_ACTIVATED = True
    while IS_ACTIVATED:
        await animepp()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(1000)  # Edit this to your required needs


@borg.on(admin_cmd(pattern="offavdp ?(.*)"))
async def turnoff(event):
    global IS_ACTIVATED
    if IS_ACTIVATED:
        await event.edit("**Turning off Avengers DP.**")
        IS_ACTIVATED = False
        await event.delete()
    else:
        await event.edit("Avengers dp is not activated.")
        asyncio.sleep(3)
        event.delete()
