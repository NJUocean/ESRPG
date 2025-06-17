import matplotlib.pyplot as plt
import os

def count_intervals(file_path, counts):
    with open(file_path, "r") as file:
        for line in file:
            try:
                value = float(line.strip())
                if value < 500:
                    counts["<0.5"] += 1
                elif 500 <= value < 1000:
                    counts["0.5-1"] += 1
                elif 1000 <= value < 1500:
                    counts["1-1.5"] += 1
                elif 1500 <= value < 2000:
                    counts["1.5-2"] += 1
                elif 2000 <= value < 5000:
                    counts["2-5"] += 1
                elif 5000 <= value < 10000:
                    counts["5-10"] += 1
                else:
                    counts[">10"] += 1
            except ValueError:
                print(
                    f"Warning: Line '{line.strip()}' is not a valid number and will be skipped."
                )


def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=18,
        )


def plot_histogram(i, gcc_counts, llvm_counts, figsize=(10, 5)):
    plt.clf()
    plt.figure(figsize=figsize)

    bar_width = 0.44

    indices = range(len(intervals))
    gcc_bars = plt.bar(
        indices, list(gcc_counts.values()), width=bar_width, label="GCC", align="center"
    )
    llvm_bars = plt.bar(
        [i + bar_width for i in indices],
        list(llvm_counts.values()),
        width=bar_width,
        label="LLVM",
        align="center",
    )
    plt.legend(fontsize=22)
    plt.xticks([i + bar_width / 2 for i in indices], intervals)
    plt.tick_params(axis='both', labelsize=22)
    plt.xlabel("Time Intervals", fontsize=26)
    plt.ylabel("Counts", fontsize=26)
    # plt.title(realname[i], fontsize=18)
    
    plt.ylim(0, 1000)
    add_labels(gcc_bars + llvm_bars)  

    plt.tight_layout()
    plt.savefig(
        os.path.join(path, f"Fig7{subindex[i]}.pdf"), format="pdf"
    )
    # plt.show()



def main():
    default_figsize = (10, 6)
    for i in range(len(fuzzers)):
        fz = fuzzers[i]
        gcc_counts = {interval: 0 for interval in intervals}
        llvm_counts = {interval: 0 for interval in intervals}
        gcc_file_path = os.path.join(path, "cpl_time", f"{fz}_gcc.txt")
        llvm_file_path = os.path.join(path, "cpl_time", f"{fz}_llvm.txt")
        count_intervals(gcc_file_path, gcc_counts)
        count_intervals(llvm_file_path, llvm_counts)
        plot_histogram(i, gcc_counts, llvm_counts, figsize=default_figsize)


fuzzers = ["Csmith", "CsmithEdge", "Hicond", "Yarpgen_v1", "Yarpgen_v2"]
realname = [
    "Csmith",
    "CsmithEdge",
    "Csmith-HiCOND",
    "YARPGen",
    "YARPGen v.2",
]
intervals = [
    "<0.5",
    "0.5-1",
    "1-1.5",
    "1.5-2",
    "2-5",
    "5-10",
    ">10",
]
subindex=["a","b","c","d","e"]
path = os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    main()
