import shutil
import os
import re

def process_content_of_row(content_of_row):
    # Use regex to find all numbers after "+/-"
    matches = re.findall(r"\+/-\s*([-+]?\d*\.?\d+)", content_of_row)

    if matches:
        # Convert all matches to float and multiply by 100
        results = [f"$\pm${float(num) * 100:.2f}" for num in matches]
        content_of_row = " | ".join(results)  # Join results with '|'
    else:
        content_of_row = "error"

    return content_of_row

def do_combine(outdir, file):

    for filename in os.listdir(outdir):
        if filename.startswith("datacard") and filename.endswith(".txt"):
            datacard = filename

    ## --PO 'map=bin/process:parameter', can be repeated the same parameter name for different processes (will be correlated into one r), first time it needs [starting_value,min,max]
    os.system(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel  --PO verbose  --PO  'map=.*/wzp6_ee_ZH_Htautau_ecm365:r_ZH[1,-1,2]' --PO 'map=.*/wzp6_ee_VBFnunu_Htautau_ecm365:r_VBF[1,-5,5]' {outdir}/{datacard} -o {outdir}/ws.root")
    os.system(f"combine -M MultiDimFit {outdir}/ws.root --cminDefaultMinimizerStrategy 0 -t -1 --expectSignal=1 -v 10 >{file}") ##  --robustFit 1

    with open(file, "r") as f:  # Avoid reusing 'file' as a variable name
        content_of_row = "error"
        content_of_row_VBF = "error"
        for line in f:
            if "r_ZH	  =" in line:
                content_of_row = line.strip()
            if "r_VBF	  =" in line:
                content_of_row_VBF = line.strip()

    return content_of_row + " | " + content_of_row_VBF

def do_combine_alt(outdir, file):

    for filename in os.listdir(outdir):
        if filename.startswith("datacard") and filename.endswith(".txt"):
            datacard = filename

    ## --PO 'map=bin/process:parameter', can be repeated the same parameter name for different processes (will be correlated into one r), first time it needs [starting_value,min,max]
    os.system(f"text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel  --PO verbose  --PO  'map=.*/wzp6_ee_ZH_Htautau_ecm365:r_ZH[1,-1,2]' --PO 'map=.*/wzp6_ee_VBFnunu_Htautau_ecm365:r_VBF[1,-5,5]' {outdir}/{datacard} -o {outdir}/ws.root")
    os.system(f"combine -M MultiDimFit {outdir}/ws.root -t -1 --expectSignal=1 -v 10 >{file}") ##  --robustFit 1

    with open(file, "r") as f:  # Avoid reusing 'file' as a variable name
        content_of_row = "error"
        content_of_row_VBF = "error"
        for line in f:
            if "r_ZH	  =" in line:
                content_of_row = line.strip()
            if "r_VBF	  =" in line:
                content_of_row_VBF = line.strip()

    return content_of_row + " | " + content_of_row_VBF

TAG = [
    "R5-explicit",
    "R5-tag",
    "ktN-explicit",
    "ktN-tag",
]
CAT = [
    "QQ",
    "LL",
    "NuNu",
]
SUBDIR = [
    'LL',
    'LH',
    'HH',
]

#load combine from CMSSW
os.system("source /cvmfs/cms.cern.ch/cmsset_default.sh")
os.system("cd /work/xzuo/combine_test/CMSSW_14_1_0_pre4/src/")
os.system("cmsenv")

input_file = "significance.txt"
outputDir = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/BDT/combine/"
output_file = outputDir + "output_xsec.csv"

tab = []

latex_table_header = """
\\begin{table}[h]
\\centering
\\begin{tabular}{|c|""" + "c|" * len(TAG) + """}
\\hline
""" + " & " + " & ".join(TAG) + """ \\\\
\\hline
"""

latex_table_footer = """
\\hline
\\end{tabular}
\\caption{Fit Results}
\\end{table}
"""

latex_table_content = latex_table_header

tab = []

for k, tag in enumerate(TAG):

    ele = []
    n_cat = []
    col = []
    #col.append(f"& {tag} ")

    for cat in CAT:
        for sub in SUBDIR:

            n_cat.append(f"{cat+sub} & ")

            dir = f"{outputDir}/{tag}/{cat}/{sub}/"

            file_read = f"{outputDir}/{tag}/{cat}/{sub}/{input_file}"

            #get fit from subcategories
            content_of_row = do_combine(dir, file_read)

            if "nan" in content_of_row:
                print("REPORCESSING")
                content_of_row = do_combine_alt(dir, file_read)

            # Write the content of the selected row to the output CSV file
            with open(output_file, "a") as csv_file:
                csv_file.write(f"{tag}/{cat}/{sub}: {content_of_row} \n")

            processed= process_content_of_row(content_of_row)
            ele.append(f"{processed} & ")

            print("Content from {} has been written to {}".format(cat+sub, output_file, content_of_row))

        input_file_dir = f"{outputDir}/{tag}/{cat}/{input_file}"
        cat_dir = f"{outputDir}/{tag}/{cat}/"

        #now for the combined subcategories
        n_cat.append(f"{cat} &")

        content_of_row = do_combine(cat_dir, input_file_dir)

        if "nan" in content_of_row:
            print("REPORCESSING")
            content_of_row = do_combine_alt(dir, file_read)

        # Write the content of the selected row to the output CSV file
        with open(output_file, "a") as csv_file:
            csv_file.write(f"{tag}/{cat}: {content_of_row} \n")

        print("Content from {} has been written to {}".format(cat, output_file))

        processed= process_content_of_row(content_of_row)
        ele.append(f"{processed} & ")

    for i in range(len(n_cat)):
        if k==0:
            col.append(n_cat[i]+ele[i])
        else:
            col.append(ele[i])

    #final fit on everything
    input_file_fin = f"{outputDir}/{tag}/{input_file}"
    dir_fin = f"{outputDir}/{tag}/"

    content_of_row = do_combine(dir_fin, input_file_fin)

    if "nan" in content_of_row:
        print("REPORCESSING")
        content_of_row = do_combine_alt(dir, file_read)

    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as csv_file:
        csv_file.write(f"{tag} combined: {content_of_row} \n\n")

    print("Content from combined has been written to {}".format(output_file))

    processed= process_content_of_row(content_of_row)

    if k==0:
        col.append(f"combined & {processed} & ")
    else:
        col.append(f"{processed} & ")
    
    if k == 0:
        for item in col:
            tab.append([item])
    else:
        for i, row in enumerate(tab):
            row.append(col[i])

for row in tab:
    latex_table_content += ' '.join([str(item) for item in row]) + ' \\\\ \hline \n'

latex_table_content += latex_table_footer

with open(outputDir + "output_table.txt", "w") as tex_file:
    tex_file.write(latex_table_content)
