# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

"""
✘ Commands Available -

• `{i}timepic`
    To Start auto - timepic.
    New Profile picture every 2 minute.

    To Stop use {i}timepic again
"""

from asyncio import sleep
from datetime import datetime
from os import path, remove
from shutil import copy2

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest


from . import light_cmd, light_bot, udB, LOGS


FIRST_ = True
scheduler = AsyncIOScheduler()


def _job_exists():
    for i in scheduler.get_jobs():
        if i.id == "time_pic":
            return 1

async def auto_time_pic():
    global FIRST_
    text2 = "Life is too short -\nto argue ,\nJust say 'fuck off'\nand move on !!"
    original = "resources/extras/timepic_template.jpg"
    photo = "timepic.jpg"
    copy2(original, photo)
    img = Image.open(photo)
    drawn_text = ImageDraw.Draw(img)
    font1 = ImageFont.truetype("resources/fonts/Ubuntu-font.ttf", 45)
    text1 = datetime.now().strftime(f"%H:%M - %d-%m-%y")
    drawn_text.text((165, 8), text1, font=font1, fill=(255, 255, 0))

    font2 = ImageFont.truetype("resources/fonts/Ubuntu-font.ttf", 32)
    drawn_text.text((385, 485), text2, font=font2, fill=(0, 0, 0))
    img.save(photo)
    try:
        if not FIRST_:
            old_dp = await light_bot.get_profile_photos("me", limit=1)
            await light_bot(DeletePhotosRequest(old_dp))
        await sleep(1)
        new_dp = await light_bot.upload_file(photo)
        await bot(UploadProfilePhotoRequest(new_dp))
        FIRST_ = False
    except Exception:
        LOGS.exception()
    finally:
        if path.exists(photo):
            remove(photo)


@light_cmd(pattern="timepic$", fullsudo=True)
async def _timepic(e):
    ofx = await e.eor("...")
    if udB.get_key("TIMEPIC"):
        udB.del_key("TIMEPIC")
        scheduler.pause_job("time_pic")
        await ofx.edit("`Stopped Time Autopic!`")
        return
    if _job_exists():
        scheduler.resume_job("time_pic")
    else:
        scheduler.add_job(auto_time_pic, trigger="interval", minutes=2, id="time_pic")
    udB.set_key("TIMEPIC", True)
    await ofx.edit("`Time Autopic Enabled!`")


if udB.get_key("TIMEPIC"):
    scheduler.add_job(auto_time_pic, trigger="interval", minutes=2, id="time_pic")

scheduler.start()
