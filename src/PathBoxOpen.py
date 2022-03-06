"""
Mod by budRich 2018,2021,2022
Written by Ross Hemsley and other collaborators 2013.
See LICENSE for details.
"""

import sublime

from os import path, makedirs, sep

from .pathbox import PathBox, PathBoxInput
from .paths import get_current_directory, tilde_prefix
from .project import add_directory_to_project


class PathBoxOpenCommand(PathBox):
    def run(self):
        current_file = None

        active_window = sublime.active_window()
        active_view = active_window.active_view()

        if active_view:
            current_file = active_view.file_name()

        folder = get_current_directory(current_file)
        PathBox.input_panel = PathBoxInput(self.open_file, "Open Path", folder)

    def open_file(self, target: str):

        if not target:
            sublime.status_message("Warning: Ignoring empty path.")
            return

        directory = ""
        filename = ""

        target = path.expanduser(target)

        # expanduser() adds a trailing sep to directories
        if target[-1] == sep:
            directory = target
        else:
            directory, _ = path.split(target)

        if not path.isdir(directory):
            try:
                makedirs(directory)
            except OSError as e:
                sublime.error_message("Failed to create path with error: " + str(e))
                return

        if path.isdir(target):
            add_directory_to_project(target)
        else:
            if not path.isfile(target):
                sublime.status_message("Created new buffer '" + filename + "'")
            sublime.active_window().open_file(target)
        PathBox.input_panel = None
