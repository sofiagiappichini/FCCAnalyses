#Input directory where the files produced at the stage1 level are
inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/gen_stage1_250604/"

#Optional: output directory, default is local running directory
outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/gen_final_250604/"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 10.8e6 #pb^-1 #to be checked again for 240 gev

#Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = True

#Save event yields in a table (optional)
saveTabular = True

#Number of CPUs to use
nCPUS = 4

#produces ROOT TTrees, default is False
doTree = False

#Mandatory: List of processes
processList = {
    "mg_ee_eetata_ecm240":{},
    "mg_ee_eetata_smeft_cehim_m1_ecm240":{},
    "mg_ee_eetata_smeft_cehim_p1_ecm240":{},
    "mg_ee_eetata_smeft_cehre_m1_ecm240":{},
    "mg_ee_eetata_smeft_cehre_p1_ecm240":{},
    "mg_ee_jjtata_ecm240":{'chunks':10},
    "mg_ee_jjtata_smeft_cehim_m1_ecm240":{'chunks':10},
    "mg_ee_jjtata_smeft_cehim_p1_ecm240":{'chunks':10},
    "mg_ee_jjtata_smeft_cehre_m1_ecm240":{'chunks':10},
    "mg_ee_jjtata_smeft_cehre_p1_ecm240":{'chunks':10},
    "mg_ee_mumutata_ecm240":{},
    "mg_ee_mumutata_smeft_cehim_m1_ecm240":{},
    "mg_ee_mumutata_smeft_cehim_p1_ecm240":{},
    "mg_ee_mumutata_smeft_cehre_m1_ecm240":{},
    "mg_ee_mumutata_smeft_cehre_p1_ecm240":{},
    }
###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {

    'mg_ee_eetata_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.0003949209283230132, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_eetata_smeft_cehim_m1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.00039496700612440505, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_eetata_smeft_cehim_p1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.00039467206272751117, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_eetata_smeft_cehre_m1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.00039526795717095316, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_eetata_smeft_cehre_p1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.00039545719323659203, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_jjtata_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.005953978259013256, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_jjtata_smeft_cehim_m1_ecm240':{"numberOfEvents": 9893750, "sumOfWeights": 9893750, "crossSection": 0.005957006930373593, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_jjtata_smeft_cehim_p1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.005952444260067142, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_jjtata_smeft_cehre_m1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.005972489422656043, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_jjtata_smeft_cehre_p1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.005960914361046144, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_mumutata_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.0003717730785778399, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_mumutata_smeft_cehim_m1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.00037101429593363667, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_mumutata_smeft_cehim_p1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.00037126725168208034, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_mumutata_smeft_cehre_m1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.00037152687307799456, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'mg_ee_mumutata_smeft_cehre_p1_ecm240':{"numberOfEvents": 1000000, "sumOfWeights": 1000000, "crossSection": 0.000371622336608876, "kfactor": 1.0, "matchingEfficiency": 1.0},


    'p8_ee_bbH_Htautau_CPeven':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.00148825, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_bbH_Htautau_CPodd':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.00148825, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_ccH_Htautau_CPeven':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.00148825, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_ccH_Htautau_CPodd':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.00148825, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_ssH_Htautau_CPeven':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.00148825, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_ssH_Htautau_CPodd':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.00148825, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_qqH_Htautau_CPeven':{"numberOfEvents": 2385875, "sumOfWeights": 2385875, "crossSection": 0.00148825, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_qqH_Htautau_CPodd':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.00148825, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_eeH_Htautau_CPeven':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.0003949209283230132, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_eeH_Htautau_CPodd':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.0003949209283230132, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_mumuH_Htautau_CPeven':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.0003717730785778399, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'p8_ee_mumuH_Htautau_CPodd':{"numberOfEvents": 2500000, "sumOfWeights": 2500000, "crossSection": 0.0003717730785778399, "kfactor": 1.0, "matchingEfficiency": 1.0},

}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### no selection, just builds the histograms, it will not be shown in the latex table
    "selReco": "true",
}

# Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well, it's only for the table ###
cutLabels = {}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "n_FSGenElectron":                  {"name":"n_FSGenElectron",                  "title":"Number of final state gen electrons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenElectron_e":                  {"name":"FSGenElectron_e",                  "title":"Final state gen electrons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_p":                  {"name":"FSGenElectron_p",                  "title":"Final state gen electrons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_pt":                 {"name":"FSGenElectron_pt",                 "title":"Final state gen electrons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenElectron_px":                 {"name":"FSGenElectron_px",                 "title":"Final state gen electrons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_py":                 {"name":"FSGenElectron_py",                 "title":"Final state gen electrons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_pz":                 {"name":"FSGenElectron_pz",                 "title":"Final state gen electrons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenElectron_y":                  {"name":"FSGenElectron_y",                  "title":"Final state gen electrons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenElectron_eta":                {"name":"FSGenElectron_eta",                "title":"Final state gen electrons #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenElectron_theta":              {"name":"FSGenElectron_theta",              "title":"Final state gen electrons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenElectron_phi":                {"name":"FSGenElectron_phi",                "title":"Final state gen electrons #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "FSGenElectron_charge":             {"name":"FSGenElectron_charge",             "title":"Final state gen electrons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSGenElectron_mass":               {"name":"FSGenElectron_mass",               "title":"Final state gen electrons mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},
    "FSGenElectron_vertex_x":           {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenElectron_vertex_y":           {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenElectron_vertex_z":           {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
   
    "n_HiggsGenTau":                      {"name":"n_HiggsGenTau",                  "title":"Number of final state gen taus",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "HiggsGenTau_e":                      {"name":"HiggsGenTau_e",                  "title":"Final state gen taus energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "HiggsGenTau_p":                      {"name":"HiggsGenTau_p",                  "title":"Final state gen taus p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "HiggsGenTau_pt":                     {"name":"HiggsGenTau_pt",                 "title":"Final state gen taus p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "HiggsGenTau_px":                     {"name":"HiggsGenTau_px",                 "title":"Final state gen taus p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "HiggsGenTau_py":                     {"name":"HiggsGenTau_py",                 "title":"Final state gen taus p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "HiggsGenTau_pz":                     {"name":"HiggsGenTau_pz",                 "title":"Final state gen taus p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "HiggsGenTau_y":                      {"name":"HiggsGenTau_y",                  "title":"Final state gen taus rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "HiggsGenTau_eta":                    {"name":"HiggsGenTau_eta",                "title":"Final state gen taus #eta",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HiggsGenTau_theta":                  {"name":"HiggsGenTau_theta",              "title":"Final state gen taus #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "HiggsGenTau_phi":                    {"name":"HiggsGenTau_phi",                "title":"Final state gen taus #phi",                                   "bin":128, "xmin":-6.4,"xmax":6.4},
    "HiggsGenTau_charge":                 {"name":"HiggsGenTau_charge",             "title":"Final state gen taus charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "HiggsGenTau_mass":                   {"name":"HiggsGenTau_mass",               "title":"Final state gen taus mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},
    "HiggsGenTau_vertex_x":               {"name":"HiggsGenTau_vertex_x", "title":"Final state gen #tau^{#font[122]{\55}} production vertex x [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "HiggsGenTau_vertex_y":               {"name":"HiggsGenTau_vertex_y", "title":"Final state gen #tau^{#font[122]{\55}} production vertex y [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "HiggsGenTau_vertex_z":               {"name":"HiggsGenTau_vertex_z", "title":"Final state gen #tau^{#font[122]{\55}} production vertex z [mm]",   "bin":100, "xmin":-2000, "xmax":2000},

    "GenDeltaPhi":              {"name":"GenDeltaPhi",            "title":"#Delta#phi (angle of decay)",                  "bin":32, "xmin":-3.14,"xmax":3.14},

}
