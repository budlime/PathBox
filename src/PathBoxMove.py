"""
by budRich 2018,2021,2022
See LICENSE for details.
"""

import sublime
import os

from typing import Optional
from .pathbox import PathBox, PathBoxInput


class PathBoxMoveCommand(PathBox):
    def run(self):
        self.view = self.window.active_view()

        if self.view:
            self.current_file = self.view.file_name()
        if self.current_file:
            PathBox.input_panel = PathBoxInput(self.move_file, "Rename Path", self.current_file)

    def move_file(self, path: str):

        new_file = os.path.expanduser(path)

        if not self.validateFileName(self.view, self.current_file, new_file):
            return

        if self.view and self.view.is_dirty():
            self.window.run_command("save")

        print(self.current_file, os.path.expanduser(path))
        if self.current_file:
            os.renames(self.current_file, os.path.expanduser(path))

        if os.access(new_file, os.R_OK):  # Can read new file
            self.window.run_command("close")
            self.window.open_file(new_file)
        else:
            sublime.error_message("Error: Can not read new file: " + new_file)

        PathBox.input_panel = None

    def validateFileName(self, view: Optional[sublime.View], old_file: Optional[str], new_file: str) -> bool:
        if len(new_file) == 0:
            sublime.error_message("Error: No new filename given.")
            return False
        if view and view.is_loading():
            sublime.error_message("Error: The file is still loading.")
            return False
        if view and view.is_read_only():
            sublime.error_message("Error: The file is read-only.")
            return False
        if new_file == old_file:
            sublime.error_message("Error: The new file name was the same as the old one.")
            return False
        return True
