#Input directory where the files produced at the stage1 level are
inputDir = "/ceph/sgiappic/HiggsCP/CP/stage2_Gen"

#Optional: output directory, default is local running directory
outputDir = "/ceph/sgiappic/HiggsCP/CP/final_Gen"

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
    'noISR_e+e-_noCuts_EWonly':{},
    'noISR_e+e-_noCuts_cehim_m1':{},
    'noISR_e+e-_noCuts_cehim_p1':{},
    'noISR_e+e-_noCuts_cehre_m1':{},
    'noISR_e+e-_noCuts_cehre_p1':{},
}
###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    'noISR_e+e-_noCuts_EWonly':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00051559935862, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'noISR_e+e-_noCuts_cehim_m1':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00051749741618, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'noISR_e+e-_noCuts_cehim_p1':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00051749741618, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'noISR_e+e-_noCuts_cehre_m1':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00058001482393, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'noISR_e+e-_noCuts_cehre_p1':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.00045498699833000005, "kfactor": 1.0, "matchingEfficiency": 1.0},

}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### no selection, just builds the histograms, it will not be shown in the latex table
    "selGen": "true",
    #"selReco_Maria": " (Recoil>120 && Recoil<140) && (TauFromJet_type[0]>=0 && TauFromJet_type[1]>=0)",
}

# Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well, it's only for the table ###
cutLabels = {}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "n_FSGenZDaughter":                  {"name":"n_FSGenZDaughter",                  "title":"Number of final state gen electrons",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenZDaughter_e":                  {"name":"FSGenZDaughter_e",                  "title":"Final state gen electrons energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenZDaughter_p":                  {"name":"FSGenZDaughter_p",                  "title":"Final state gen electrons p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenZDaughter_pt":                 {"name":"FSGenZDaughter_pt",                 "title":"Final state gen electrons p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenZDaughter_px":                 {"name":"FSGenZDaughter_px",                 "title":"Final state gen electrons p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenZDaughter_py":                 {"name":"FSGenZDaughter_py",                 "title":"Final state gen electrons p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenZDaughter_pz":                 {"name":"FSGenZDaughter_pz",                 "title":"Final state gen electrons p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenZDaughter_y":                  {"name":"FSGenZDaughter_y",                  "title":"Final state gen electrons rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenZDaughter_eta":                {"name":"FSGenZDaughter_eta",                "title":"Final state gen electrons #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenZDaughter_theta":              {"name":"FSGenZDaughter_theta",              "title":"Final state gen electrons #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenZDaughter_phi":                {"name":"FSGenZDaughter_phi",                "title":"Final state gen electrons #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenZDaughter_charge":             {"name":"FSGenZDaughter_charge",             "title":"Final state gen electrons charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSGenZDaughter_mass":               {"name":"FSGenZDaughter_mass",               "title":"Final state gen electrons mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},
    "FSGenZDaughter_vertex_x":           {"name":"FSGenZDaughter_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenZDaughter_vertex_y":           {"name":"FSGenZDaughter_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenZDaughter_vertex_z":           {"name":"FSGenZDaughter_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSGenZDaughter_DEta":                   {"name":"FSGenZDaughter_DEta",           "title":"Gen di-electron #Delta#eta ",                  "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenZDaughter_Acoplanarity":           {"name":"FSGenZDaughter_Acoplanarity",           "title":"Gen di-electron #Delta#phi",                  "bin":32, "xmin":-3.2,"xmax":3.2},

    "n_FSRGenTau":                      {"name":"n_FSRGenTau",                  "title":"Number of final state gen taus",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSRGenTau_e":                      {"name":"FSRGenTau_e",                  "title":"Final state gen taus energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSRGenTau_p":                      {"name":"FSRGenTau_p",                  "title":"Final state gen taus p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSRGenTau_pt":                     {"name":"FSRGenTau_pt",                 "title":"Final state gen taus p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSRGenTau_px":                     {"name":"FSRGenTau_px",                 "title":"Final state gen taus p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSRGenTau_py":                     {"name":"FSRGenTau_py",                 "title":"Final state gen taus p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSRGenTau_pz":                     {"name":"FSRGenTau_pz",                 "title":"Final state gen taus p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSRGenTau_y":                      {"name":"FSRGenTau_y",                  "title":"Final state gen taus rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSRGenTau_eta":                    {"name":"FSRGenTau_eta",                "title":"Final state gen taus #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSRGenTau_theta":                  {"name":"FSRGenTau_theta",              "title":"Final state gen taus #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSRGenTau_phi":                    {"name":"FSRGenTau_phi",                "title":"Final state gen taus #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSRGenTau_charge":                 {"name":"FSRGenTau_charge",             "title":"Final state gen taus charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
    "FSRGenTau_mass":                   {"name":"FSRGenTau_mass",               "title":"Final state gen taus mass [GeV]",             "bin":20, "xmin":0., "xmax":2.},
    "FSRGenTau_vertex_x":               {"name":"FSRGenTau_vertex_x", "title":"Final state gen #tau^{#font[122]{\55}} production vertex x [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSRGenTau_vertex_y":               {"name":"FSRGenTau_vertex_y", "title":"Final state gen #tau^{#font[122]{\55}} production vertex y [mm]",   "bin":100, "xmin":-2000, "xmax":2000},
    "FSRGenTau_vertex_z":               {"name":"FSRGenTau_vertex_z", "title":"Final state gen #tau^{#font[122]{\55}} production vertex z [mm]",   "bin":100, "xmin":-2000, "xmax":2000},

    #"n_TauNeg_MuNuNu":                  {"name":"n_TauNeg_MuNuNu",          "title":"Number of #tau^{-} decays into #mu #nu #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_MuNuNu_Phot":             {"name":"n_TauNeg_MuNuNu_Phot",     "title":"Number of #tau^{-} decays into #mu #nu #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_ENuNu":                   {"name":"n_TauNeg_ENuNu",           "title":"Number of #tau^{-} decays into e #nu #nu per events",              "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_ENuNu_Phot":              {"name":"n_TauNeg_ENuNu_Phot",      "title":"Number of #tau^{-} decays into e #nu #nu #gamma per events",       "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_PiNu":                    {"name":"n_TauNeg_PiNu",            "title":"Number of #tau^{-} decays into #pi #nu per events",                "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_PiNu_Phot":               {"name":"n_TauNeg_PiNu_Phot",       "title":"Number of #tau^{-} decays into #pi #nu #gamma per events",         "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_KNu":                     {"name":"n_TauNeg_KNu",             "title":"Number of #tau^{-} decays into K #nu per events",                  "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_KNu_Phot":                {"name":"n_TauNeg_KNu_Phot",        "title":"Number of #tau^{-} decays into K #nu #gamma per events",           "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_PiK0Nu":                  {"name":"n_TauNeg_PiK0Nu",          "title":"Number of #tau^{-} decays into #pi K^{0} #nu per events",          "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_PiK0Nu_Phot":             {"name":"n_TauNeg_PiK0Nu_Phot",     "title":"Number of #tau^{-} decays into #pi K^{0} #nu #gamma per events",   "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_KK0Nu":                   {"name":"n_TauNeg_KK0Nu",           "title":"Number of #tau^{-} decays into K K^{0} #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_KK0Nu_Phot":              {"name":"n_TauNeg_KK0Nu_Phot",      "title":"Number of #tau^{-} decays into K K^{0} #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_3PiNu":                   {"name":"n_TauNeg_3PiNu",           "title":"Number of #tau^{-} decays into 3 #pi #nu per events",              "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauNeg_3PiNu_Phot":              {"name":"n_TauNeg_3PiNu_Phot",      "title":"Number of #tau^{-} decays into 3 #pi #nu #gamma per events",       "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_PiKKNu":                  {"name":"n_TauNeg_PiKKNu",          "title":"Number of #tau^{-} decays into #pi K K #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauNeg_PiKKNu_Phot":             {"name":"n_TauNeg_PiKKNu_Phot",     "title":"Number of #tau^{-} decays into #pi K K #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},

    #"n_TauPos_MuNuNu":                  {"name":"n_TauPos_MuNuNu",          "title":"Number of #tau^{+} decays into #mu #nu #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5}, 
    #"n_TauPos_MuNuNu_Phot":             {"name":"n_TauPos_MuNuNu_Phot",     "title":"Number of #tau^{+} decays into #mu #nu #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_ENuNu":                   {"name":"n_TauPos_ENuNu",           "title":"Number of #tau^{+} decays into e #nu #nu per events",              "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_ENuNu_Phot":              {"name":"n_TauPos_ENuNu_Phot",      "title":"Number of #tau^{+} decays into e #nu #nu #gamma per events",       "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiNu":                    {"name":"n_TauPos_PiNu",            "title":"Number of #tau^{+} decays into #pi #nu per events",                "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiNu_Phot":               {"name":"n_TauPos_PiNu_Phot",       "title":"Number of #tau^{+} decays into #pi #nu #gamma per events",         "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_KNu":                     {"name":"n_TauPos_KNu",             "title":"Number of #tau^{+} decays into K #nu per events",                  "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_KNu_Phot":                {"name":"n_TauPos_KNu_Phot",        "title":"Number of #tau^{+} decays into K #nu #gamma per events",           "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiK0Nu":                  {"name":"n_TauPos_PiK0Nu",          "title":"Number of #tau^{+} decays into #pi K^{0} #nu per events",          "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiK0Nu_Phot":             {"name":"n_TauPos_PiK0Nu_Phot",     "title":"Number of #tau^{+} decays into #pi K^{0} #nu #gamma per events",   "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_KK0Nu":                   {"name":"n_TauPos_KK0Nu",           "title":"Number of #tau^{+} decays into K K^{0} #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_KK0Nu_Phot":              {"name":"n_TauPos_KK0Nu_Phot",      "title":"Number of #tau^{+} decays into K K^{0} #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_3PiNu":                   {"name":"n_TauPos_3PiNu",           "title":"Number of #tau^{+} decays into 3 #pi #nu per events",              "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_3PiNu_Phot":              {"name":"n_TauPos_3PiNu_Phot",      "title":"Number of #tau^{+} decays into 3 #pi #nu #gamma per events",       "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiKKNu":                  {"name":"n_TauPos_PiKKNu",          "title":"Number of #tau^{+} decays into #pi K K #nu per events",            "bin":2, "xmin":-0.5, "xmax":1.5},
    #"n_TauPos_PiKKNu_Phot":             {"name":"n_TauPos_PiKKNu_Phot",     "title":"Number of #tau^{+} decays into #pi K K #nu #gamma per events",     "bin":2, "xmin":-0.5, "xmax":1.5},

    "n_FSGenNeutrino":                  {"name":"n_FSGenNeutrino",                  "title":"Number of final state gen neutrinos",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "FSGenNeutrino_e":                  {"name":"FSGenNeutrino_e",                  "title":"Final state gen neutrinos energy [GeV]",           "bin":50, "xmin":0, "xmax":100},
    "FSGenNeutrino_p":                  {"name":"FSGenNeutrino_p",                  "title":"Final state gen neutrinos p [GeV]",                "bin":50, "xmin":0, "xmax":100},
    "FSGenNeutrino_pt":                 {"name":"FSGenNeutrino_pt",                 "title":"Final state gen neutrinos p_{T} [GeV]",            "bin":50, "xmin":0, "xmax":100},
    "FSGenNeutrino_px":                 {"name":"FSGenNeutrino_px",                 "title":"Final state gen neutrinos p_{x} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenNeutrino_py":                 {"name":"FSGenNeutrino_py",                 "title":"Final state gen neutrinos p_{y} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenNeutrino_pz":                 {"name":"FSGenNeutrino_pz",                 "title":"Final state gen neutrinos p_{z} [GeV]",            "bin":50,"xmin":-100 ,"xmax":100},
    "FSGenNeutrino_y":                  {"name":"FSGenNeutrino_y",                  "title":"Final state gen neutrinos rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "FSGenNeutrino_eta":                {"name":"FSGenNeutrino_eta",                "title":"Final state gen neutrinos #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenNeutrino_theta":              {"name":"FSGenNeutrino_theta",              "title":"Final state gen neutrinos #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "FSGenNeutrino_phi":                {"name":"FSGenNeutrino_phi",                "title":"Final state gen neutrinos #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSGenNeutrino_charge":             {"name":"FSGenNeutrino_charge",             "title":"Final state gen neutrinos charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},
                                        
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

    "n_GenHiggs":                       {"name":"n_GenHiggs",                  "title":"Number of gen Higgs",              "bin":5, "xmin":-0.5, "xmax":4.5},
    "GenHiggs_e":                       {"name":"GenHiggs_e",                  "title":"Gen Higgs energy [GeV]",           "bin":75, "xmin":0 ,"xmax":150},
    "GenHiggs_p":                       {"name":"GenHiggs_p",                  "title":"Gen Higgs p [GeV]",                "bin":75, "xmin":0 ,"xmax":150},
    "GenHiggs_pt":                      {"name":"GenHiggs_pt",                 "title":"Gen Higgs p_{T} [GeV]",            "bin":75, "xmin":0 ,"xmax":150},
    "GenHiggs_px":                      {"name":"GenHiggs_px",                 "title":"Gen Higgs p_{x} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenHiggs_py":                      {"name":"GenHiggs_py",                 "title":"Gen Higgs p_{y} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenHiggs_pz":                      {"name":"GenHiggs_pz",                 "title":"Gen Higgs p_{z} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenHiggs_y":                       {"name":"GenHiggs_y",                  "title":"Gen Higgs rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "GenHiggs_mass":                    {"name":"GenHiggs_y",                  "title":"Gen Higgs M [GeV]",                "bin":50, "xmin":90, "xmax":140},
    "GenHiggs_eta":                     {"name":"GenHiggs_eta",                "title":"Gen Higgs #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "GenHiggs_theta":                   {"name":"GenHiggs_theta",              "title":"Gen Higgs #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "GenHiggs_phi":                     {"name":"GenHiggs_phi",                "title":"Gen Higgs #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "GenHiggs_charge":                  {"name":"GenHiggs_charge",             "title":"Gen Higgs charge",                 "bin":3, "xmin":-1.5,"xmax":1.5},

    #### CP variables

    "GenZ_e":                       {"name":"GenZ_e",                  "title":"Gen Z energy [GeV]",           "bin":75, "xmin":0 ,"xmax":150},
    "GenZ_p":                       {"name":"GenZ_p",                  "title":"Gen Z p [GeV]",                "bin":75, "xmin":0 ,"xmax":150},
    "GenZ_pt":                      {"name":"GenZ_pt",                 "title":"Gen Z p_{T} [GeV]",            "bin":75, "xmin":0 ,"xmax":150},
    "GenZ_px":                      {"name":"GenZ_px",                 "title":"Gen Z p_{x} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenZ_py":                      {"name":"GenZ_py",                 "title":"Gen Z p_{y} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenZ_pz":                      {"name":"GenZ_pz",                 "title":"Gen Z p_{z} [GeV]",            "bin":300, "xmin":-150 ,"xmax":150},
    "GenZ_y":                       {"name":"GenZ_y",                  "title":"Gen Z rapidity",               "bin":40, "xmin":-4., "xmax":4.},
    "GenZ_mass":                    {"name":"GenZ_y",                  "title":"Gen Z M [GeV]",                "bin":50, "xmin":90, "xmax":140},
    "GenZ_eta":                     {"name":"GenZ_eta",                "title":"Gen Z #eta",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "GenZ_theta":                   {"name":"GenZ_theta",              "title":"Gen Z #theta",                 "bin":16, "xmin":0,"xmax":3.2},
    "GenZ_phi":                     {"name":"GenZ_phi",                "title":"Gen Z #phi",                   "bin":32, "xmin":-3.2,"xmax":3.2},

    "FSRGenTau_DEta":              {"name":"FSRGenTau_DEta",              "title":"Gen di-#tau #Delta#eta",                  "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSRGenTau_Acoplanarity":              {"name":"FSRGenTau_Acoplanarity",              "title":"Gen di-#tau #Delta#phi",                  "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSRGenTau_cos":               {"name":"FSRGenTau_cos",               "title":"Gen di-#tau cos#theta",                   "bin":100, "xmin":-1.,"xmax":1.},
    "FSRGenTau_DR":                {"name":"FSRGenTau_DR",                "title":"Gen di-#tau #Delta R",                    "bin":70, "xmin":0,"xmax":7.},
    "FSRGenTau_DEta":           {"name":"FSRGenTau_DEta",           "title":"Gen di-#tau #Delta#eta in H rest frame",                  "bin":32, "xmin":-3.2,"xmax":3.2},
    "FSRGenTau_Acoplanarity":           {"name":"FSRGenTau_Acoplanarity",           "title":"Gen di-#tau #Delta#phi in H rest frame",                  "bin":32, "xmin":-3.2,"xmax":3.2},

    "HRF_GenTau_px":                 {"name":"HRF_GenTau_px",                 "title":"Gen #tau p_{x} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTau_py":                 {"name":"HRF_GenTau_py",                 "title":"Gen #tau p_{y} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTau_pz":                 {"name":"HRF_GenTau_pz",                 "title":"Gen #tau p_{z} [GeV] in H rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "HRF_GenTau_p":                  {"name":"HRF_GenTau_p",                  "title":"Gen #tau p [GeV] in H rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTau_pt":                 {"name":"HRF_GenTau_pt",                 "title":"Gen #tau p_{T} [GeV] in H rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTau_e":                  {"name":"HRF_GenTau_e",                  "title":"Gen #tau energy [GeV] in H rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "HRF_GenTau_eta":                {"name":"HRF_GenTau_eta",                "title":"Gen #tau #eta in H rest frame",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "HRF_GenTau_phi":                {"name":"HRF_GenTau_phi",                "title":"Gen #tau #phi in H rest frame",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "HRF_GenTau_theta":              {"name":"HRF_GenTau_theta",              "title":"Gen #tau #theta in H rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "HRF_GenTau_y":                  {"name":"HRF_GenTau_y",                  "title":"Gen #tau rapidity in H rest frame",               "bin":40, "xmin":-4., "xmax":4.},
    "HRF_GenTau_DEta":                   {"name":"HRF_GenTau_DEta",           "title":"Gen di-#tau #Delta#eta in H rest frame",                  "bin":32, "xmin":-3.2,"xmax":3.2},
    "HRF_GenTau_Acoplanarity":           {"name":"HRF_GenTau_Acoplanarity",           "title":"Gen di-#tau #Delta#phi in H rest frame",                  "bin":32, "xmin":-3.2,"xmax":3.2},

    "ZRF_GenZDaughter_px":                 {"name":"ZRF_GenZDaughter_px",                 "title":"Gen electron p_{x} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZDaughter_py":                 {"name":"ZRF_GenZDaughter_py",                 "title":"Gen electron p_{y} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZDaughter_pz":                 {"name":"ZRF_GenZDaughter_pz",                 "title":"Gen electron p_{z} [GeV] in Z rest frame",            "bin":50,"xmin":-100 ,"xmax":100},
    "ZRF_GenZDaughter_p":                  {"name":"ZRF_GenZDaughter_p",                  "title":"Gen electron p [GeV] in Z rest frame",                "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZDaughter_pt":                 {"name":"ZRF_GenZDaughter_pt",                 "title":"Gen electron p_{T} [GeV] in Z rest frame",            "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZDaughter_e":                  {"name":"ZRF_GenZDaughter_e",                  "title":"Gen electron energy [GeV] in Z rest frame",           "bin":75, "xmin":0 ,"xmax":150},
    "ZRF_GenZDaughter_eta":                {"name":"ZRF_GenZDaughter_eta",                "title":"Gen electron #eta in Z rest frame",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "ZRF_GenZDaughter_phi":                {"name":"ZRF_GenZDaughter_phi",                "title":"Gen electron #phi in Z rest frame",                   "bin":32, "xmin":-3.2,"xmax":3.2},
    "ZRF_GenZDaughter_theta":              {"name":"ZRF_GenZDaughter_theta",              "title":"Gen electron #theta in Z rest frame",                 "bin":16, "xmin":0,"xmax":3.2},
    "ZRF_GenZDaughter_y":                  {"name":"ZRF_GenZDaughter_y",                  "title":"Gen electron rapidity in Z rest frame",               "bin":40, "xmin":-4., "xmax":4.},
    "ZRF_GenZDaughter_DEta":                   {"name":"ZRF_GenZDaughter_DEta",           "title":"Gen di-electron #Delta#eta in Z rest frame",                  "bin":32, "xmin":-3.2,"xmax":3.2},
    "ZRF_GenZDaughter_Acoplanarity":           {"name":"ZRF_GenZDaughter_Acoplanarity",           "title":"Gen di-electron #Delta#phi in Z rest frame",                  "bin":32, "xmin":-3.2,"xmax":3.2},

    "GenThetastar":           {"name":"GenThetastar",         "title":"Gen #theta^{*}",                  "bin":32, "xmin":0,"xmax":3.2},
    "GenTheta2":              {"name":"GenTheta2",            "title":"Gen #theta_{2}",                  "bin":32, "xmin":0,"xmax":3.2},
    "GenPhi1":                {"name":"GenPhi1",              "title":"Gen #phi_{1}",                    "bin":32, "xmin":0,"xmax":3.2},
    "GenPhi":                 {"name":"GenPhi",               "title":"Gen #phi",                        "bin":32, "xmin":0,"xmax":3.2},
    "GenTheta1":              {"name":"GenTheta1",            "title":"Gen #theta_{1}",                  "bin":32, "xmin":0,"xmax":3.2},

    "GenThetastar_cos":           {"name":"GenThetastar_cos",         "title":"Gen cos#theta^{*}",                  "bin":50, "xmin":-1.,"xmax":1.},
    "GenTheta2_cos":              {"name":"GenTheta2_cos",            "title":"Gen cos#theta_{2}",                  "bin":50, "xmin":-1.,"xmax":1.},
    "GenPhi1_cos":                {"name":"GenPhi1_cos",              "title":"Gen cos#phi_{1}",                    "bin":50, "xmin":-1.,"xmax":1.},
    "GenPhi_cos":                 {"name":"GenPhi_cos",               "title":"Gen cos#phi",                        "bin":50, "xmin":-1.,"xmax":1.},
    "GenTheta1_cos":              {"name":"GenTheta1_cos",            "title":"Gen cos#theta_{1}",                  "bin":50, "xmin":-1.,"xmax":1.},

    "GenRecoil":                   {"name":"GenRecoil",                   "title":"Gen M_{recoil} [GeV]",                     "bin":80, "xmin":80., "xmax":160.},
    

}
