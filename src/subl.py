"""
Copyright (c) 2022 budRich
Copyright (c) 2017 Randy Lai <randy.cs.lai@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

the subl() function in this file was copied from ProjectManager
https://github.com/randy3k/ProjectManager
"""

import sublime, sublime_plugin
from subprocess import Popen
from typing import Optional


def subl(*args: str):
    executable_path = sublime.executable_path()
    if sublime.platform() == "osx":
        app_path = executable_path[: executable_path.rfind(".app/") + 5]
        executable_path = app_path + "Contents/SharedSupport/bin/subl"

    Popen([executable_path] + list(args))

    def on_activated():
        window = sublime.active_window()
        view: Optional[sublime.View] = window.active_view()

        if not view:
            return

        if sublime.platform() == "windows":
            # fix focus on windows
            window.run_command("focus_neighboring_group")  # type: ignore
            window.focus_view(view)

        sublime_plugin.on_activated(view.id())
        sublime.set_timeout_async(lambda: sublime_plugin.on_activated_async(view.id()))

    sublime.set_timeout(on_activated, 300)
