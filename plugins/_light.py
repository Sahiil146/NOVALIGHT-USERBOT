# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

from telethon.errors import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
)

from . import LOG_CHANNEL, LOGS, Button, asst, eor, get_string, light_cmd

REPOMSG = """
• **LIGHT USERBOT** •\n
• Repo - [Click Here](https://github.com/CodeWithTyagi/light)
• Addons - [Click Here](https://github.com/CodeWithTyagi/lightAddons)
• Support - @CodeWithTyagi
"""

RP_BUTTONS = [
    [
        Button.url(get_string("bot_3"), "https://github.com/CodeWithTyagi/light"),
        Button.url("Addons", "https://github.com/CodeWithTyagi/lightAddons"),
    ],
    [Button.url("Support Group", "t.me/CodeWithTyagi")],
]

ULTSTRING = """🎇 **Thanks for Deploying light Userbot!**

• Here, are the Some Basic stuff from, where you can Know, about its Usage."""


@light_cmd(
    pattern="repo$",
    manager=True,
)
async def repify(e):
    try:
        q = await e.client.inline_query(asst.me.username, "")
        await q[0].click(e.chat_id)
        return await e.delete()
    except (
        ChatSendInlineForbiddenError,
        ChatSendMediaForbiddenError,
        BotMethodInvalidError,
    ):
        pass
    except Exception as er:
        LOGS.info(f"Error while repo command : {str(er)}")
    await e.eor(REPOMSG)


@light_cmd(pattern="light$")
async def uselight(rs):
    button = Button.inline("Start >>", "initft_2")
    msg = await asst.send_message(
        LOG_CHANNEL,
        ULTSTRING,
        file="https://graph.org/file/d0e6c23a71edc59e7f778.jpg",
        buttons=button,
    )
    if not (rs.chat_id == LOG_CHANNEL and rs.client._bot):
        await eor(rs, f"**[Click Here]({msg.message_link})**")
