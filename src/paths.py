"""
Mod by budRich 2018,2021,2022
Written by Ross Hemsley and other collaborators 2013.
See LICENSE for details.
"""

from os.path import isdir, expanduser, split, join
from os import listdir, sep, getenv

from typing import List, Optional


def directory_listing_with_slahes(source_dir: str) -> List[str]:
    output: List[str] = []
    for filename in listdir(source_dir):
        if isdir(join(source_dir, filename)):
            output.append(filename + sep)
        else:
            output.append(filename)

    return output


def tilde_prefix(target: str, use_tilde: bool):
    home: Optional[str] = getenv("HOME")
    target = expanduser(target)

    # make sure directories have a trailing slash
    if isdir(target) and target != sep and target[-1] != sep:
        target += sep

    if use_tilde and home and target.startswith(home):
        target = "~" + target[len(home) :]

    return target


def get_current_directory(view_filename: Optional[str]) -> str:

    if view_filename:
        directory, _ = split(view_filename)
    else:
        directory = "~"

    return tilde_prefix(directory, True)
