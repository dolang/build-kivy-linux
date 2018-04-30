"""
Utilities.

:author: Dominik Lang
:license: MIT
"""

from collections import namedtuple
from pathlib import Path


__all__ = ['WheelNameInfo', 'parse_wheel_name']


WheelNameInfo = namedtuple('WheelNameInfo',
                           ('distribution, version, build_tag,'
                            ' python_tag, abi_tag, platform_tag'))


def parse_wheel_name(name):
    """Parse the name of a wheel and return a `WheelNameInfo`.
    
    Accepts a `Path` or any object whose string representation is the
    name of a wheel file.
    """
    if isinstance(name, Path):
        name = name.absolute().name  # convert to string path name
    else:
        name = str(name)  # ensure it's a string
    try:
        assert name.endswith('.whl'), "name doesn't end with '.whl'"
        parts = name[:-4].split('-')
        if len(parts) == 5:  # build_tag is optional and not present
            # Per the PEP (427/491) only numbers are allowed as
            # `build_tag` if it's present.  Inserting an empty string
            # to denote it's missing, so all parts have the same type.
            parts.insert(2, '')
        assert len(parts) == 6, "it doesn't have the expected number of parts"
        return WheelNameInfo(*parts)
    except Exception as ex:
        raise ValueError("Unable to parse '{}'. Error: {}".format(name, ex))
