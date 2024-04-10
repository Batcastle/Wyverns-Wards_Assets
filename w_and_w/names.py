#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  names.py
#
#  Copyright 2024 Thomas Castleman <batcastle@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""Explain what this program does here!!!"""
from __future__ import print_function
import sys
import json
import random as rand


def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] == 2:
    __eprint__("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)

# get length of argv
ARGC = len(sys.argv)


with open("settings.json", "r") as file:
    library_dir = json.load(file)["lib_location"]
    
    
def generate_name(gender: str, loc=library_dir, include_lastname=True) -> str:
    """Generate a random name given a specific gender"""
    if loc[-1] == "/":
        path = loc
    else:
        path = loc + "/"
    if type(include_lastname) is not bool:
        raise TypeError(f"include_lastname is not bool. Type: { type(include_lastname) }")
    with open(path + "Etc/Names.json", "r") as file:
        data = json.load(file)
    if type(gender) in (bool, str, None):
        if gender is None:
            first = data["FIRST"]["NEUTRAL"]
        elif gender in (True, "MALE"):
            first = data["FIRST"]["MALE"] + data["FIRST"]["NEUTRAL"]
        elif gender in (False, "FEMALE"):
            first = data["FIRST"]["FEMALE"] + data["FIRST"]["NEUTRAL"]
        else:
            raise AttributeError("Not a recognized input.")
    first = rand.sample(first, 1)[0]
    last = rand.sample(data["LAST"], 1)[0]
    if include_lastname:
        return f"{ first } { last }"
    return first
    


if __name__ == "__main__":
    main(ARGC, sys.argv)
