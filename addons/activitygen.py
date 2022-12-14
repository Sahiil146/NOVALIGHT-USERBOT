# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE



"""
✘ Commands Available -

• `{i}bored`
    Get some activity to do when you get bored
"""

from . import async_searcher, light_cmd


@light_cmd(pattern="bored$")
async def bored_cmd(event):
    msg = await event.eor("`Generating an Activity for You!`")
    content = await async_searcher(
        "https://www.boredapi.com/api/activity", re_json=True
    )
    m = f"**Activity:** `{content['activity']}`"
    if content.get("link"):
        m += f"**Read More:** {content['link']}"
    if content.get("participants"):
        m += f"\n**Participants Required:** `{content['participants']}`"
    if content.get("price"):
        m += f"\n**Price:** `{content['price']}`"
    await msg.edit(m)
