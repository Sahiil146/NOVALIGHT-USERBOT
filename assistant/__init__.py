# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

from telethon import Button, custom

from plugins import ATRA_COL, InlinePlugin
from LightUB import *
from LightUB import _ult_cache
from LightUB._misc import owner_and_sudos
from LightUB._misc._assistant import asst_cmd, callback, in_pattern
from LightUB.fns.helper import *
from LightUB.fns.tools import get_stored_file
from strings import get_languages, get_string

OWNER_NAME = light_bot.full_name
OWNER_ID = light_bot.uid

AST_PLUGINS = {}


async def setit(event, name, value):
    try:
        udB.set_key(name, value)
    except BaseException:
        return await event.edit("`Something Went Wrong`")


def get_back_button(name):
    return [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
