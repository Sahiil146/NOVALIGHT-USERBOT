# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

"""
Exceptions which can be raised by Light UserBot.
"""


class LightUBError(Exception):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...
