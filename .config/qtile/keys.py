from libqtile.config import Click, Drag, KeyChord, Key
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal


mod = "mod4"
alt = "mod1"


terminal = guess_terminal("x-terminal-emulator")


old_layout = "gridselect"


def switch_gridselect(qtile):
    global old_layout
    old_layout, qtile.current_group.layout = qtile.current_group.layout.name, old_layout


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "l", lazy.spawn("betterlock-wrapper --manual"), desc="Lock screen"),
    Key([mod], "p", lazy.spawn("xset dpms force off"), desc="Turn the screen black"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
    Key(["control"], "Print", lazy.spawn("flameshot full"), desc="Take a screenshot of the whole screen"),
    Key([mod], "Tab", lazy.group.next_window(), desc="Move window focus to other window"),
    Key([mod], "grave", lazy.spawn("rofi -modi window,windowcd -show window"), desc="Move focus using rofi"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "x", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.function(switch_gridselect), desc="Switch between current and gridselect layout"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod, "shift"], "r", spawncmd("Spawn", "appprompt"), desc="Spawn a command using a prompt widget"),
    # Key([mod], "r", spawncmd("Spawn App", "appprompt", "gtk-launch '%s'", "app", strict_completer=True),
    #     desc="Spawn an application using a prompt widget"),
    Key([mod, "shift"], "r", lazy.spawn("rofi -show run"), desc="Spawn a command using rofi"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn an application using rofi"),
    Key([alt], "f4", lazy.window.kill(), desc="Kill focused window.")
]


def resize(w, h):
    pass


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]
