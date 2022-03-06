import sublime
import re
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

    if newproject and settings.get("create_new_project_if_empty"):

        def cb_new_project(name: str) -> None:
            if len(name) < 1:
                name = filename

            project_file_dir = settings.get("new_project_file_location", ".")
            if project_file_dir == ".":
                project_file_dir = directory
            else:
                project_file_dir = sublime.expand_variables(project_file_dir, win.extract_variables())
            project_file_dir = expanduser(project_file_dir)
            project_file_path = join(project_file_dir, "%s.sublime-project" % (name))
            workspace_file_path = re.sub(r"\.sublime-project$", ".sublime-workspace", project_file_path)

            if not isdir(project_file_dir):
                makedirs(project_file_dir)

            with open(project_file_path, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(sublime.encode_value(win.project_data(), True))

            with open(workspace_file_path, mode="w", encoding="utf-8", newline="\n") as f:
                f.write(sublime.encode_value({}, True))

            self.window.run_command("close_project")  # type: ignore
            self.window.run_command("close_workspace")  # type: ignore
            self.window.run_command("close_all")  # type: ignore
            subl("--project", workspace_file_path)

        win.show_input_panel(
            "New Project: ",
            filename,
            cb_new_project,
            None,
            None,
        )
