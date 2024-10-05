from libqtile import layout
from libqtile.backend.base import Window
from libqtile.config import ScreenRect, Bar
from libqtile.log_utils import logger

import math

from color import window_border


class BetterBsp(layout.Bsp):
    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults([("inner_margin", 0)])

    def configure(self, client: Window, screen_rect: ScreenRect) -> None:
        self.root.calc_geom(screen_rect.x, screen_rect.y, screen_rect.width, screen_rect.height)
        node = self.get_node(client)
        color = self.border_focus if client.has_focus else self.border_normal
        border = 0 if node is self.root and not self.border_on_single else self.border_width
        margin = self.margin_on_single if node is self.root else self.margin
        if type(margin) is not list:
            margin = [margin, margin, margin, margin]
        else:
            margin = margin.copy()
        if node is not None:
            bar_top: Bar = self.group.screen.top

            if node.y != bar_top.height:  # not north
                margin[0] = self.inner_margin
            if node.x + node.w != screen_rect.width:  # not east
                margin[1] = self.inner_margin
            if node.y + node.h != screen_rect.height + bar_top.height:  # not south
                margin[2] = self.inner_margin
            if node.x != 0:  # not west
                margin[3] = self.inner_margin

            client.place(
                node.x,
                node.y,
                node.w - 2 * border,
                node.h - 2 * border,
                border,
                color,
                margin=margin,
            )
        client.unhide()


class GridSelect(layout.Matrix):
    defaults = [
        ("border_width", 1, "Border width."),
        ("margin_focused", 15, "Margin width for focused windows"),
        ("margin_unfocused", 25, "Margin width for unfocused windows")
    ]

    def __init__(self, **config):
        layout.Matrix.__init__(self, **config)
        self.add_defaults(GridSelect.defaults)

    def configure(self, client: Window, screen_rect: ScreenRect) -> None:
        columns = max(math.ceil(math.sqrt(len(self.clients))), 2)
        if client not in self.clients:
            return
        idx = self.clients.index(client)
        row = idx // columns
        col = idx % columns
        px = self.border_focus if client.has_focus else self.border_normal
        # calculate position and size
        column_width = int(screen_rect.width / float(columns))
        row_height = int(screen_rect.height / float(columns))
        xoffset = screen_rect.x + col * column_width
        yoffset = screen_rect.y + row * row_height
        win_width = column_width - 2 * self.border_width
        win_height = row_height - 2 * self.border_width
        margin = self.margin_focused if client.has_focus else self.margin_unfocused
        # place
        client.place(
            xoffset,
            yoffset,
            win_width,
            win_height,
            self.border_width,
            px,
            margin=margin,
        )
        client.unhide()


layouts = [
    BetterBsp(
        margin=[0, 26, 0, 26],
        inner_margin=13,
        wrap_clients=True,
        **window_border
    ),
    layout.Max(
        margin=[0, 26, 0, 26],
        **window_border
    )
]
