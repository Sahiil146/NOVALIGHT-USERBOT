import sys
from os import environ
from typing import Any, Dict, List, Union
from glob import glob

from yaml import safe_load

from LightUB import *

# from LightUB.fns.tools import translate


LightConfig.lang = udB.get_key("language") or environ.get("LANGUAGE", "en")

languages = {}


for file in glob("strings/strings/*yml"):
    if file.endswith(".yml"):
        code = file.split("/")[-1].split("\\")[-1][:-4]
        try:
            languages[code] = safe_load(
                open(file, encoding="UTF-8"),
            )
        except Exception as er:
            LOGS.info(f"Error in {file[:-4]} language file")
            LOGS.exception(er)


def get_string(key: str, _res: bool = True) -> Any:
    lang = LightConfig.lang
    if lang not in languages:
        lang = "en"
    try:
        return languages[lang][key]
    except KeyError:
        return f"Failed to get string for '{key}'"


def get_help(key):
    doc = get_string(f"help_{key}", _res=False)
    if doc:
        return get_string("cmda") + doc


def get_languages() -> Dict[str, Union[str, List[str]]]:
    return {
        code: {
            "name": languages[code]["name"],
            "natively": languages[code]["natively"],
            "authors": languages[code]["authors"],
        }
        for code in languages
    }
