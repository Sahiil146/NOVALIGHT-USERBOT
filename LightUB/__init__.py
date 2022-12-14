# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

import os
import sys
import time

from .startup import *


class LightConfig:
    lang = "en"
    thumb = "resources/extras/light.jpg"


from .configs import Var
from .version import __version__
from .startup._database import LightDB
from .startup.BaseClient import LightClient
from .startup.connections import validate_session, vc_connection
from .startup.funcs import _version_changes, autobot, enable_inline, update_envs

if not os.path.exists("./plugins"):
    LOGS.error("'plugins' folder not found!\nMake sure that, you are on correct path.")
    exit()

start_time = time.time()
_ult_cache = {}
_ignore_eval = []

udB = LightDB()
update_envs()

if udB.ping():
    LOGS.info(f"Connected to {udB.name} Successfully !!")

BOT_MODE = udB.get_key("BOTMODE")
DUAL_MODE = udB.get_key("DUAL_MODE")

if BOT_MODE:
    if DUAL_MODE:
        udB.del_key("DUAL_MODE")
        DUAL_MODE = False
    light_bot = None

    if not udB.get_key("BOT_TOKEN"):
        LOGS.critical('"BOT_TOKEN" not Found! Please add it, in order to use "BOTMODE"')

        sys.exit()
else:
    light_bot = LightClient(
        validate_session(Var.SESSION, LOGS),
        udB=udB,
        app_version=__version__,
        device_model="Light",
    )
    light_bot.run_in_loop(autobot())

asst = LightClient(None, bot_token=udB.get_key("BOT_TOKEN"), udB=udB)

if BOT_MODE:
    light_bot = asst
    if udB.get_key("OWNER_ID"):
        try:
            light_bot.me = light_bot.run_in_loop(
                light_bot.get_entity(udB.get_key("OWNER_ID"))
            )
        except Exception as er:
            LOGS.exception(er)
elif not asst.me.bot_inline_placeholder:
    light_bot.run_in_loop(enable_inline(light_bot, asst.me.username))

vcClient = vc_connection(udB, light_bot)

_version_changes(udB)

HNDLR = udB.get_key("HNDLR") or "."
DUAL_HNDLR = udB.get_key("DUAL_HNDLR") or "/"
SUDO_HNDLR = udB.get_key("SUDO_HNDLR") or HNDLR
