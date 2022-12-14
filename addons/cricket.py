# Ported from Old Friday Bot.
# Credits to their developers.

"""
✘ Commands Available -

• `{i}cricket`
    Get Live Cricket Score from Cricinfo.com
"""


from urllib.request import urlopen

from bs4 import BeautifulSoup

from . import light_cmd


@light_cmd(pattern="cricket$")
async def cricket_score(event):
    my = await event.eor("`getting scroes..`")
    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    page = urlopen(score_page)
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")
    Sed = ""
    for match in result:
        Sed += match.get_text() + "\n\n"
    await my.edit(
        f"<b><u>Match information gathered successful</b></u>\n\n\n<code>{Sed}</code>",
        parse_mode="HTML",
    )
