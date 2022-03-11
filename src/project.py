"""
by budRich 2018,2021,2022
See LICENSE for details.
"""

import sublime
from os.path import split
from .paths import tilde_prefix


def add_directory_to_project(target: str) -> None:
    win = sublime.active_window()
    project_data = win.project_data() or {}
    project_folders = project_data.get("folders") or []
    settings = sublime.load_settings("PathBox.sublime-settings")

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

    if newproject and settings.get("use_project_manager"):
        win.run_command("project_manager", {"action": "add_project"})
