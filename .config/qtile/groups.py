from libqtile.config import Group, KeyChord, Key, Match, MatchAll, InvertMatch, ScratchPad, DropDown
from libqtile.lazy import lazy

from keys import keys, mod

groups = [
    Group(
        "1",
        label="⬤",
    ),

    Group(
        "2",
        label="⬤",
    ),

    Group(
        "3",
        label="⬤",
    ),

    Group(
        "4",
        label="⬤",
    ),

    Group(
        "5",
        label="⬤",
    ),

    Group(
        "6",
        label="⬤",
    ),

    Group(
        "7",
        label="⬤",
    ),

    Group(
        "8",
        label="⬤",
        layout="max",
        matches=[
            Match(wm_class="discord"),
            Match(wm_class="thunderbird-default"),
            Match(wm_class="Signal")
        ]
    ),

    Group(
        "9",
        label="⬤",
        layout="max",
        matches=[
            MatchAll(
                Match(wm_class="steam"),
                InvertMatch(Match(title="Launching..."))
            ),
            Match(wm_class="lutris"),
            Match(wm_class="heroic"),
        ]
    ),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(toggle=True),
            desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False),
            desc="Move focused window to group {}".format(i.name))
    ])
