# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from libqtile import qtile, layout, hook
from libqtile.config import Match, MatchAll, InvertMatch
from libqtile.backend.x11.window import Window
from libqtile.log_utils import logger
from libqtile.utils import send_notification

from color import window_border
from screens import screens, widget_defaults, extension_defaults
from keys import mod, mouse
from groups import groups, keys
from layouts import layouts


@hook.subscribe.startup_once
def autorun():
    qtile.spawn("lxpolkit")
    qtile.spawn("betterlock-wrapper --setup")
    qtile.spawn("picom --daemon")
    qtile.spawn("steam -silent")
    qtile.spawn("heroic --no-gui")
    qtile.spawn("lutris")
    qtile.spawn("discord --start-minimized")
    qtile.spawn("signal-desktop")
    qtile.spawn("thunderbird")

    def close_lutris(window):
        if window.name == "Lutris":
            window.kill()
            hook.unsubscribe.client_new(close_lutris)

    hook.subscribe.client_new(close_lutris)


def check_godot(client: Window):
    return "Godot_Editor" in client.get_wm_class() and not (
        client.name.endswith(" - Godot Engine") or client.name.endswith(" - Project Manager")
        or client.name == "Godot"
    ) or "Godot_Engine" in client.get_wm_class() or "Godot_ProjectList" in client.get_wm_class()


def check_brave(client: Window):
    return " - Brave" in client.name and "brave-browser-beta" not in client.get_wm_class()


def focus_behavior(client: Window) -> bool:
    focus: bool = (
        "firefox" in client.get_wm_class()
        or "brave-browser-beta" in client.get_wm_class()
        or "Signal" in client.get_wm_class()
        or "heroic" in client.get_wm_class()
        or ("discord" in client.get_wm_class() and client.name != "Discord")
        or client.group.screen == qtile.current_screen
    )
    if not focus:
        pass  # send_notification()
    return focus


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_width=1,
    **window_border,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(func=check_godot),
        MatchAll(
            Match(wm_class="steam"),
            InvertMatch(Match(title="Steam"))
        ),
        Match(func=check_brave),
    ]
)
auto_fullscreen = True
focus_on_window_activation = focus_behavior
reconfigure_screens = False

auto_minimize = True

wl_input_rules = None

wl_xcursor_theme = None
wl_xcursor_size = 24


wmname = "LG3D"
