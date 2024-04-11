#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  confirm_library_integrity.py
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
import os


def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] == 2:
    __eprint__("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)

# get length of argv
ARGC = len(sys.argv)


def scan_files(directory):
    FILES = os.listdir(directory)
    status = False
    library = {}
    if directory[-1] != "/":
        directory = directory + "/"
    for each in FILES:
        if os.path.isfile(directory + each):
            path = directory + each
            try:
                with open(path, "r") as file:
                    data = json.load(file)
            except json.JSONDecodeError as e:
                __eprint__(f"Error loading {path}: JSON Syntax Error")
                __eprint__(f"Error: {e}")
                status = True
                continue
            if type(data) is not dict:
                __eprint__(f"{path} must contain a dict, not {type(data)}")
                status = True
                continue
            library = dict(library, **data)
        elif os.path.isdir(directory + each):
            recurse = scan_files(directory + each)
            status = recurse[0]
            library = dict(library, **recurse[1])
    return [status, library]

status = scan_files("Library")
if status[0]:
    __eprint__("Errors found!")
    exit(1)
print("No Errors found. Library has good integrity.")
size = sys.getsizeof(status[1])
unit = "bytes"
units = ["KiB", "MiB", "GiB", "TiB"]
count = 0
while (size / 1024) >= 1:
    size = size / 1024
    unit = units[count]
    count += 1

print(f"Size of library in memory: { size } { unit }")
