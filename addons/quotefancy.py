# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE


"""
✘ Commands Available

• `{i}qfancy`
    Gets random quotes from QuoteFancy.com.
"""

from telethon.errors import ChatSendMediaForbiddenError

from quotefancy import get_quote

from . import *


@light_cmd(pattern="qfancy$")
async def quotefancy(e):
    mes = await e.eor(get_string("com_1"))
    img = get_quote("img", download=True)
    try:
        await e.client.send_file(e.chat_id, img)
        os.remove(img)
        await mes.delete()
    except ChatSendMediaForbiddenError:
        quote = get_quote("text")
        await eor(mes, f"`{quote}`")
    except Exception as err:
        await eor(mes, f"**ERROR** - {err}")
