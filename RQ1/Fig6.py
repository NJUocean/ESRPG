import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import random


def load_data(file_path):
    """Load the Excel file into a DataFrame."""
    return pd.read_excel(file_path)


def calculate_common_columns(dataframes):
    """Calculate the common columns among all DataFrames."""
    common_columns = set(dataframes[0].columns)
    for df in dataframes[1:]:
        common_columns &= set(df.columns)
    return list(common_columns)


fuzzers = ["Csmith", "CsmithEdge", "Hicond", "Yarpgen_v1", "Yarpgen_v2"]
path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(path, "metrics")
items = ["Cov_Percent"]

labels = [
    "Csmith",
    "CsmithEdge",
    "Csmith-HiCOND",
    "Y-func",
    "Y-driver",
    "Y2-func",
    "Y2-driver"
]

colors = [
 [0.03892374631199824, 0.22215416638333962, 0.2146292097999376], 
 [0.10544235879053843, 0.41220704827933863, 0.08283568783823614],
 [0.27139496542521246, 0.731897287195613, 0.03294509132892931],
 [0.46519565887206316, 0.4066007122761941, 0.9901784114492592],
 [0.21128199410199222, 0.27842456002264304, 0.9519047964109129],
 [0.6786347190644018, 0.40647669953174037, 0.6293543349959105],
 [0.136798093648127, 0.6961856471716872, 0.811341910113077],
 ]


def main():
    datas = []
    # Load data
    for fz in fuzzers:
        if not fz.startswith("Yarpgen"):
            file_path = os.path.join(data_path, fz + "_stat.xlsx")
            data = load_data(file_path)
            datas.append(data)
        else:
            file_path1 = os.path.join(data_path, fz + "_func_stat.xlsx")
            data1 = load_data(file_path1)
            file_path2 = os.path.join(data_path, fz + "_driver_stat.xlsx")
            data2 = load_data(file_path2)
            datas.append(data1)
            datas.append(data2)

    for i in range(len(items)):
        name = items[i]
        data = []

        for d in datas:
            data.append(d[name].values)

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_alpha(0)
        positions = np.arange(1, len(data) * 3 + 1, 3)
        vp_parts = ax.violinplot(data, positions=positions, showmeans=False, showmedians=True, widths=2.0)


        for i, pc in enumerate(vp_parts["bodies"]):
            pc.set_facecolor(colors[i % len(colors)])

        for line in ["cmeans", "cmins", "cbars", "cmedians", "cmaxes"]:
            if line in vp_parts.keys():
                vp_parts[line].set_color((0, 0, 0, 0))

        # plot
        bp_parts = ax.boxplot(
            data,
            positions=positions,
            widths=1,
            patch_artist=True,
            showfliers=False,
        )
        for box in bp_parts["boxes"]:
            box.set(facecolor="none", edgecolor="black")
        for median in bp_parts["medians"]:
            median.set(color="black", linewidth=1.5)

        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=-15,fontsize=12)
        ax.set_yticklabels(ax.get_yticks(), fontsize=12)

        ax.yaxis.grid(True, linestyle="--", alpha=0.7)

        plt.tight_layout()
        plt.savefig(os.path.join(path,"Fig6.pdf"), format="pdf")



if __name__ == "__main__":
    main()
