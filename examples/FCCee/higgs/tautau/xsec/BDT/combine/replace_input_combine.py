import shutil
import os

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
output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/combine/output_xsec_BDT.csv"
outputDir = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/combine/"

for cat in CAT:
    for sub in SUBDIR:

        file_read = f"{outputDir}/{cat}/{sub}/{input_file}"

        #get fit from subcategories
        os.system(f"text2workspace.py {outputDir}/{cat}/{sub}/datacard.txt -o {outputDir}/{cat}/{sub}/ws.root")
        os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/{cat}/{sub}/ws.root --rMin -2 >{file_read}")

        with open(file_read, "r") as file:
                read = False
                for line in file:
                    if "Best fit r:" in line:
                        content_of_row=line[11:]
                        read=True
                if read == False:
                    content_of_row='error'

        # Write the content of the selected row to the output CSV file
        with open(output_file, "a") as csv_file:
            csv_file.write(f"{cat}/{sub}: {content_of_row} \n")

        print("Content from {} has been written to {}".format(sub, output_file))

    input_file_dir = f"{outputDir}/{cat}/{input_file}"

    #now for the combined subcategories
    os.system(f"text2workspace.py {outputDir}/{cat}/datacard_{cat}.txt -o {outputDir}/{cat}/ws.root")
    os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/{cat}/ws.root --rMin -2 >{input_file_dir}")

    with open(input_file_dir, "r") as file:
            read = False
            for line in file:
                if "Best fit r:" in line:
                    content_of_row=line[11:]
                    read=True
            if read == False:
                content_of_row='error'

    # Write the content of the selected row to the output CSV file
    with open(output_file, "a") as csv_file:
        csv_file.write(f"{cat}: {content_of_row} \n")

    print("Content from {} has been written to {}".format(cat, output_file))

#final fit on everything
input_file_fin = f"{outputDir}/{input_file}"

os.system(f"text2workspace.py {outputDir}/datacard_combined.txt -o {outputDir}/ws.root")
os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/ws.root --rMin -2 >{input_file_fin}")

with open(input_file_fin, "r") as file:
        read = False
        for line in file:
            if "Best fit r:" in line:
                content_of_row=line[11:]
                read=True
        if read == False:
            content_of_row='error'

# Write the content of the selected row to the output CSV file
with open(output_file, "a") as csv_file:
    csv_file.write(f"combined: {content_of_row} \n")

print("Content from combined has been written to {}".format(output_file))
