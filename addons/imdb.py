# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

"""
Search movie details from IMDB

✘ Commands Available
• `{i}imdb <keyword>`
"""

from . import *


@light_cmd(pattern="imdb ?(.*)")
async def imdbot(e):
    m = await e.eor("`...`")
    movie_name = e.pattern_match.group(1)
    if not movie_name:
        return await eor(m, "`Provide a movie name too`")
    try:
        mk = await e.client.inline_query("imdbot", movie_name)
        await mk[0].click(e.chat_id)
        await m.delete()
    except IndexError:
        return await eor(m, "No Results Found...")
    except Exception as er:
        return await eor(m, str(er))
