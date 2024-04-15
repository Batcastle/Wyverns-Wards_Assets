#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  settings.py
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
import copy

def __eprint__(*args, **kwargs):
    """Make it easier for us to print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


if sys.version_info[0] == 2:
    __eprint__("Please run with Python 3 as Python 2 is End-of-Life.")
    exit(2)


class Settings_Abstraction():
    """Settings management data class"""
    def get(self, key):
        """Get data with key"""
        if key in self.settings.keys():
            return self.settings[key]
        else:
            raise KeyError(f"Key {key} not found in {self.settings.keys()}")
            
    def set(self, key, data):
        """Set new data with key
        
        NOTE: Any changes made here are temporary. To make them permenant, call:
        
            Settings.apply_updates()
        
        """
        if not self.changes_not_applied:
            self.changes_not_applied = True
            self.settings_copy = copy.deepcopy(self.settings)
        self.settings[key] = data
        
    def apply_changes(self, bypass_check=False):
        """Make any changes to settings permanent
        
        """
        if self.changes_not_applied or bypass_check:
            try:
                with open(self.settings_file, "w+") as file:
                    json.dump(self.settings, file, indent=2)
            except (PermissionError, IOError) as e:
                print(f"An unknown error occurred:\n{e}")
                return False
            self.changes_not_applied = False
            return True
        return False
    
    def undo_changes(self):
        """Attempt to undo changes
        
        Return True if successful, False if not.
        """
        if self.changes_not_applied:
            if self.settings == self.settings_copy:
                # We have no backups anymore. It's too late.
                # You have likely already reverted any changes. The data you want is likely too old.
                return False
            self.settings = copy.deepcopy(self.settings_copy)
            # Changes where not applied and this is the first revert. We can recover.
            return True
        # Any changes have already been applied. We do not overwrite self.settings_copy when that
        # happens, specifically in case of this scenario
        if self.settings == self.settings_copy:
            # This shouldn't happen, since we don't overwrite the copy when we write to disk,
            # but someone could come in and manually do it. If that happens, you basically screw yourself over.
            return False
        self.settings = copy.deepcopy(self.settings_copy)
        return True
        
class User_Settings(Settings_Abstraction):
    """User Settings class"""
    def __init__(self):
        """Initialization and loading of data"""
        self.settings_file = "user_settings.json"
        self.changes_not_applied = False
        if os.path.isfile(self.settings_file):
            with open(self.settings_file, "r") as file:
                self.settings = json.load(file)
        else:
            self.settings = {}
            self.apply_changes(bypass_check=True)
        self.settings_copy = copy.deepcopy(self.settings)
        

class Internal_Settings(Settings_Abstraction):
    """Internal Settings Class"""
    def __init__(self):
        """Initialization and loading of data"""
        self.settings_file = "internal_settings.json"
        self.changes_not_applied = False
        if os.path.isfile(self.settings_file):
            with open(self.settings_file, "r") as file:
                self.settings = json.load(file)
        else:
            self.settings = {}
            self.apply_changes(bypass_check=True)
        self.settings_copy = copy.deepcopy(self.settings)
