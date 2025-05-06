#Input directory where the files produced at the stage1 level are
inputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/stage1/dd/"

outputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/final/dd/"

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
    'IDEA_events_000421007': {},
    'CMS_Phase2_events_000421007': {},
    'CMS_Phase1_events_000421007': {},
}

###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    "IDEA_events_000421007":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 9.702e-9, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "CMS_Phase2_events_000421007":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 9.702e-9, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "CMS_Phase1_events_000421007":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 9.702e-9, "kfactor": 1.0, "matchingEfficiency": 1.0},
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
histoList = {
    ######## Monte-Carlo particles #######
    "n_GenDown":                  {"name":"n_GenDown",                  "title":"Number of gen Downs",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "GenDown_e":                  {"name":"GenDown_e",                  "title":"gen Downs energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "GenDown_p":                  {"name":"GenDown_p",                  "title":"gen Downs p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "GenDown_pt":                 {"name":"GenDown_pt",                 "title":"gen Downs p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "GenDown_px":                 {"name":"GenDown_px",                 "title":"gen Downs p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "GenDown_py":                 {"name":"GenDown_py",                 "title":"gen Downs p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "GenDown_pz":                 {"name":"GenDown_pz",                 "title":"gen Downs p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "GenDown_y":                  {"name":"GenDown_y",                  "title":"gen Downs rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "GenDown_eta":                {"name":"GenDown_eta",                "title":"gen Downs #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "GenDown_theta":              {"name":"GenDown_theta",              "title":"gen Downs #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "GenDown_phi":                {"name":"GenDown_phi",                "title":"gen Downs #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "GenDown_charge":             {"name":"GenDown_charge",             "title":"gen electrons charge",             "bin":3, "xmin":-1.5,"xmax":1.5},
    "GenDown_mass":               {"name":"GenDown_mass",               "title":"gen Downs mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},

    
    "n_TagJet_kt2":                  {"name":"n_TagJet_kt2",                  "title":"Number of Jets",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "TagJet_kt2_e":                   {"name":"TagJet_kt2_e",                   "title":"Jet energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "TagJet_kt2_p":                   {"name":"TagJet_kt2_p",                   "title":"Jet p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "TagJet_kt2_pt":                  {"name":"TagJet_kt2_pt",                  "title":"Jet p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "TagJet_kt2_px":                  {"name":"TagJet_kt2_px",                  "title":"Jet p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "TagJet_kt2_py":                  {"name":"TagJet_kt2_py",                  "title":"Jet p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "TagJet_kt2_pz":                  {"name":"TagJet_kt2_pz",                  "title":"Jet p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "TagJet_kt2_eta":                 {"name":"TagJet_kt2_eta",                 "title":"Jet #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "TagJet_kt2_theta":               {"name":"TagJet_kt2_theta",               "title":"Jet #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "TagJet_kt2_phi":                 {"name":"TagJet_kt2_phi",                 "title":"Jet #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "TagJet_kt2_charge":              {"name":"TagJet_kt2_charge",              "title":"Jet charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "TagJet_kt2_mass":                {"name":"TagJet_kt2_mass",                "title":"Jet mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},

    "Down_p_res_0_20":              {"name":"Down_p_res_0_20",              "title":"p_{reco}-p_{gen}/p_{gen} 0 < p_{gen} < 20 GeV", "bin":200, "xmin":-2., "xmax":2}, 
    "Down_p_res_20_40":             {"name":"Down_p_res_20_40",             "title":"p_{reco}-p_{gen}/p_{gen} 20 < p_{gen} < 40 GeV","bin":200, "xmin":-5, "xmax":15.},
    "Down_p_res_40_60":             {"name":"Down_p_res_40_60",             "title":"p_{reco}-p_{gen}/p_{gen} 40 < p_{gen} < 60 GeV","bin":200, "xmin":-20, "xmax":20},
    "Down_p_res_60_higher":         {"name":"Down_p_res_60_higher",         "title":"p_{reco}-p_{gen}/p_{gen} 60 GeV < p_{gen} ",    "bin":200, "xmin":-20, "xmax":20}, 
    "Down_p_res_total":             {"name":"Down_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":200, "xmin":-20, "xmax":20}, 
}