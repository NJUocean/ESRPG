import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.abspath(__file__))

files = [
    os.path.join(path,"gen_time", "CsmithEdge_fail.txt"),
    os.path.join(path,"gen_time", "CsmithEdge_succ.txt"),
]


all_data = pd.DataFrame()
for file in files:
    data_list = []
    with open(file, "r") as f:
        for line in f:
            parts = line.strip().split(" | ")
            data_list.append(float(parts[1]))
    df = pd.DataFrame(
        {
            "Generation Time": data_list,
            "Label": "CsmithEdge-fail" if "fail" in file else "CsmithEdge-succ",
        }
    )
    all_data = pd.concat([all_data, df])

for label in all_data["Label"].unique():
    data_result = all_data[all_data["Label"] == label]
    sns.kdeplot(data=data_result, x="Generation Time", label=label, linewidth=2, shade=False)

current_xlim = plt.xlim()
new_xlim = (current_xlim[0], 400)
plt.xlim(new_xlim)
plt.xlabel("Generation Time", fontsize=18)
plt.ylabel("Density", fontsize=18)
plt.tick_params(axis='both', labelsize=16)
plt.legend(fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(path,"Fig12b.pdf"), format="pdf")

