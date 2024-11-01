import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

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


def plt_barh_three(
    data_file, height, width, x, y, z, total_entries_file, height_text_substitution=[]
):
    custom_palette = ["#32CD32", "#FFA500", "#FF6347"]
    sns.set(style="white", palette=custom_palette)

    data = pd.read_csv(f"statistics/{data_file}.csv").sort_values(
        by="0", ascending=False
    )

    criteria = (
        data[height].map(height_text_substitution)
        if height_text_substitution
        else data[height]
    )
    count_0 = data[x].to_numpy()
    count_1 = data[y].to_numpy()
    count_2 = data[z].to_numpy()

    fig, ax = plt.subplots(figsize=(8, 6))

    bar_width = 0.8
    bar1 = plt.barh(criteria, count_0, height=bar_width, label=x)
    bar2 = plt.barh(
        criteria,
        count_1,
        height=bar_width,
        left=count_0,
        label=y,
    )
    bar3 = plt.barh(
        criteria,
        count_2,
        height=bar_width,
        left=np.array(count_0) + np.array(count_1),
        label=z,
    )

    shift = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for bars in [bar1, bar2, bar3]:
        for i, bar in enumerate(bars):
            bar_width = bar.get_width()
            plt.text(
                bar_width / 2 + shift[i],
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar_width)}",
                ha="center",
                va="center",
                fontsize=14,
                color="white",
                fontweight="bold",
            )
            shift[i] += bar_width

    plt.xlabel(width)
    plt.ylabel(height)

    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3)

    ax.invert_yaxis()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    with open(f"statistics/{total_entries_file}.txt", "r") as file:
        total_entries = int(file.read().strip())

    plt.xticks([0, total_entries])

    plt.tight_layout()
    plt.savefig(f"images/{data_file}_barh_stack.png")


plt_bar("grade_distribution", "Grade", "Count", GRADE_COLORS)

criteria_text = {
    "user_authentication_account_management": "Account Management Capabilities",
    "user_authentication_authentication": "Authentication Measures",
    "system_authentication_with_other_systems": "Authentication Measures with Other Systems",
    "user_authentication_brute_force_protection": "Brute-force Protection",
    "system_communications": "Communications' Level of Encryption",
    "device_known_hardware_tampering": "Documented Hardware Tampering",
    "device_known_vulnerabilties": "Documented Vulnerabilities",
    "user_authentication_event_logging": "Event Logging",
    "device_updatability": "Frequency of Software Updates",
    "user_authentication_passwords": "Password Change Requirements After Setup",
    "device_prior_attacks": "Prior History in IoT Attacks",
    "system_storage": "Storage's Level of Encryption",
}

plt_barh_three(
    "criteria_count", "Criterion", "Count", "0", "1", "2", "total_pages", criteria_text
)
