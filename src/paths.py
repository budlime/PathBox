"""
Mod by budRich 2018,2021,2022
Written by Ross Hemsley and other collaborators 2013.
See LICENSE for details.
"""

import sublime
from os.path import isdir, expanduser, split, join
from os import listdir, sep, getenv

from typing import List, Optional

HOME_DIRECTORY = "~"


def add_directory_to_project(target: str) -> None:
    win = sublime.active_window()
    project_data = win.project_data() or {}
    project_folders = project_data.get("folders") or []

    newproject = project_data == {}

    _, filename = split(target)
    directory = tilde_prefix(target, True)[:-1]

    folder = dict(
        path=directory,
        name=filename,
        follow_symlinks=True,
        folder_exclude_patterns=[".*"],
    )
    if all(folder["path"] != directory for folder in project_folders):
        project_data.setdefault("folders", []).append(folder)
    win.set_project_data(project_data)

    if newproject:
        win.run_command("project_manager", {"action": "add_project"})


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

    if use_tilde and home and target.startswith(home):
        target = "~" + target[len(home) :]

    return target


def get_current_directory(view_filename: Optional[str]) -> str:
    """
    Returns current files parent directory. Or
    Home directory With a trailing slash
    """
    if view_filename:
        directory, _ = split(view_filename)
    else:
        directory = HOME_DIRECTORY

    if directory != sep:
        directory += sep

    return tilde_prefix(directory, True)
