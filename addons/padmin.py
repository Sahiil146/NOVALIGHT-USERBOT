"""
✘ Commands Available -

• `{i}padmin`
    Prank Promote Anyone.
"""

from asyncio import sleep

from . import light_cmd


@light_cmd(pattern="padmin$")
async def padmin(e):
    msg = await e.eor("`Promoting this User...`")
    data = [
        "Promoting User As Admin...",
        "Enabling All Permissions To User...",
        "(1) Send Messages: ☑️",
        "(1) Send Messages: ✅",
        "(2) Send Media: ☑️",
        "(2) Send Media: ✅",
        "(3) Send Stickers & GIFs: ☑️",
        "(3) Send Stickers & GIFs: ✅",
        "(4) Send Polls: ☑️",
        "(4) Send Polls: ✅",
        "(5) Embed Links: ☑️",
        "(5) Embed Links: ✅",
        "(6) Add Users: ☑️",
        "(6) Add Users: ✅",
        "(7) Pin Messages: ☑️",
        "(7) Pin Messages: ✅",
        "(8) Change Chat Info: ☑️",
        "(8) Change Chat Info: ✅",
        "Promoted User Successfully",
        "Congratulations, you're an Admin now !!",
    ]
    for i in data:
        await sleep(1.2)
        await msg.edit(f"**{i}**")
