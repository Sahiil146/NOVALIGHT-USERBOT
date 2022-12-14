# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

# Ported Plugin

"""
✘ Commands Available -

• `{i}autoname`
   `Starts AUTONAME`.

• `{i}stopname`
   `Stops AUTONAME.`

• `{i}autobio`
   `Starts AUTOBIO.`

• `{i}stopbio`
   `Stops AUTOBIO.`
"""

import random

from telethon.tl.functions.account import UpdateProfileRequest

from . import *


@light_cmd(pattern="(auto|stop)name$")
async def autoname_(event):
    match = event.pattern_match.group(1)
    if match == "stop":
        udB.del_key("AUTONAME")
        await event.eor("`AUTONAME has been Stopped !`")
        return
    udB.set_key("AUTONAME", "True")
    await eod(event, "`Started AUTONAME`")
    while True:
        getn = udB.get_key("AUTONAME")
        if not getn:
            return
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"🕒{HM} ⚡{OWNER_NAME}⚡ {DM} 🗓️"
        await event.client(UpdateProfileRequest(first_name=name))
        await asyncio.sleep(1111)


@light_cmd(pattern="(auto|stop)bio$")
async def autoname_(event):
    match = event.pattern_match.group(1)
    if match == "stop":
        udB.del_key("AUTOBIO")
        await event.eor("`AUTOBIO has been Stopped !`")
        return
    udB.set_key("AUTOBIO", "True")
    await eod(event, "`Started AUTOBIO`")
    BIOS = [
        "Busy Today !",
        "light USER",
        "Enjoying Life!",
        "Unique as Always!" "Sprinkling a bit of magic",
        "Intelligent !",
    ]
    while True:
        getn = udB.get_key("AUTOBIO")
        if not getn:
            return
        BIOMSG = random.choice(BIOS)
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"📅{DM} | {BIOMSG} | ⌚️{HM}"
        await event.client(
            UpdateProfileRequest(
                about=name,
            )
        )
        await asyncio.sleep(1111)
