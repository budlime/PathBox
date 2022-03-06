this is a modified fork of the [iOpener] package.  

### python38/ST4
With newer versions of sublime text
One can use the python38 interpreter that includes
the typing library. With LSP installed this helps
developing quite a bit. So I refactored the code
to be more or less statically typed.
This however makes the package not compatible with
earlier versions of sublime (not even ST3).

And I therefor dropped the different tests for
sublime versions.

### Restructured the project 
`iOpener.py` -> `pathbox.py`, `PathBoxOpen.py`

I extracted the tab-completion stuff into a separate module
so it is "easy" to use it for other things than opening a file.

**PathBoxMove** command will rename the **path** of the currently
open file. *i.e* move it. Using the same UI. If a directory needed
doesn't exist it will get created.

**PathBoxOpen** command is similar to iOpener, it will also
create necessary directories when it is used to open a
non-existing file. *i.e* creating a new file.
If a directory is opened it gets added to the current
project. 

If the setting `"create_new_project_if_empty"` is
set to **true**, a new project will get created
when adding a directory when no project is active.

It is also, in the settings file, possible to
specify a directory where the `sublime-project`
file should be placed in that case.
(Defaults to "." *i.e.* the same directory that
was added).

Worth noting is that by making the more general
module `pathbox.py`, I decided to drop support
for history.

With iOpener when multiple completions is available
when `tab` was pressed, an additional `tab` press
was needed to show the completions. With PathBox
completions are shown after the first press
instead.

You have to enable keybindings yourself,
personally i use:  

```JSON
{ "keys": ["ctrl+o"], "command": "path_box_open" },
{ "keys": ["f2"], "command": "path_box_move" },
```


[iOpener]: https://github.com/rosshemsley/iOpener
[ProjectManager]: https://github.com/randy3k/ProjectManager
