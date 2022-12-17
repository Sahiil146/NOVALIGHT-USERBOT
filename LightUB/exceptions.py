# NovaLight UserBot
# Copyright (C) 2021-2022 Nova akki
#
# This file is a part of < https://github.com/manuop1234/NOVALIGHT-USERBOT >
# Please read the GNU Affero General Public License in
# https://github.com/manuop1234/NOVALIGHT-USERBOT/blob/main/LICENSE

"""
Exceptions which can be raised by Light UserBot.
"""


class LightUBError(Exception):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...
