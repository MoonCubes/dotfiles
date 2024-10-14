from libqtile import bar, qtile
from libqtile import widget as basewidget
from libqtile.command.base import expose_command
from libqtile.config import Screen
from libqtile.utils import send_notification
from libqtile.log_utils import logger
from libqtile.scratchpad import ScratchPad

import qtile_extras.widget as widget


from os import path, listdir
from re import search, match

from color import colors


def window_count():
    windows = 0
    for i in qtile.groups:
        if type(i) is ScratchPad:
            continue
        windows += len(i.windows)
    return windows


class BetterNvidiaSensors(widget.NvidiaSensors):
    defaults = [
        (
            "format_normal",
            "{temp}°C",
            "Display string format. Three options available:  "
            "``{temp}`` - temperature, ``{fan_speed}`` and ``{perf}`` - "
            "performance level",
        ),
        (
            "format_hovered",
            "{fan_speed}",
            "Display string format. Three options available:  "
            "``{temp}`` - temperature, ``{fan_speed}`` and ``{perf}`` - "
            "performance level",
        ),
        ("foreground_alert", "ff0000", "Foreground colour alert"),
        (
            "gpu_bus_id",
            "",
            "GPU's Bus ID, ex: ``01:00.0``. If leave empty will display all " "available GPU's",
        ),
        ("update_interval", 5, "Update interval in seconds."),
        (
            "threshold",
            70,
            "If the current temperature value is above, "
            "then change to foreground_alert colour",
        ),
    ]

    def __init__(self, **config):
        basewidget.base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(BetterNvidiaSensors.defaults)
        self.foreground_normal = self.foreground
        self.format = self.format_normal

        self.add_callbacks(
            {
                "Button1": self.open_settings
            }
        )

    def open_settings(self):
        qtile.spawn("nvidia-settings")

    def mouse_enter(self, *args, **kwargs):
        self.format = self.format_hovered
        self.force_update()

    def mouse_leave(self, *args, **kwargs):
        self.format = self.format_normal
        self.force_update()


class SmartExit(widget.WidgetBox):
    """
    A button to shut down Qtile or the Computer.
    """

    class SmartExitWidget(widget.TextBox):

        def __init__(self, default, action_name, action, override):
            widget.TextBox.__init__(self)
            self.add_defaults([
                ("action_text", default, "The default text"),
                ("confirm_text", "Confirm", "The text displayed after being pressed."),
                ("decorations", [
                    widget.decorations.RectDecoration(
                        radius=5,
                        line_colour=colors[0],
                        line_width=1,
                        padding_y=3,
                        colour="66666689",
                        filled=True
                    )
                ])
            ])
            self.add_callbacks({"Button1": self.trigger})
            self.action_name = action_name
            self.action = action
            self.override = override
            self.__reset()

        def __reset(self):
            self.pressed = False
            self.text = self.action_text

        @expose_command()
        def trigger(self):
            windows = window_count()
            if not windows or self.pressed:
                self.action()
            else:
                if self.override:
                    self.pressed = True
                    self.text = self.confirm_text
                    send_notification(f"Confirm {self.action_name.capitalize()}",
                                      f"{windows} windows are still open. Do you really want to {self.action_name}?")
                    self.timeout_add(10, self.__reset)
                else:
                    send_notification(f"{self.action_name.capitalize()}",
                                      f"Can't {self.action_name} while {windows} windows are still open.")

    pressed = False

    def __init__(self, override: bool = False, **config):
        widget.TextBox.__init__(self, **config)
        self.add_defaults(widget.WidgetBox.defaults)
        self.box_is_open = False
        self.add_callbacks({"Button3": self.toggle})

        self.add_defaults([
            ("logout_text", "Logout", "The text displayed on the button."),
            ("shutdown_text", " Shutdown ", "The text displayed on the button."),
            ("reboot_text", " Reboot ", "The text displayed on the button."),
            ("confirm_text", "Confirm", "The text displayed after being pressed.")
        ])
        self.override = override
        self.widgets = [
            widget.Spacer(5),
            self.SmartExitWidget(self.shutdown_text, "shutdown", lambda: qtile.spawn('systemctl poweroff'),
                                 self.override),
            widget.Spacer(5),
            self.SmartExitWidget(self.reboot_text, "reboot", lambda: qtile.spawn('systemctl reboot'), self.override),
        ]

        self.close_button_location: str
        if self.close_button_location not in ["left", "right"]:
            val = self.close_button_location
            logger.warning("Invalid value for 'close_button_location': %s", val)
            self.close_button_location = "left"

        self.add_callbacks({"Button1": self.trigger})
        self.__reset()

    def __reset(self):
        self.pressed = False
        self.set_box_label()

    def set_box_label(self):
        self.text = self.logout_text

    def _configure(self, qtile, bar):
        widget.WidgetBox._configure(self, qtile, bar)
        self.set_box_label()

    @expose_command()
    def trigger(self):
        windows = window_count()
        if not windows or self.pressed:
            self.qtile.stop()
        else:
            if self.override:
                self.pressed = True
                self.text = self.confirm_text
                send_notification("Confirm Logout", f"{windows} windows are still open. Do you really want to logout?")
                self.timeout_add(10, self.__reset)
            else:
                send_notification("Logout", f"Can't logout while {windows} windows are still open.")


class Timer(widget.TextBox):
    timer = None

    def __init__(self, **config):
        widget.TextBox.__init__(self, "0", **config)
        self.__reset(True)
        self.add_callbacks({"Button1": self.timer_pause})
        self.add_callbacks({"Button3": self.timer_stop})

    def __reset(self, init=False):
        self.is_counting = False
        self.countdown = 0
        self.text = ""
        self.timer.cancel() if self.timer is not None and not init else None
        qtile.current_screen.top.draw() if not init else None

    def update(self):
        if not self.is_counting:
            return

        if self.countdown == 0:
            self.timer_finish()
            return

        m, s = divmod(self.countdown, 60)
        if m > 99:
            m = 99
            s = 59
        self.text = f"{f'0{m}'[-2:]}:{f'0{s}'[-2:]}"
        self.countdown -= 1
        self.timer = self.timeout_add(1, self.update)
        self.draw()

    @expose_command("start")
    def timer_start(self, time_regex: str):
        regex = r"(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?"
        time = match(regex, time_regex).groupdict()
        m = int(time["minutes"]) if time["minutes"] else 0
        s = int(time["seconds"]) if time["seconds"] else 0
        self.countdown = m * 60 + s
        self.is_counting = True
        self.update()
        qtile.current_screen.top.draw()

    @expose_command("pause")
    def timer_pause(self):
        self.is_counting = not self.is_counting
        self.update()

    @expose_command("stop")
    def timer_stop(self):
        self.__reset()

    def timer_finish(self):
        self.timer_stop()
        qtile.spawn("mpv --no-video /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga")
        send_notification("Timer", "The timer has finished", timeout=6000)


class DynamicTaskList(widget.TaskList):
    def calc_box_widths(self):
        """
        Calculate box width for each window in current group.
        """
        windows = self.windows
        window_count = len(windows)

        # if no windows present for current group just return empty list
        if not window_count:
            return []

        # Determine available and max average width for task name boxes.
        width_total = self.max_width - 2 * self.margin_x - (window_count - 1) * self.spacing

        names = [self.get_taskname(w) for w in windows]

        if self.icon_size == 0:
            icons = len(windows) * [None]
        else:
            icons = [self.get_window_icon(w) for w in windows]

        # Obey title_width_method if specified
        if self.title_width_method == "uniform":
            width_uniform = width_total // window_count
            width_boxes = [width_uniform for w in range(window_count)]
        else:
            # Default behaviour: calculated width for each task according to
            # icon and task name consisting
            # of state abbreviation and window name
            width_boxes = [
                int(
                    self.box_width(names[idx])
                    + ((self.icon_size + self.padding_x) if icons[idx] else 0)
                )
                for idx in range(window_count)
            ]

        # Obey max_title_width if specified
        if self.max_title_width:
            width_boxes = [min(w, self.max_title_width) for w in width_boxes]
        width_boxes[-1] += 1

        return zip(windows, icons, names, width_boxes)


def tasklist_parse_text(text):
    title_firefox = ' — Mozilla Firefox'
    title_firefox_private = title_firefox + ' Private Browsing'
    title_chromium = ' - Chromium'
    title_brave = " - Brave"
    title_browser = False
    if text.endswith(title_firefox):
        title_browser = True
        text = text[:-len(title_firefox)]
    elif text.endswith(title_firefox_private):
        title_browser = True
        text = 'Firefox'
    elif text.endswith(title_chromium):
        title_browser = True
        text = text[:-len(title_chromium)]
    elif text.endswith(title_brave):
        title_browser = True
        text = text[:-len(title_brave)]
    if title_browser:
        title_browser_max = 75
        if len(text) > title_browser_max:
            text = '%s…' % text[:title_browser_max - 2]
    return text


decoration = dict(
    decorations=[
        widget.decorations.RectDecoration(
            radius=5,
            line_colour=colors[0],
            line_width=1,
            padding_y=3,
            colour="66666689",
            filled=True
        )
    ],
    padding=10
)


widget_defaults = dict(
    font="DejaVu Sans",
    fontsize=12,
    padding=3,
    foreground=colors[3]
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(10),
                widget.Clock(
                    format="<span weight='bold'>%H:%M:%S</span> %d.%m.%y",
                    **decoration
                ),
                widget.Spacer(10),
                widget.DF(
                    partition="/home",
                    warn_space=75,
                    visible_on_warn=False,
                    format="{uf}{m}B",
                    **decoration
                ),
                widget.Spacer(10),
                widget.CurrentLayoutIcon(
                    custom_icon_paths=["/home/ole/.config/qtile/icons"],
                    use_mask=True
                ),
                widget.Spacer(10),
                BetterNvidiaSensors(
                    format_normal="🌡 {temp}C",
                    format_hovered="🌡 {fan_speed}",
                    foreground=colors[3]
                ),
                widget.Spacer(10),
                widget.Chord(),
                widget.Spacer(),
                widget.GroupBox(
                    margin_y=2,
                    borderwidth=6,
                    inactive=colors[3],
                    active=colors[2],
                    this_current_screen_border=colors[1],
                    highlight_method="text",
                    urgent_alert_method="text",
                    disable_drag=True,
                    toggle=False,
                    decorations=[
                        widget.decorations.RectDecoration(
                            radius=9,
                            line_colour=colors[0],
                            line_width=1,
                            padding_y=3,
                            colour="00000066",
                            filled=True
                        )
                    ]
                ),
                widget.Spacer(),
                Timer(fmt="<span weight='bold'>{}</span>"),
                widget.Spacer(10),
                widget.Systray(),
                widget.Spacer(10),
                widget.Volume(
                    volume_app="pavucontrol",
                    fmt="🔉 {}",
                    **decoration
                ),
                widget.Spacer(10),
                SmartExit(**decoration),
                widget.Spacer(10),
            ],
            26,
            background=colors[0]
        ),
        bottom=bar.Bar(
            [
                widget.Spacer(1),
                widget.Spacer(),
                DynamicTaskList(
                    highlight_method="block",
                    parse_text=tasklist_parse_text,
                    stretch=False,
                    background="00000066",
                    border="66666669",
                    rounded=True
                ),
                widget.Spacer(),
                widget.Spacer(1),
            ],
            26,
            background=colors[0]
        ),
        wallpaper="/home/ole/.local/share/backgrounds/unsplash/johannes-plenio-hvrpOmuMrAI-unsplash.jpg",
        wallpaper_mode="fill",
        x11_drag_polling_rate=75
    )]
