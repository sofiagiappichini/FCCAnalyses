#Input directory where the files produced at the stage1 level are
inputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/stage1_res/tautau/"

outputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/final_res/tautau/"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 10.8e6 #pb^-1 #to be checked again for 240 gev

#Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = True

#Save event yields in a table (optional)
saveTabular = True

#Number of CPUs to use
#nCPUs = 6

#produces ROOT TTrees, default is False
doTree = False

processList = {
    'IDEA': {},
    'IDEA_CMS2': {},
    'IDEA_CMS2_2': {},
    'CMS_Phase2_events_000731799': {},
    'CMS_Phase1_events_000731799': {},
}

###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    "IDEA":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.002897, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'IDEA_CMS2': {"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.002897, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'IDEA_CMS2_2': {"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.002897, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "CMS_Phase2_events_000731799":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.002897, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "CMS_Phase1_events_000731799":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.002897, "kfactor": 1.0, "matchingEfficiency": 1.0},
}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### no selection, just builds the histograms, it will not be shown in the latex table
    "selReco": "true",
    #"selReco_100Coll150": "Collinear_mass>100 && Collinear_mass<150",
}

# Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well, it's only for the table ###
cutLabels = {
    "selReco": "No additional selection",
    #"selReco_100Coll150": "100<M_{collinear}<150 GeV",
}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {    ######## Reconstructed particles #######
                            
    "RecoH_px":                 {"name":"RecoH_px",                 "title":"Reco H p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "RecoH_py":                 {"name":"RecoH_py",                 "title":"Reco H p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "RecoH_pz":                 {"name":"RecoH_pz",                 "title":"Reco H p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "RecoH_p":                  {"name":"RecoH_p",                  "title":"Reco H p [GeV]",                "bin":75, "xmin":0 ,"xmax":150},
    "RecoH_pt":                 {"name":"RecoH_pt",                 "title":"Reco H p_{T} [GeV]",            "bin":75, "xmin":0 ,"xmax":150},
    "RecoH_e":                  {"name":"RecoH_e",                  "title":"Reco H energy [GeV]",           "bin":75, "xmin":0 ,"xmax":150},
    "RecoH_eta":                {"name":"RecoH_eta",                "title":"Reco H #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoH_phi":                {"name":"RecoH_phi",                "title":"Reco H #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoH_theta":              {"name":"RecoH_theta",              "title":"Reco H #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "RecoH_y":                  {"name":"RecoH_y",                  "title":"Reco H rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "RecoH_mass":               {"name":"RecoH_mass",               "title":"Reco H mass",                   "bin":75, "xmin":0 ,"xmax":150},

}