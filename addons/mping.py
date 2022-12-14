"""
✘ Commands Available -

• `{i}mping`
    Media (Image) Ping.
"""

from time import time
from random import choice

from . import LIGHT_IMAGES, light_cmd, time_formatter, get_string, start_time


@light_cmd(pattern="mping$")
async def m_ping(e):
    start = time()
    x = await e.respond("Pong !", file=choice(LIGHT_IMAGES))
    end = round((time() - start) * 1000)
    uptime = time_formatter((start - start_time) * 1000)
    await x.edit(
        "\n█▀█ █▀█ █▄░▄█ █▀▀ █\n█▀▀ █▄█ █░▀░█ █▄█ ▄\n\n"
        + get_string("ping").format(end, uptime)
    )
