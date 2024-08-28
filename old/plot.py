import plotext as plt
import yfinance as yf

plt.date_form("d/m/Y")
start = plt.string_to_datetime("01/01/2023")
end = plt.today_datetime()
data = yf.download("SPY", start, end)
dates = plt.datetimes_to_string(data.index)

plt.clf()
plt.theme("dark")
plt.candlestick(dates, data)
plt.title("SPY Stock Price CandleSticks")

# plt.show()


from rich.console import Group
from rich.ansi import AnsiDecoder
from rich.panel import Panel
# import plotext as plt

# # Create some data
# x = [1, 2, 3, 4, 5]
# y = [10, 20, 25, 30, 40]

# # Plot the data
# plt.scatter(x, y)
# plt.title("Scatter Plot")
# plt.show()


from rich.console import Console
console = Console()

width, height = console.width-4, console.height-4 #console.size#
print(console.size)

plt.plotsize(width, height)


# Capture the plot as a string
plot_str = plt.build()


# Display the plot in a rich panel
renderable = Panel(Group(*AnsiDecoder().decode(plot_str)), title="My Scatter Plot")
console.print(renderable)
