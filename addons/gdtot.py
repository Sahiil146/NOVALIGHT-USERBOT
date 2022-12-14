"""
✘ Commands Available -

• `{i}gdtot <gdtot link>`
    Get GDrive Link from GDToT.

    - To Use this plugin, add gdtot key in db -
    eg - `{i}setdb GDTOT_CRYPT ur_key`
"""

from re import findall
from base64 import b64decode
from requests import Session, get
from urllib.parse import urlparse, parse_qs

from . import LOGS, udB, light_cmd


def parse_info(res):
    title = findall(">(.*?)<\/h5>", res.text)[0]
    info = findall('<td\salign="right">(.*?)<\/td>', res.text)
    return {"title": title, "size": info[0], "date": info[1]}


def gdtot_scraper(url, crypt):
    client = Session()
    client.cookies.clear()
    client.cookies.update({"crypt": crypt})
    res = client.get(url, timeout=12)

    info = parse_info(res)
    chk_url = get("https://new.gdtot.nl/").url
    res = client.get(f"{chk_url}dld?id={url.rsplit('/', 1)[1]}")

    try:
        url = findall('URL=(.*?)"', res.text)[0]
    except:
        return False, "The requested URL could not be retrieved."

    params = parse_qs(urlparse(url).query)

    if not params.get("gd") or params["gd"][0] in ("false", "null"):
        LOGS.error(params)
        return False, "Could not find the drive URL."

    try:
        gd = params["gd"][0]
        return True, (b64decode(str(gd)).decode(), info)
    except Exception:
        LOGS.error(params)
        return False, "Invalid Response from Server."
    finally:
        client.cookies.pop("crypt")
        client.close()


# ===============================================================


@light_cmd(pattern="gdtot ?(.*)")
async def gdtot_parser(e):
    if not (key := udB.get_key("GDTOT_CRYPT")):
        return await e.eor("Add GDToT Crypt key in `GDTOT_CRYPT`")
    if not (url := e.pattern_match.group(1)):
        return await e.eor("`gib gdtot link..`", time=8)

    msg = await e.eor("`extracting drive link..`")
    buul, data = gdtot_scraper(url, key)
    if not buul:
        await msg.edit(f"**Error:** `{data}`")
        return

    dct = data[1]
    link = f"https://drive.google.com/open?id={data[0]}"
    txt = f" 🎥 **Title -**  `{dct['title']}` \n 🖇️ **Size -**  `{dct['size']}` \n 🔗 **Link -**  `{link}`"

    await msg.edit(f"**__Parsed GDrive Link from GDToT__** \n\n{txt}")
