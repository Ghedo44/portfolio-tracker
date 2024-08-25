from rich.layout import Layout
from rich.live import Live
from rich.ansi import AnsiDecoder
from rich.console import Group
from rich.jupyter import JupyterMixin
from rich.panel import Panel
from rich.text import Text
import plotext as plt

def make_plot(width, height, phase = 0, title = None):
    plt.clf()
    l, frames = 1000, 30
    x = range(1, l + 1)
    y = plt.sin(periods = 2, length = l, phase = 2 * phase  / frames)
    plt.scatter(x, y, marker = "fhd")
    plt.plotsize(width, height)
    plt.xaxes(0, "upper")
    plt.yaxes(0, "right")
    plt.title(title)
    #color = 255
    #plt.canvas_color(color)
    #plt.axes_color(color)
    #plt.cls()
    return plt.build()

class plotextMixin(JupyterMixin):
    def __init__(self, phase = 0, title = None):
        self.decoder = AnsiDecoder()
        self.phase = phase
        self.title = title
        
    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = make_plot(self.width, self.height, self.phase, self.title)
        self.rich_canvas = Group(*self.decoder.decode(canvas))
        yield self.rich_canvas

def make_layout():
    layout = Layout(name = "root")
    layout.split(Layout(name = "header", size = 3), Layout(name="main", ratio = 1))
    layout["main"].split_column(
        Layout(name = "static", ratio = 1),
        Layout(name = "dynamic"))
    return layout

layout = make_layout()

header = layout['header']
title = plt.colorize("Pl✺ ", "cyan bold") + plt.colorize("text ", "dim bold") + "integration with " + plt.colorize("rich_", "bold dim")
spaces = (plt.terminal_size()[0] - len(plt.uncolorize(title))) // 2
header.update(Text("\n" + " " * spaces + title))

static = layout["static"]
dynamic = layout["dynamic"]

mixin_static = plotextMixin(title = "Static Plot")
mixin_static_panel = Panel(mixin_static)
static.update(mixin_static_panel)

# mixin_dynamic = plotextMixin(title = "Dynamic Plot")
# mixin_dynamic_panel = Panel(mixin_dynamic)

# with Live(layout, refresh_per_second = 0.0001) as live:
#     while True:
#         mixin_dynamic.phase += 1
#         dynamic.update(mixin_dynamic_panel)
#         live.refresh()