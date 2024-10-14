from libqtile.config import Click, Drag, KeyChord, Key
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.utils import guess_terminal


mod = "mod4"
alt = "mod1"

terminal = guess_terminal("x-terminal-emulator")


keys = [
    Key([mod], "l", lazy.spawn("betterlock-wrapper --manual"), desc="Lock screen"),
    Key([mod], "p", lazy.spawn("xset dpms force off"), desc="Turn the screen black"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
    Key(["control"], "Print", lazy.spawn("flameshot full"), desc="Take a screenshot of the whole screen"),
    Key([mod], "Pause", lazy.spawn("toggle_media"), desc="Pause or play media"),

    Key([mod], "Tab", lazy.group.next_window(), desc="Move window focus to next window"),
    Key([mod], "grave", lazy.spawn("rofi -modi window,windowcd -show window"), desc="Move focus using rofi"),


    Key([mod], "a", lazy.layout.left(), desc="Move focus left"),
    Key([mod], "d", lazy.layout.right(), desc="Move focus right"),
    Key([mod], "s", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "w", lazy.layout.up(), desc="Move focus up"),
    
    Key([mod, "shift"], "a", lazy.layout.move_left(), desc="Move window left"),
    Key([mod, "shift"], "d", lazy.layout.move_right(), desc="Move window right"),
    Key([mod, "shift"], "s", lazy.layout.move_down(), desc="Move window down"),
    Key([mod, "shift"], "w", lazy.layout.move_up(), desc="Move window up"),
    
    Key([mod, "control"], "a", lazy.layout.grow_width(-50), desc="Grow window left"),
    Key([mod, "control"], "d", lazy.layout.grow_width(50), desc="Grow window right"),
    Key([mod, "control"], "s", lazy.layout.grow_height(50), desc="Grow window down"),
    Key([mod, "control"], "w", lazy.layout.grow_height(-50), desc="Grow window up"),

    Key([mod, alt], "a", lazy.layout.integrate_left(), desc="Integrate window left"),
    Key([mod, alt], "d", lazy.layout.integrate_right(), desc="Integrate window right"),
    Key([mod, alt], "s", lazy.layout.integrate_down(), desc="Integrate window down"),
    Key([mod, alt], "w", lazy.layout.integrate_up(), desc="Integrate window up"),

    Key([mod], "up", lazy.layout.mode_vertical(), desc="Integrate window down"),
    Key([mod], "down", lazy.layout.mode_vertical(), desc="Integrate window down"),
    Key([mod], "right", lazy.layout.mode_horizontal(), desc="Integrate window up"),
    Key([mod], "left", lazy.layout.mode_horizontal(), desc="Integrate window up"),

    Key([mod, "shift"], "up", lazy.layout.mode_vertical_split(), desc="Integrate window down"),
    Key([mod, "shift"], "down", lazy.layout.mode_vertical_split(), desc="Integrate window down"),
    Key([mod, "shift"], "left", lazy.layout.mode_horizontal_split(), desc="Integrate window up"),
    Key([mod, "shift"], "right", lazy.layout.mode_horizontal_split(), desc="Integrate window up"),

    Key([mod], "n", lazy.layout.reset_size(), desc="Reset all window sizes"),


    Key([mod], "x", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),

    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "m", lazy.window.toggle_maximize(), desc="Toggle maximized on the focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "r", lazy.spawn("rofi -show run"), desc="Spawn a command using rofi"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn an application using rofi"),
    Key([alt], "f4", lazy.window.kill(), desc="Kill focused window.")
]


start_size: tuple[int, int] = (0, 0)

@lazy.function
def get_size(qtile):
    global start_size
    start_size = qtile.current_window.get_size()
    return start_size


@lazy.function
def resize(qtile, x, y):
    layout = qtile.current_layout
    windows = list(filter(lambda e: not e.floating, layout.group.windows))
    if layout.name == "plasma" and not qtile.current_window.floating and len(windows) > 1:
        mouse_pos: tuple[int, int] = qtile.core.get_mouse_position()

        middle_x: int = int(layout.focused_node.x + (layout.focused_node.width / 2))
        middle_y: int = int(layout.focused_node.y + (layout.focused_node.height / 2))

        if middle_x <= mouse_pos[0]:
            layout.focused_node.width = x
        else:
            layout.focused_node.width = start_size[0] * 2 - x

        if middle_y <= mouse_pos[1]:
            layout.focused_node.height = y
        else:
            layout.focused_node.height = start_size[1] * 2 - y

        layout.layout(windows, layout.group.screen.get_rect())

    else:
        qtile.current_window.set_size_floating(x, y)

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position(), start=lazy.window.get_position()),
    Drag([mod], "Button3", resize(), start=get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

