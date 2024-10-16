from libqtile import layout
from libqtile.backend.base import Window
from libqtile.config import ScreenRect
from libqtile.log_utils import logger

import math

from color import window_border, window_border_fixed


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


class Plasma(layout.Plasma):
    def swap(self, c1: Window, c2: Window) -> None:
        node_c1 = node_c2 = None
        for leaf in self.root.all_leafs:
            if leaf.payload is not None:
                if c1.wid == leaf.payload.wid:
                    node_c1 = leaf
                elif c2.wid == leaf.payload.wid:
                    node_c2 = leaf
            if node_c1 is not None and node_c2 is not None:
                node_c1.payload, node_c2.payload = node_c2.payload, node_c1.payload
                return


layouts = [
    Plasma(
        margin=[10, 20, 10, 20],
        **window_border,
        **window_border_fixed
    ),
    layout.Max(
        margin=[10, 20, 10, 20],
    ),
]
