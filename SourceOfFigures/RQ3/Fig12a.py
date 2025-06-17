import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.abspath(__file__))
fuzzers = [
    "Csmith",
    "Hicond",
]
labels = ["Csmith", "Csmith-HiCOND"]
files = [os.path.join(path,"gen_time", fz + "_succ.txt") for fz in fuzzers]

for i in range(len(files)):
    file = files[i]
    fz = fuzzers[i]
    data_list = []
    with open(file, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")
            data_list.append(float(parts[1]))
    df = pd.DataFrame({"Generation Time": data_list})
    sns.kdeplot(data=df, x="Generation Time", label=labels[i], linewidth=2, shade=False)

plt.xlabel("Generation Time", fontsize=18)
plt.ylabel("Density", fontsize=18)
plt.tick_params(axis='both', labelsize=16)
plt.legend(fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(path,"Fig12a.pdf"), format="pdf")
