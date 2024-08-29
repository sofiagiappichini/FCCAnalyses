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
output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/CP/combine/output_xsec.csv"
outputDir = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/CP/combine/"

for cat in CAT:
    for sub in SUBDIR:

        #get fit from subcategories
        os.system(f"text2workspace.py {outputDir}/{cat}/{sub}/datacard.txt -o {outputDir}/{cat}/{sub}/ws.root")
        os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/{cat}/{sub}/ws.root --rMin -2 >{outputDir}/{cat}/{sub}/{input_file}")

        with open(input_file, "r") as file:
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

    #now for the combined subcategories
    os.system(f"text2workspace.py {outputDir}/{cat}/datacard_{cat}.txt -o {outputDir}/{cat}/ws.root")
    os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/{cat}/ws.root --rMin -2 >{outputDir}/{cat}/{input_file}")

    with open(input_file, "r") as file:
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
os.system(f"text2workspace.py {outputDir}/datacard_combined.txt -o {outputDir}/ws.root")
os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/ws.root --rMin -2 >{outputDir}/{input_file}")

with open(input_file, "r") as file:
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
