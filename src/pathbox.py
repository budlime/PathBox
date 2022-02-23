"""
A package to make opening files in Sublime Text a little bit less painful.
Licensed under GPL V2.

Mod by budRich 2018,2021,2022
Written by Ross Hemsley and other collaborators 2013.
"""

import sublime
import sublime_plugin

from os.path import isdir, expanduser, split, join

from .matching import get_completion, COMPLETION_TYPE, get_matches
from .paths import directory_listing_with_slahes, tilde_prefix

from typing import Optional, Callable

STATUS_MESSAGES = {
    COMPLETION_TYPE.CompleteButNotUnique: "Complete, but not unique",
    COMPLETION_TYPE.NoMatch: "No match",
    COMPLETION_TYPE.Complete: None,
}


def show_completion_message(completion_type: int):
    status = STATUS_MESSAGES.get(completion_type)

    if status:
        sublime.status_message(status)


class PathBox(sublime_plugin.WindowCommand):
    """
    This is the command called by the UI.
    input_panel contains an instance of the class
    PathBoxInput when the input is active,
    otherwise it contains None.
    """

    input_panel: "Optional[PathBoxInput]" = None


class PathBoxInput:
    """
    This class encapsulates the behaviors relating
    to the file open panel used by the package. We
    create an instance when the panel is open, and
    destroy it when the panel is closed.
    """

    def __init__(self, callback: Callable[..., None], prompt: str, start_text: Optional[str]):
        # If the user presses tab, and nothing happens, remember it.
        # If they press tab again, we show them a list of files.

        self.path_cache = None

        active_window = sublime.active_window()

        self.view: sublime.View = active_window.show_input_panel(
            "%s: " % (prompt),
            tilde_prefix(start_text, True) if start_text else "",
            callback,
            self.update,
            self.cancel,
        )

    def update(self, text: str):
        """
        If the user updates the input, reset the 'failed completion' flag.
        """
        del text

    def cancel(self):
        PathBox.input_panel = None

    def get_text(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def set_text(self, s: str):
        self.view.run_command("path_box_update", {"append": False, "text": s})

    def show_completions(self):
        """
        Show a quick panel containing the possible completions.
        """
        active_window = sublime.active_window()
        directory, filename = split(self.get_text())
        directory_listing = directory_listing_with_slahes(expanduser(directory))
        self.path_cache = get_matches(filename, directory_listing)

        if len(self.path_cache) == 0:
            show_completion_message(COMPLETION_TYPE.NoMatch)
        else:
            active_window.show_quick_panel(self.path_cache, self.on_done)

    def on_done(self, i: int):
        if self.path_cache is None:
            return

        elif i != -1:
            directory, _ = split(self.get_text())
            new_path = join(directory, self.path_cache[i])
            self.path_cache = None

            if isdir(expanduser(new_path)):
                self.set_text(new_path)
                sublime.active_window().focus_view(self.view)
            else:
                sublime.active_window().open_file(new_path)
                sublime.active_window().run_command("hide_panel", {"cancel": True})
        else:
            sublime.active_window().focus_view(self.view)

    def append_text(self, s: str):
        self.view.run_command("path_box_update", {"append": True, "text": s})


class PathBoxEventListener(sublime_plugin.EventListener):
    """
    When the tab key is tapped we must know that
    a PathBox widget is focused, this sets the
    "path_box" contect to true.
    """

    def on_query_context(self, view: sublime.View, key: str, *_) -> Optional[bool]:
        return key == "path_box" and PathBox.input_panel and PathBox.input_panel.view.id() == view.id()


class PathBoxUpdateCommand(sublime_plugin.TextCommand):
    """
    The edit command used for editing the text in the input panel.
    """

    def run(self, edit: sublime.Edit, append: bool, text: str):
        if append:
            self.view.insert(edit, self.view.size(), text)
        else:
            self.view.replace(edit, sublime.Region(0, self.view.size()), text)


class PathBoxCompleteCommand(sublime_plugin.WindowCommand):
    """
    The command called by tapping tab in the open panel.
    """

    def run(self, *_):
        input_panel = PathBox.input_panel

        if input_panel:
            completion, completion_type = get_completion(input_panel.get_text())
            show_completion_message(completion_type)
            input_panel.set_text(completion)

            if completion_type != COMPLETION_TYPE.Complete:
                input_panel.show_completions()
