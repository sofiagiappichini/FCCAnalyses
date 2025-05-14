#Input directory where the files produced at the stage1 level are
inputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/stage1_res/ee/"

outputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/final_res/ee/"

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
    'IDEA_events_041153094': {},
    'IDEA_CMS2': {},
    'IDEA_CMS1': {},
    'CMS_Phase2_events_041153094': {},
    'CMS_Phase1_events_041153094': {},
}

###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    "IDEA_events_041153094":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 1.28e-5, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "IDEA_CMS2":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 1.28e-5, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "IDEA_CMS1":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 1.28e-5, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "CMS_Phase2_events_041153094":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 1.28e-5, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "CMS_Phase1_events_041153094":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 1.28e-5, "kfactor": 1.0, "matchingEfficiency": 1.0},
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
    "n_FSGenElectron":                  {"name":"n_FSGenElectron",                  "title":"Number of final state gen electrons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenElectron_e":                  {"name":"FSGenElectron_e",                  "title":"Final state gen electrons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_p":                  {"name":"FSGenElectron_p",                  "title":"Final state gen electrons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_pt":                 {"name":"FSGenElectron_pt",                 "title":"Final state gen electrons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_px":                 {"name":"FSGenElectron_px",                 "title":"Final state gen electrons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_py":                 {"name":"FSGenElectron_py",                 "title":"Final state gen electrons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_pz":                 {"name":"FSGenElectron_pz",                 "title":"Final state gen electrons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_y":                  {"name":"FSGenElectron_y",                  "title":"Final state gen electrons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenElectron_eta":                {"name":"FSGenElectron_eta",                "title":"Final state gen electrons #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenElectron_theta":              {"name":"FSGenElectron_theta",              "title":"Final state gen electrons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenElectron_phi":                {"name":"FSGenElectron_phi",                "title":"Final state gen electrons #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenElectron_charge":             {"name":"FSGenElectron_charge",             "title":"Final state gen electrons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSGenElectron_mass":               {"name":"FSGenElectron_mass",               "title":"Final state gen electrons mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},

    "n_FSGenMuon":                      {"name":"n_FSGenMuon",                  "title":"Number of final state gen muons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenMuon_e":                      {"name":"FSGenMuon_e",                  "title":"Final state gen muons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenMuon_p":                      {"name":"FSGenMuon_p",                  "title":"Final state gen muons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenMuon_pt":                     {"name":"FSGenMuon_pt",                 "title":"Final state gen muons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenMuon_px":                     {"name":"FSGenMuon_px",                 "title":"Final state gen muons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenMuon_py":                     {"name":"FSGenMuon_py",                 "title":"Final state gen muons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenMuon_pz":                     {"name":"FSGenMuon_pz",                 "title":"Final state gen muons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenMuon_y":                      {"name":"FSGenMuon_y",                  "title":"Final state gen muons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenMuon_eta":                    {"name":"FSGenMuon_eta",                "title":"Final state gen muons #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenMuon_theta":                  {"name":"FSGenMuon_theta",              "title":"Final state gen muons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenMuon_phi":                    {"name":"FSGenMuon_phi",                "title":"Final state gen muons #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenMuon_charge":                 {"name":"FSGenMuon_charge",             "title":"Final state gen muons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSGenMuon_mass":                   {"name":"FSGenMuon_mass",               "title":"Final state gen muons mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},

    "n_FSGenPhoton":                    {"name":"n_FSGenPhoton",                  "title":"Number of final state gen photons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenPhoton_e":                    {"name":"FSGenPhoton_e",                  "title":"Final state gen photons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenPhoton_p":                    {"name":"FSGenPhoton_p",                  "title":"Final state gen photons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenPhoton_pt":                   {"name":"FSGenPhoton_pt",                 "title":"Final state gen photons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenPhoton_px":                   {"name":"FSGenPhoton_px",                 "title":"Final state gen photons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenPhoton_py":                   {"name":"FSGenPhoton_py",                 "title":"Final state gen photons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenPhoton_pz":                   {"name":"FSGenPhoton_pz",                 "title":"Final state gen photons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenPhoton_y":                    {"name":"FSGenPhoton_y",                  "title":"Final state gen photons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenPhoton_eta":                  {"name":"FSGenPhoton_eta",                "title":"Final state gen photons #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenPhoton_theta":                {"name":"FSGenPhoton_theta",              "title":"Final state gen photons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenPhoton_phi":                  {"name":"FSGenPhoton_phi",                "title":"Final state gen photons #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenPhoton_charge":               {"name":"FSGenPhoton_charge",             "title":"Final state gen photons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},

    ######## Reconstructed particles #######

    "n_RecoElectrons":                  {"name":"n_RecoElectrons",                  "title":"Number of reco electrons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoElectron_e":                   {"name":"RecoElectron_e",                   "title":"Reco electron energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_p":                   {"name":"RecoElectron_p",                   "title":"Reco electron p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_pt":                  {"name":"RecoElectron_pt",                  "title":"Reco electron p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoElectron_px":                  {"name":"RecoElectron_px",                  "title":"Reco electron p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_py":                  {"name":"RecoElectron_py",                  "title":"Reco electron p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_pz":                  {"name":"RecoElectron_pz",                  "title":"Reco electron p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoElectron_y":                   {"name":"RecoElectron_y",                   "title":"Reco electron rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoElectron_eta":                 {"name":"RecoElectron_eta",                 "title":"Reco electron #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_theta":               {"name":"RecoElectron_theta",               "title":"Reco electron #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoElectron_phi":                 {"name":"RecoElectron_phi",                 "title":"Reco electron #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoElectron_charge":              {"name":"RecoElectron_charge",              "title":"Reco electron charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoElectron_mass":                {"name":"RecoElectron_mass",                "title":"Reco electron mass [GeV]",                     "bin":100, "xmin":0.000509999, "xmax":0.000511999},
    #"Electron_p_res_0_20":              {"name":"Electron_p_res_0_20",              "title":"Momentum resolution 0 < p_{gen} < 20 GeV", "bin":200, "xmin":-0.08, "xmax":0.08}, 
    #"Electron_p_res_20_40":             {"name":"Electron_p_res_20_40",             "title":"Momentum resolution 20 < p_{gen} < 40 GeV","bin":200, "xmin":-0.08, "xmax":0.08},
    #"Electron_p_res_40_60":             {"name":"Electron_p_res_40_60",             "title":"Momentum resolution 40 < p_{gen} < 60 GeV","bin":200, "xmin":-0.08, "xmax":0.08},
    #"Electron_p_res_60_higher":         {"name":"Electron_p_res_60_higher",         "title":"Momentum resolution 60 GeV < p_{gen} ",    "bin":200, "xmin":-0.08, "xmax":0.08}, 
    "Electron_p_res_total":             {"name":"Electron_p_res_total",             "title":"Momentum resolution",    "bin":2000, "xmin":-0.2, "xmax":0.2}, 

    "n_RecoMuons":                  {"name":"n_RecoMuons",                  "title":"Number of reco muons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoMuon_e":                   {"name":"RecoMuon_e",                   "title":"Reco muon energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_p":                   {"name":"RecoMuon_p",                   "title":"Reco muon p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_pt":                  {"name":"RecoMuon_pt",                  "title":"Reco muon p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoMuon_px":                  {"name":"RecoMuon_px",                  "title":"Reco muon p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_py":                  {"name":"RecoMuon_py",                  "title":"Reco muon p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_pz":                  {"name":"RecoMuon_pz",                  "title":"Reco muon p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoMuon_y":                   {"name":"RecoMuon_y",                   "title":"Reco muon rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoMuon_eta":                 {"name":"RecoMuon_eta",                 "title":"Reco muon #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_theta":               {"name":"RecoMuon_theta",               "title":"Reco muon #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoMuon_phi":                 {"name":"RecoMuon_phi",                 "title":"Reco muon #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoMuon_charge":              {"name":"RecoMuon_charge",              "title":"Reco muon charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoMuon_mass":                {"name":"RecoMuon_mass",                "title":"Reco muon mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},

    "n_RecoPhotons":            {"name":"n_RecoPhotons",                  "title":"Number of reco photons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
    "RecoPhoton_e":             {"name":"RecoPhoton_e",                   "title":"Reco photon energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_p":             {"name":"RecoPhoton_p",                   "title":"Reco photon p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_pt":            {"name":"RecoPhoton_pt",                  "title":"Reco photon p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
    "RecoPhoton_px":            {"name":"RecoPhoton_px",                  "title":"Reco photon p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_py":            {"name":"RecoPhoton_py",                  "title":"Reco photon p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_pz":            {"name":"RecoPhoton_pz",                  "title":"Reco photon p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
    "RecoPhoton_y":             {"name":"RecoPhoton_y",                   "title":"Reco photon rapidity",                       "bin":40, "xmin":-4., "xmax":4.},
    "RecoPhoton_eta":           {"name":"RecoPhoton_eta",                 "title":"Reco photon #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_theta":         {"name":"RecoPhoton_theta",               "title":"Reco photon #theta",                         "bin":16, "xmin":0,"xmax":3.2},
    "RecoPhoton_phi":           {"name":"RecoPhoton_phi",                 "title":"Reco photon #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
    "RecoPhoton_charge":        {"name":"RecoPhoton_charge",              "title":"Reco photon charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
    "RecoPhoton_mass":          {"name":"RecoPhoton_mass",                 "title":"Reco photon mass [GeV]",                         "bin":50, "xmin":-0.05,"xmax":0.05},
}