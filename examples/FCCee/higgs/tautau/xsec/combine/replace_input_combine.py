import shutil
import os
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
output_file = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/combine/output_xsec.csv"
outputDir = "/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/combine/"

for tag in TAG:
    for cat in CAT:
        for sub in SUBDIR:

            file_read = f"{outputDir}/{tag}/{cat}/{sub}/{input_file}"

            #get fit from subcategories
            os.system(f"text2workspace.py {outputDir}/{tag}/{cat}/{sub}/datacard.txt -o {outputDir}/{tag}/{cat}/{sub}/ws.root")
            os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/{tag}/{cat}/{sub}/ws.root --rMin -2 >{file_read}")

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
                csv_file.write(f"{tag}/{cat}/{sub}: {content_of_row} \n")

            print("Content from {} has been written to {}".format(sub, output_file))

        input_file_dir = f"{outputDir}/{tag}/{cat}/{input_file}"

        #now for the combined subcategories
        os.system(f"text2workspace.py {outputDir}/{tag}/{cat}/datacard_{cat}.txt -o {outputDir}/{tag}/{cat}/ws.root")
        os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/{tag}/{cat}/ws.root --rMin -2 >{input_file_dir}")

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
            csv_file.write(f"{tag}/{cat}: {content_of_row} \n")

        print("Content from {} has been written to {}".format(cat, output_file))

    #final fit on everything
    input_file_fin = f"{outputDir}/{tag}/{input_file}"

    os.system(f"text2workspace.py {outputDir}/{tag}/datacard_combined.txt -o {outputDir}/{tag}/ws.root")
    os.system(f"combine -M FitDiagnostics -t -1 --expectSignal=1 {outputDir}/{tag}/ws.root --rMin -2 >{input_file_fin}")

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
        csv_file.write(f"{tag} combined: {content_of_row} \n\n")

    print("Content from combined has been written to {}".format(output_file))
