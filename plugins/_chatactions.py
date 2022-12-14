# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.utils import get_display_name

from LightUB.dB import stickers
from LightUB.dB.forcesub_db import get_forcesetting
from LightUB.dB.gban_mute_db import is_gbanned
from LightUB.dB.greetings_db import get_goodbye, get_welcome, must_thank
from LightUB.dB.nsfw_db import is_profan
from LightUB.fns.helper import inline_mention
from LightUB.fns.tools import async_searcher, create_tl_btn, get_chatbot_reply

try:
    from ProfanityDetector import detector
except ImportError:
    detector = None

from . import LOG_CHANNEL, LOGS, asst, get_string, types, udB, light_bot
from ._inline import something


@light_bot.on(events.ChatAction())
async def Function(event):
    try:
        await DummyHandler(event)
    except Exception as er:
        LOGS.exception(er)


async def DummyHandler(ult):
    # clean chat actions
    key = udB.get_key("CLEANCHAT") or []
    if ult.chat_id in key:
        try:
            await ult.delete()
        except BaseException:
            pass

    # thank members
    if must_thank(ult.chat_id):
        chat_count = (await ult.client.get_participants(ult.chat_id, limit=0)).total
        if chat_count % 100 == 0:
            stik_id = chat_count / 100 - 1
            sticker = stickers[stik_id]
            await ult.respond(file=sticker)

    # force subscribe
    if (
        udB.get_key("FORCESUB")
        and ((ult.user_joined or ult.user_added))
        and get_forcesetting(ult.chat_id)
    ):
        user = await ult.get_user()
        if not user.bot:
            joinchat = get_forcesetting(ult.chat_id)
            try:
                await light_bot(GetParticipantRequest(int(joinchat), user.id))
            except UserNotParticipantError:
                await light_bot.edit_permissions(
                    ult.chat_id, user.id, send_messages=False
                )
                res = await light_bot.inline_query(
                    asst.me.username, f"fsub {user.id}_{joinchat}"
                )
                await res[0].click(ult.chat_id, reply_to=ult.action_message.id)

    if ult.user_joined or ult.added_by:
        user = await ult.get_user()
        chat = await ult.get_chat()

        # gban check
        reason = is_gbanned(user.id)
        if reason and chat.admin_rights:
            try:
                await ult.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                gban_watch = get_string("can_1").format(inline_mention(user), reason)
                await ult.reply(gban_watch)
            except Exception as er:
                LOGS.exception(er)

        # greetings
        elif get_welcome(ult.chat_id):
            user = await ult.get_user()
            chat = await ult.get_chat()
            title = chat.title or "this chat"
            count = (
                chat.participants_count
                or (await ult.client.get_participants(chat, limit=0)).total
            )
            mention = inline_mention(user)
            name = user.first_name
            fullname = get_display_name(user)
            uu = user.username
            username = f"@{uu}" if uu else mention
            wel = get_welcome(ult.chat_id)
            msgg = wel["welcome"]
            med = wel["media"] or None
            userid = user.id
            msg = None
            if msgg:
                msg = msgg.format(
                    mention=mention,
                    group=title,
                    count=count,
                    name=name,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                )
            if wel.get("button"):
                btn = create_tl_btn(wel["button"])
                await something(ult, msg, med, btn)
            elif msg:
                send = await ult.reply(
                    msg,
                    file=med,
                )
                await asyncio.sleep(150)
                await send.delete()
            else:
                await ult.reply(file=med)

    elif (ult.user_left or ult.user_kicked) and get_goodbye(ult.chat_id):
        user = await ult.get_user()
        chat = await ult.get_chat()
        title = chat.title or "this chat"
        count = (
            chat.participants_count
            or (await ult.client.get_participants(chat, limit=0)).total
        )
        mention = inline_mention(user)
        name = user.first_name
        fullname = get_display_name(user)
        uu = user.username
        username = f"@{uu}" if uu else mention
        wel = get_goodbye(ult.chat_id)
        msgg = wel["goodbye"]
        med = wel["media"]
        userid = user.id
        msg = None
        if msgg:
            msg = msgg.format(
                mention=mention,
                group=title,
                count=count,
                name=name,
                fullname=fullname,
                username=username,
                userid=userid,
            )
        if wel.get("button"):
            btn = create_tl_btn(wel["button"])
            await something(ult, msg, med, btn)
        elif msg:
            send = await ult.reply(
                msg,
                file=med,
            )
            await asyncio.sleep(150)
            await send.delete()
        else:
            await ult.reply(file=med)


@light_bot.on(
    events.NewMessage(
        incoming=True,
        func=lambda e: e.text,
    )
)
async def chatBot_replies(e):
    sender = await e.get_sender()
    if not isinstance(sender, types.User):
        return
    key = udB.get_key("CHATBOT_USERS") or {}
    if key.get(e.chat_id) and sender.id in key[e.chat_id]:
        msg = await get_chatbot_reply(e.message.message)
        if msg:
            sleep = udB.get_key("CHATBOT_SLEEP") or 2
            await asyncio.sleep(sleep)
            await e.reply(msg)
    if detector and is_profan(e.chat_id):
        x, y = detector(e.text)
        if y:
            await e.delete()
