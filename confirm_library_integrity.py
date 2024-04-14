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
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass


def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] == 2:
    __eprint__("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)

# get length of argv
ARGC = len(sys.argv)
with open("settings.json", "r") as file:
    settings = json.load(file)
    
def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = sys.getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = sys.getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


def scan_files(directory):
    FILES = os.listdir(directory)
    status = False
    library = {}
    if directory[-1] != "/":
        directory = directory + "/"
    for each in FILES:
        if os.path.isfile(directory + each):
            if each.split(".")[-1].upper() != "JSON":
                continue
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
            data = {path.split("/")[-1].split(".")[0]: data}
            library = dict(library, **data)
        elif os.path.isdir(directory + each):
            recurse = scan_files(directory + each)
            status = recurse[0]
            library = dict(library, **recurse[1])
    return [status, library]

status = scan_files(settings["lib_location"])
if status[0]:
    __eprint__("Errors found!")
    exit(1)
print("No Errors found. Library has good integrity.")
size = total_size(status[1])
unit = "bytes"
units = ["KiB", "MiB", "GiB", "TiB"]
count = 0
while (size / 1024) >= 1:
    size = size / 1024
    unit = units[count]
    count += 1

print(f"Size of library in memory: { '{:.1f}'.format(size) } { unit }")
