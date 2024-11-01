import matplotlib.pyplot as plt
import pandas as pd

GRADE_COLORS = (
    "green",
    "limegreen",
    "greenyellow",
    "yellow",
    "orange",
    "orangered",
    "red",
)


def plt_bar(data_file, x, height, color):
    data = pd.read_csv(f"statistics/{data_file}.csv")
    bars = plt.bar(data.get(x), data.get(height), color=color)

    for bar in bars:
        yval = bar.get_height()
        percentage = "{:.1%}".format(yval / data.get(height).sum())
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            percentage,
            ha="center",
            va="bottom",
        )

    plt.xlabel(x)
    plt.ylabel(height)

    plt.savefig(f"images/{data_file}_bar.png")
    plt.clf()


plt_bar("grade_distribution", "Grade", "Count", GRADE_COLORS)
