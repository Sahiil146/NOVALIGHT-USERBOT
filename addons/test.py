# Ported From DarkCobra Originally By UNIBORG
#
# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

"""
✘ Commands Available -

• `{i}test`
    Test Your Server Speed.
"""

from datetime import datetime

import speedtest

from . import light_cmd


temxt = (
    "**Light Speedtest completed in {0} seconds.**\n\n"
    "**Download:**  `{1}` \n"
    "**Upload:**  `{2}` \n"
    "**Ping:**  `{3} ms` \n"
    "**Internet Provider:**  `{4}` \n"
    "**ISP Rating:**  `{5}` \n"
)


@light_cmd(pattern="test ?(.*)")
async def speemdtest(event):
    args = event.pattern_match.group(1)
    xx = await eor(event, "`Calculating your Server's Speed..`")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).seconds
    response = s.results.dict()

    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")

    if args and args == "text":
        await xx.edit(
            temxt.format(
                ms,
                convert_from_bytes(download_speed),
                convert_from_bytes(upload_speed),
                ping_time,
                i_s_p,
                i_s_p_rating,
            )
        )
    else:
        try:
            speedtest_image = s.results.share()
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption="**SpeedTest** completed in {} seconds".format(ms),
                force_document=False,
                reply_to=event.reply_to_msg_id,
                allow_cache=False,
            )
            await xx.delete()
        except Exception as exc:
            xx2 = temxt.format(
                ms,
                convert_from_bytes(download_speed),
                convert_from_bytes(upload_speed),
                ping_time,
                i_s_p,
                i_s_p_rating,
            )
            return await xx.edit(f"{xx2} \n**Exception:** `{exc}`")
