# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

"""
Fetch Random anime quotes

Command : `{i}aniquote`
"""

from . import light_cmd, async_searcher


@light_cmd(pattern="aniquote")
async def _(ult):
    u = await ult.eor("...")
    try:
        resp = await async_searcher(
            "https://animechan.vercel.app/api/random", re_json=True
        )
        results = f"**{resp['quote']}**\n"
        results += f" — __{resp['character']} ({resp['anime']})__"
        return await u.edit(results)
    except Exception:
        await u.edit("`Something went wrong LOL ...`")
