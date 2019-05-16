#!/usr/bin/env python3

import re


def is_valid(name):
    """
    Check if specified name is compliant with requirements for it.

    The max length of the name is 16 characters. It seems reasonable to have this limitation
    because the plugin name is used for directory name on the file system and it is also used
    as a name of some Python objects, like class names, so it is expected to be relatively short.
    """
    return bool(re.match(r'^[a-z][0-9a-z_]{2,15}$', name))


def to_camel(name):
    """
    Convert plugin name from snake to camel case
    """
    return name.title().replace('_', '')


def to_caps(name):
    """
    Convert plugin name from snake to upper snake case
    """
    return name.upper()


def to_dash(name):
    """
    Convert plugin name from snake case to dash representation
    """
    return name.replace('_', '-')
