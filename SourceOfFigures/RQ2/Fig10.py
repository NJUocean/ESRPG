import upsetplot as upset
import matplotlib.pyplot as plt
import os

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    compilers = ["gcc", "llvm"]
    fuzzers = ["Csmith", "CsmithEdge", "Csmith-HiCOND", "YARPGen", "YARPGen v.2"]
    upset_names = ["Fig10a", "Fig10b"]
    
    for i, compiler in enumerate(compilers):
        outname = upset_names[i]
        if compiler == "gcc":
            files = [
                "out_gcc_Csmith.txt",
                "out_gcc_CsmithEdge.txt",
                "out_gcc_Hicond.txt",
                "out_gcc_Yarpgen_v1.txt",
                "out_gcc_Yarpgen_v2.txt",
            ]
        else:
            files = [
                "out_llvm_Csmith.txt",
                "out_llvm_CsmithEdge.txt",
                "out_llvm_Hicond.txt",
                "out_llvm_Yarpgen_v1.txt",
                "out_llvm_Yarpgen_v2.txt",
            ]
        
        data = {}
        for j, file in enumerate(files):
            file_path = os.path.join(path, "covered_compiler_lines", file)
            try:
                with open(file_path, "r") as f:
                    elements = {line.strip() for line in f if line.strip()}  # Convert to set and remove empty lines
                data[fuzzers[j]] = elements
            except FileNotFoundError:
                print(f"Warning: File {file} not found. Skipping.")
                continue
        
        if not data:
            print(f"No data for {compiler}. Skipping plot.")
            continue
        
        upset_data = upset.from_contents(data)
        upset_obj = upset.UpSet(upset_data, subset_size='count', show_counts=True)
        
        plt.figure(figsize=(10, 6))
        upset_obj.plot()

        fig = plt.gcf()
        ax = fig.axes[3]
        ax.tick_params(axis='y', labelsize=12) 
        ax.set_ylabel('Intersection Size', fontsize=14)  

        plt.tight_layout()  
        output_path = os.path.join(path, f"{outname}.pdf")
        plt.savefig(output_path, format="pdf", bbox_inches='tight')
        plt.close()

if __name__ == "__main__":
    main()