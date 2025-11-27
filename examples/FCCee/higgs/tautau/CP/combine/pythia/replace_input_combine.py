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

def do_combine(outdir):

    for filename in os.listdir(outdir):
        if filename.startswith("datacard") and filename.endswith(".txt"):
            datacard = filename

    ## instructions from the CP CMS model https://github.com/Ksavva1021/Combine_HtautauCP/tree/adding_mt
    os.system(f"combineTool.py -m 125 -M T2W -P CombineHarvester.Combine_HtautauCP.CPMixtureDecays:CPMixtureDecays -i {outdir}/{datacard} -o {outdir}/ws.root --parallel 8")
    os.system(f"combineTool.py -m 125 -M MultiDimFit --setParameters muV=1,alpha=0,muggH=1,mutautau=1 --setParameterRanges alpha=-90,90 --points 41 --redefineSignalPOIs alpha  -d {outdir}/ws.root --algo grid -t -1 --there -n .alpha --alignEdges 1 --freezeParameters lumiScale")
    os.system(f"cd {outdir}")
    os.system(f"python3 /afs/cern.ch/user/s/sgiappic/CMSSW_14_1_0_pre4/src/CombineHarvester/Combine_HtautauCP/scripts/plot1DScan.py --main={outdir}/higgsCombine.alpha.MultiDimFit.mH125.root --POI=alpha --output={outdir}/alpha_cmb --no-numbers --no-box --x-min=-90 --x-max=90 --y-max=8")

def get_alpha_sigma_from_file(filename="poi_value.txt"):
    alpha = None
    sigma_plus = None
    sigma_minus = None
    with open(filename, "r") as f:
        for line in f:
            if "Best fit:" in line:
                alpha = float(line.split(":")[1].strip())
            elif "+1 sigma:" in line:
                sigma_plus = float(line.split(":")[1].strip())
            elif "-1 sigma:" in line:
                sigma_minus = float(line.split(":")[1].strip())
    return alpha, sigma_plus, sigma_minus

TAG = [
    #"R5-explicit",
    #"R5-tag",
    #"ktN-explicit",
    #"ktN-tag",
    "",
]
CAT = [
    "QQ",
    "LL",
    #"NuNu",
]
SUBDIR = [
    #'LL',
    #'LH',
    'HH',
    #'HH_one',
    #'HH_not',
]

#load combine from CMSSW
#os.system("source /cvmfs/cms.cern.ch/cmsset_default.sh")
#os.system("cd /work/xzuo/combine_test/CMSSW_14_1_0_pre4/src/")
#os.system("cmsenv")

outputDir = "/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/CP/combine/pythia/251107_ILC/"
outdir_plot = "/eos/user/s/sgiappic/www/Higgs_CP/ecm240/pythia/"
output_file = outputDir + "/output_CP.csv"

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

ele = []
n_cat = []
col = []
#col.append(f"& {tag} ")

for cat in CAT:
    for sub in SUBDIR:

        n_cat.append(f"{cat+sub} & ")

        dir = f"{outputDir}/{cat}/{sub}/"

        #get fit from subcategories
        do_combine(dir)
        alpha, sigma_plus, sigma_minus = get_alpha_sigma_from_file(dir + "poi_value.txt")

        # Write the content of the selected row to the output CSV file
        with open(output_file, "a") as csv_file:
            csv_file.write(f"{cat}/{sub}: {alpha} +{sigma_plus} -{sigma_minus} \n")
            
        ele.append(f"{alpha} +{sigma_plus} -{sigma_minus} & ")

        print("Content from {} has been written to {}".format(cat+sub, output_file))

    cat_dir = f"{outputDir}/{cat}/"

    #now for the combined subcategories
    n_cat.append(f"{cat} &")

    #get fit from subcategories
    do_combine(cat_dir)
    alpha, sigma_plus, sigma_minus = get_alpha_sigma_from_file(cat_dir + "poi_value.txt")

    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as csv_file:
        csv_file.write(f"{cat}: {alpha} +{sigma_plus} -{sigma_minus} \n")
        
    ele.append(f"{alpha} +{sigma_plus} -{sigma_minus} & ")

    print("Content from {} has been written to {}".format(cat, output_file))

for i in range(len(n_cat)):
    col.append(n_cat[i]+ele[i])

#final fit on everything
dir_fin = f"{outputDir}/"

#get fit from subcategories
do_combine(dir_fin)
alpha, sigma_plus, sigma_minus = get_alpha_sigma_from_file(dir_fin + "poi_value.txt")

# Write the content of the selected row to the output CSV file
with open(output_file, "a") as csv_file:
    csv_file.write(f"combination: {alpha} +{sigma_plus} -{sigma_minus} \n")
    
ele.append(f"{alpha} +{sigma_plus} -{sigma_minus} & ")

print("Content from combined has been written to {}".format(output_file))

col.append(f"combined & {alpha} +{sigma_plus} -{sigma_minus}  & ")

for item in col:
    tab.append([item])

for row in tab:
    latex_table_content += ' '.join([str(item) for item in row]) + ' \\\\ \hline \n'

latex_table_content += latex_table_footer

with open(outputDir + "/output_table.txt", "w") as tex_file:
    tex_file.write(latex_table_content)