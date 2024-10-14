from libqtile.config import Group, Key, Match, MatchAll, InvertMatch, ScratchPad, DropDown
from libqtile.lazy import lazy

from keys import keys, mod

groups = [
    Group(
        "1",
        label="⬤",
        spawn="sensible-browser"
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
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "NVIDIA Settings",
                "/usr/bin/nvidia-settings",
                on_focus_lost_hide=False,
                width=0.8,
                height=0.82,
                x=0.1,
                y=0.09

            ),
            DropDown(
                "Pavucontrol",
                "/usr/bin/pavucontrol",
                on_focus_lost_hide=False,
                width=0.5,
                height=0.5,
                x=0.25,
                y=0.25
            )
        ]
    )
]

for i in groups:
    if type(i) is ScratchPad:
        continue
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(toggle=True),
            desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False),
            desc="Move focused window to group {}".format(i.name))
    ])

for idx, dropdown in enumerate(groups[-1].dropdowns):
    keys.append(Key(
        [mod], f"f{idx + 1}", lazy.group["scratchpad"].dropdown_toggle(dropdown.name),
        desc=f"Toggle DropDown '{dropdown.name}'"
    ))

