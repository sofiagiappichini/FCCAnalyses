import shutil
import os
import re

def process_content_of_row(content_of_row):

    result_min = ""
    result_plus = ""
    read_p = False
    read_m = False

    for n,i in enumerate(content_of_row):
        if i in "-+":
            if i=="-":
                if "/" in content_of_row[n+1:n+7]:
                    continue
                result_min=float(content_of_row[n+1:n+7])*100
                read_m = True

            if i=="+":
                if "(" in content_of_row[n+1:n+7]:
                    print("ERROR in +")
                    continue
                result_plus=float(content_of_row[n+1:n+7])*100
                read_p = True

    if read_m and read_p:
        #return f"\\substack{{^{+{result_plus}}}_{{-{negative_error}}}}"
        content_of_row = f"-{result_min:.2f}, +{result_plus:.2f}"

    else:
        content_of_row = 'error'
    
    return content_of_row

def do_combine(outdir, file):

    for filename in os.listdir(outdir):
        if filename.startswith("datacard") and filename.endswith(".txt"):
            datacard = filename

    os.system(f"text2workspace.py {outdir}/{datacard} -o {outdir}/ws.root")
    os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outdir}/ws.root --rMin -10  --cminDefaultMinimizerStrategy 0 --robustFit 1 >{file}")

    with open(file, "r") as file:
            read = False
            for line in file:
                if "Best fit r:" in line:
                    content_of_row=line[11:]
                    read=True
            if read == False:
                content_of_row='error'

    return content_of_row

def do_combine_alt(outdir, file):

    for filename in os.listdir(outdir):
        if filename.startswith("datacard") and filename.endswith(".txt"):
            datacard = filename

    os.system(f"text2workspace.py {outdir}/{datacard} -o {outdir}/ws.root")
    os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outdir}/ws.root --rMin -10  --cminDefaultMinimizerStrategy 0 >{file}")

    with open(file, "r") as file:
            read = False
            for line in file:
                if "Best fit r:" in line:
                    content_of_row=line[11:]
                    read=True
            if read == False:
                content_of_row='error'

    print(content_of_row)

    return content_of_row

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
outputDir = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/combine/"
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
            processed= process_content_of_row(content_of_row)

            if processed == 'error':
                print("REPORCESSING")
                content_of_row = do_combine_alt(dir, file_read)

            # Write the content of the selected row to the output CSV file
            with open(output_file, "a") as csv_file:
                csv_file.write(f"{tag}/{cat}/{sub}: {content_of_row} \n")

            processed= process_content_of_row(content_of_row)
            ele.append(f"{processed} & ")

            print("Content from {} has been written to {}".format(cat+sub, output_file))

        input_file_dir = f"{outputDir}/{tag}/{cat}/{input_file}"
        cat_dir = f"{outputDir}/{tag}/{cat}/"

        #now for the combined subcategories
        n_cat.append(f"{cat} &")

        content_of_row = do_combine(cat_dir, input_file_dir)
        processed = process_content_of_row(content_of_row)

        if processed == 'error':
            print("REPORCESSING")
            content_of_row = do_combine_alt(cat_dir, input_file_dir)

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
    processed= process_content_of_row(content_of_row)

    if processed == 'error':
        print("REPORCESSING")
        content_of_row = do_combine_alt(dir_fin, input_file_fin)

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