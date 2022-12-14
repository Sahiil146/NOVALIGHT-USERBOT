# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

import asyncio
import os
import time
from random import choice

import requests
from telethon import Button, events
from telethon.tl import functions, types

from LightUB._misc._assistant import asst_cmd, callback, in_pattern
from LightUB._misc._decorators import light_cmd
from LightUB._misc._wrappers import eod, eor
from LightUB.dB import DEVLIST, LIGHT_IMAGES
from LightUB.fns.helper import *
from LightUB.fns.info import *
from LightUB.fns.misc import *
from LightUB.fns.tools import *
from LightUB.version import __version__
from strings import get_help, get_string
from LightUB import *


OWNER_NAME = light_bot.full_name
OWNER_ID = light_bot.uid
LOG_CHANNEL = udB.get_key("LOG_CHANNEL")

quotly = Quotly()
con = TgConverter
Redis = udB.get_key
ultroid = ultroid_bot = light = Light = light_bot
ultroid_cmd = light_cmd


def inline_pic():
    INLINE_PIC = udB.get_key("INLINE_PIC")
    if INLINE_PIC is None:
        INLINE_PIC = choice(LIGHT_IMAGES)
    elif INLINE_PIC == False:
        INLINE_PIC = None
    return INLINE_PIC


def deEmojify(text):
    from emoji import replace_emoji

    text = str(text).strip()
    return replace_emoji(args, replace="")


Telegraph = telegraph_client()

List = []
Dict = {}
InlinePlugin = {}
N = 0
cmd = light_cmd
STUFF = {}

# Chats, which needs to be ignore for some cases
# Considerably, there can be many
# Feel Free to Add Any other...

NOSPAM_CHAT = [
    -1001232996686,  # Light Chat
    -1001387666944,  # PyrogramChat
    -1001109500936,  # TelethonChat
    -1001050982793,  # Python
    -1001256902287,  # DurovsChat
    -1001473548283,  # SharingUserbot
]

KANGING_STR = [
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "Hehe me stel ur stiker...",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pack looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal-Your-Sticker is stealing this sticker... ",
]

ATRA_COL = [
    "DarkCyan",
    "DeepSkyBlue",
    "DarkTurquoise",
    "Cyan",
    "LightSkyBlue",
    "Turquoise",
    "MediumVioletRed",
    "Aquamarine",
    "Lightcyan",
    "Azure",
    "Moccasin",
    "PowderBlue",
]
