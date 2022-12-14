# Light UserBot
# Copyright (C) 2021-2022 CodeWithTyagi
#
# This file is a part of < https://github.com/CodeWithTyagi/Light >
# Please read the GNU Affero General Public License in
# https://www.github.com/CodeWithTyagi/Light/blob/main/LICENSE

from .. import udB


def get_stuff():
    return udB.get_key("ECHO") or {}


def add_echo(chat, user):
    x = get_stuff()
    k = x.get(int(chat))
    if k:
        if user not in k:
            k.append(int(user))
        x.update({int(chat): k})
    else:
        x.update({int(chat): [int(user)]})
    return udB.set_key("ECHO", x)


def rem_echo(chat, user):
    x = get_stuff()
    k = x.get(int(chat))
    if k:
        if user in k:
            k.remove(int(user))
        x.update({int(chat): k})
    return udB.set_key("ECHO", x)


def check_echo(chat, user):
    x = get_stuff()
    k = x.get(int(chat))
    if k and int(user) in k:
        return True


def list_echo(chat):
    x = get_stuff()
    return x.get(int(chat))
