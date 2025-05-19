import ROOT
import os

DIRECTORIES = [
    #"/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/R5-explicit/",
    #"/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/R5-tag/",
    "/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit-new/",
    "/afs/cern.ch/user/s/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag-new/",
]
SUBDIR = [
    'LL',
    'LH',
    'HH',
]
#category to plot
CAT = [
    "QQ",
    "LL",
    "NuNu",
]

for dir in DIRECTORIES:
    for cat in CAT:

        directory = dir + cat
        print(f"Directory {directory}")

        for sub in SUBDIR:

            os.system(f"fccanalysis run {directory}/analysis_stage2_{cat}{sub}.py")
            print(f"Executed {cat}{sub}")        