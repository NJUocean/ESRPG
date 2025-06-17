import matplotlib.pyplot as plt
import numpy as np
import re
import os


def parse_log_file(file_path, key):
    pattern = re.compile(r"Functions Coverage: .+?, (\d+)/(\d+)")
    line_pattern = re.compile(r"Lines Coverage: .+?, (\d+)/(\d+)")
    with open(file_path, "r") as file:
        for line in file:
            match = pattern.search(line)
            if match and key == "functions":
                return int(match.group(1))
            line_match = line_pattern.search(line)
            if line_match and key == "lines":
                return int(line_match.group(1))
    return None


def plot_coverage(data, ylabel, outname):

    plt.figure(figsize=(10, 6))

    linewidth = 2.0
    plt.plot(x, data[0], "g-.", label=fuzzers[0], linewidth=linewidth) 
    plt.plot(x, data[1], "b-", label=fuzzers[1], linewidth=linewidth)
    plt.plot(x, data[2], "r--", label=fuzzers[2], linewidth=linewidth)
    plt.plot(x, data[3], "m:", label=fuzzers[3], linewidth=linewidth)
    plt.plot(x, data[4], "c-", label=fuzzers[4], linewidth=linewidth)

    if outname == fig_line_name[0]: 
        plt.legend(fontsize=16)

    plt.xlabel("#Test Programs", fontsize=24, fontweight="bold")
    plt.ylabel(ylabel, fontsize=24, fontweight="bold")

    plt.xticks(x[1::2])
    plt.tick_params(axis='both', labelsize=18)

    plt.tight_layout()

    plt.savefig(os.path.join(basepath, outname + ".pdf"), format="pdf")

    # plt.show()
    plt.close()


def get_data(directory):
    function_coverages = []
    line_coverages = []
    for subdir, dirs, files in os.walk(directory):
        for log_file in range(20):
            log_file_name = f"{log_file}.log"
            if log_file_name in files:
                log_file_path = os.path.join(subdir, log_file_name)
                function_coverage = parse_log_file(log_file_path, "functions")
                line_coverage = parse_log_file(log_file_path, "lines")
                if function_coverage is not None:
                    function_coverages.append(function_coverage)
                if line_coverage is not None:
                    line_coverages.append(line_coverage)
    return function_coverages, line_coverages


x = list(range(500, 10500, 500))
basepath = os.path.dirname(os.path.abspath(__file__))
fuzzersFold = ["Csmith", "CsmithEdge", "Hicond", "Yarpgen_v1", "Yarpgen_v2"]
fuzzers = ["Csmith", "CsmithEdge", "Csmith-HiCOND", "YARPgen", "YARPgen v.2"]
compilers = ["gcc", "llvm"]
fig_line_name = ["Fig9a", "Fig9b"]
def main():
    for i in range(len(compilers)):
        yl = [[] for _ in range(5)]
        yf = [[] for _ in range(5)]
        compiler = compilers[i]
        for j in range(len(fuzzers)):
            fz = fuzzersFold[j]
            folder_path = os.path.join(basepath, "compiler_cov", compiler, fz)
            yf[j], yl[j] = get_data(folder_path)

        plot_coverage(yl, "#Covered Lines", fig_line_name[i])

if __name__ == "__main__":
    main()