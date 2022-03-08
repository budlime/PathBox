import sublime
from os import makedirs
from os.path import split, expanduser, join, isdir
from .paths import tilde_prefix
from .subl import subl


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

    if newproject and settings.get("create_new_project_with_project_manager"):
        win.run_command("project_manager", {"action": "add_project"})
