# This plugin uses @Stickerizerbot to send stickers

"""
✘ Commands Available -

• `{i}sz <some_text>`
    Get a Random sticker of ur text.
"""

from random import choice, randrange
from emoji import replace_emoji

from . import light_cmd, deEmojify


dct = {"#": 66, "&": 23}


@ultroid_cmd(pattern="sz ?(.*)")
async def stickerizer(e):
    msg = await e.eor("...")
    args = e.pattern_match.group(1)
    reply = await e.get_reply_message()
    if not args:
        if reply and reply.text:
            args = reply.text
        else:
            await msg.eor("`give sum text.. ` 🤡", time=8)
            return
    style = choice(list(dct.keys()))
    args = style + str(randrange(dct[style])) + args
    try:
        stick = await e.client.inline_query("stickerizerbot", deEmojify(args))
        await e.eor("@stickerizerbot", file=stick[0].document)
        await msg.try_delete()
    except Exception as exc:
        await msg.edit(f"`{exc}`")
