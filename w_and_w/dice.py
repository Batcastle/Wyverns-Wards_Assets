#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  dice.py
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
import random as rand
import w_and_w.rules as rules


if sys.version_info[0] == 2:
    __eprint__("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)


def roll(faces: int, count: int, decader: bool = False) -> list:
    """Simulate rolling dice.

    This function provides a simple function call to perform dice rolls and coin flips.
    This function will always return True if called with faces == 1, and will throw an error if
    faces is > 20.
    Examples:
        - Roll 3D8: roll(8, 3)
        - Roll 1D2 (single coin flip): roll(2, 1)
        - Roll 2D20: roll(20, 2)
        - Roll 1D10 and 1 Decader die (for rolling out of 100): roll(10, 1, decader=True) + roll(10, 1)
    """
    if type(faces) != int:
        raise TypeError(f"`faces` is not int, got type: { type(faces) }")
    if type(count) != int:
        raise TypeError(f"`count` is not int, got type: { type(count) }")
    if type(decader) != bool:
        raise TypeError(f"`decader` is not bool, got type: { type(decader) }")
    if faces == 1:
        return [True] * count
    elif faces <= 0:
        raise ValueError("Cannot roll zero or fewer dice.")
    elif faces > 20:
        raise rules.RulesViolation(f"Cannot use dice with > 20 faces. Faces: { faces }")
    if decader:
        if faces != 10:
            raise ValueError(f"Faces must be 10 if using a decader. Faces: { faces }")
        output = []
        for each in range(count):
            output.append(rand.randint(0, 9) * 10)
        return output
    output = []
    for each in range(count):
        output.append(rand.randint(1, faces))
    return output
