#Input directory where the files produced at the stage1 level are
inputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/stage1_res/had/"

outputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/final_res/had/"

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
    'IDEA_CMS1': {},
    'CMS_Phase2_events_002119867': {},
    'CMS_Phase1_events_002119867': {},
}

###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    "IDEA":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.0269, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'IDEA_CMS2': {"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.0269, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'IDEA_CMS1': {"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.0269, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "CMS_Phase2_events_002119867":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.0269, "kfactor": 1.0, "matchingEfficiency": 1.0},
    "CMS_Phase1_events_002119867":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.0269, "kfactor": 1.0, "matchingEfficiency": 1.0},
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

    #"CHadron_p_res_total":             {"name":"CHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":2000, "xmin":-0.1, "xmax":0.1}, 
#    "n_genBottoms":            {"name":"n_genBottoms",             "title":"Number of MC b quarks",    "bin":7, "xmin":0, "xmax":7},
#    "genBottom_p":             {"name":"genBottom_p",              "title":"MC b quark p [GeV]",       "bin":50, "xmin":0,"xmax":50},
#    "genBottom_e":             {"name":"genBottom_e",                   "title":"MC b quark energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
#    "genBottom_pt":            {"name":"genBottom_pt",                  "title":"MC b quark p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
#    "genBottom_px":            {"name":"genBottom_px",                  "title":"MC b quark p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "genBottom_py":            {"name":"genBottom_py",                  "title":"MC b quark p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "genBottom_pz":            {"name":"genBottom_pz",                  "title":"MC b quark p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "genBottom_eta":           {"name":"genBottom_eta",                 "title":"MC b quark #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
#    "genBottom_theta":         {"name":"genBottom_theta",               "title":"MC b quark #theta",                         "bin":16, "xmin":0,"xmax":3.2},
#    "genBottom_phi":           {"name":"genBottom_phi",                 "title":"MC b quark #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
#    "genBottom_charge":        {"name":"genBottom_charge",              "title":"MC b quark charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
#    "genBottom_mass":          {"name":"genBottom_mass",                 "title":"MC b quark mass [GeV]",                         "bin":50, "xmin":0,"xmax":10},

#    "n_FSGenNeutralHadrons":                {"name":"n_FSGenNeutralHadrons",                "title":"Number of MC neutral hadrons",   "bin":20, "xmin":0, "xmax":20},
#    "FSGenNeutralHadrons_p":                {"name":"FSGenNeutralHadrons_p",                "title":"MC neutral hadron p [GeV]",      "bin":50,"xmin":0 ,"xmax":50},
#    "FSGenNeutralHadrons_eta":              {"name":"FSGenNeutralHadrons_eta",              "title":"MC neutral hadron #eta",         "bin":32, "xmin":-3.2,"xmax":3.2},

#    "n_FSGenChargedHadrons":                {"name":"n_FSGenChargedHadrons",                "title":"Number of MC charged hadrons",   "bin":70, "xmin":0, "xmax":70},
 #   "FSGenChargedHadrons_p":                {"name":"FSGenChargedHadrons_p",                "title":"MC charged hadron p [GeV]",      "bin":50,"xmin":0 ,"xmax":50},
#    "FSGenChargedHadrons_eta":              {"name":"FSGenChargedHadrons_eta",              "title":"MC charged hadron #eta",         "bin":32, "xmin":-3.2,"xmax":3.2},

#    "n_NeutralHadron":                {"name":"n_NeutralHadron",                "title":"Number of Reco neutral hadrons",   "bin":20, "xmin":0, "xmax":20},
#    "NeutralHadron_p":                {"name":"NeutralHadron_p",                "title":"neutral hadron p [GeV]",      "bin":50,"xmin":0 ,"xmax":50},
#    "NeutralHadron_eta":              {"name":"NeutralHadron_eta",              "title":"Reco neutral hadron #eta",         "bin":32, "xmin":-3.2,"xmax":3.2},

#    "n_ChargedHadron":                {"name":"n_ChargedHadron",                "title":"Number of Reco charged hadrons",   "bin":70, "xmin":0, "xmax":70},
#    "ChargedHadron_p":                {"name":"ChargedHadron_p",                "title":"charged hadron p [GeV]",      "bin":50,"xmin":0 ,"xmax":50},
#    "ChargedHadron_eta":              {"name":"ChargedHadron_eta",              "title":"Reco charged hadron #eta",         "bin":32, "xmin":-3.2,"xmax":3.2},

    #"n_ChargedHadron":                  {"name":"CHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":7, "xmin":-1, "xmax":1},
    #"n_NeutralHadron":                  {"name":"CHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":7, "xmin":-1, "xmax":1},
    #"n_FSGenNeutralHadrons":            {"name":"CHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":7, "xmin":-1, "xmax":1},
    #"n_FSGenChargedHadrons":            {"name":"CHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":7, "xmin":-1, "xmax":1},
#    "n_DeltaNeutralHadrons":            {"name":"n_DeltaNeutralHadrons",             "title":"n_{Reco_NH}-n_{MC_NH}",    "bin":30, "xmin":-15, "xmax":15},
    
#    "CHadron_dR":                      {"name":"CHadron_dR",                      "title":"charged hadron dR between MC and Reco",          "bin":50,"xmin":0 ,"xmax":0.2},
#    "NHadron_dR":                      {"name":"NHadron_dR",                      "title":"neutral hadron dR between MC and Reco",          "bin":50,"xmin":0 ,"xmax":0.6},

#    "n_NHadron_low_dR":            {"name":"n_NHadron_low_dR",                  "title":"Number of reco neutral hadrons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
 #   "NHadron_low_dR_e":             {"name":"NHadron_low_dR_e",                   "title":"Neutral hadron energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
 #   "NHadron_low_dR_p":             {"name":"NHadron_low_dR_p",                   "title":"Neutral hadron p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
#    "NHadron_low_dR_pt":            {"name":"NHadron_low_dR_pt",                  "title":"Neutral hadron p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
#    "NHadron_low_dR_px":            {"name":"NHadron_low_dR_px",                  "title":"Neutral hadron p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "NHadron_low_dR_py":            {"name":"NHadron_low_dR_py",                  "title":"Neutral hadron p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "NHadron_low_dR_pz":            {"name":"NHadron_low_dR_pz",                  "title":"Neutral hadron p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "NHadron_low_dR_eta":           {"name":"NHadron_low_dR_eta",                 "title":"Neutral hadron #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
#    "NHadron_low_dR_theta":         {"name":"NHadron_low_dR_theta",               "title":"Neutral hadron #theta",                         "bin":16, "xmin":0,"xmax":3.2},
#    "NHadron_low_dR_phi":           {"name":"NHadron_low_dR_phi",                 "title":"Neutral hadron #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
#    "NHadron_low_dR_charge":        {"name":"NHadron_low_dR_charge",              "title":"Neutral hadron charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
#    "NHadron_low_dR_mass":          {"name":"NHadron_low_dR_mass",                 "title":"Neutral hadron mass [GeV]",                         "bin":50, "xmin":0,"xmax":10},
#    "NHadron_low_dR_MCPDG_1":                      {"name":"NHadron_low_dR_MCPDG",                      "title":"MC PDG of neutral hadrons with dR < 0.01 to there MC",          "bin":800,"xmin":-400 ,"xmax":400},
#    "NHadron_low_dR_MCPDG_2":                      {"name":"NHadron_low_dR_MCPDG",                      "title":"MC PDG of neutral hadrons with dR < 0.01 to there MC",          "bin":200,"xmin":2100 ,"xmax":2300},

#    "n_NHadron_high_dR":            {"name":"n_NHadron_high_dR",                  "title":"Number of reco neutral hadrons",                     "bin":5, "xmin":-0.5, "xmax":4.5},
#    "NHadron_high_dR_e":             {"name":"NHadron_high_dR_e",                   "title":"Neutral hadron energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},
#    "NHadron_high_dR_p":             {"name":"NHadron_high_dR_p",                   "title":"Neutral hadron p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
#    "NHadron_high_dR_pt":            {"name":"NHadron_high_dR_pt",                  "title":"Neutral hadron p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
#    "NHadron_high_dR_px":            {"name":"NHadron_high_dR_px",                  "title":"Neutral hadron p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "NHadron_high_dR_py":            {"name":"NHadron_high_dR_py",                  "title":"Neutral hadron p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "NHadron_high_dR_pz":            {"name":"NHadron_high_dR_pz",                  "title":"Neutral hadron p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "NHadron_high_dR_eta":           {"name":"NHadron_high_dR_eta",                 "title":"Neutral hadron #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
#    "NHadron_high_dR_theta":         {"name":"NHadron_high_dR_theta",               "title":"Neutral hadron #theta",                         "bin":16, "xmin":0,"xmax":3.2},
#    "NHadron_high_dR_phi":           {"name":"NHadron_high_dR_phi",                 "title":"Neutral hadron #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
#    "NHadron_high_dR_charge":        {"name":"NHadron_high_dR_charge",              "title":"Neutral hadron charge",                         "bin":3, "xmin":-1.5,"xmax":1.5},
#    "NHadron_high_dR_mass":          {"name":"NHadron_high_dR_mass",                 "title":"Neutral hadron mass [GeV]",                         "bin":50, "xmin":0,"xmax":10},
#    "NHadron_high_dR_MCPDG_1":                     {"name":"NHadron_high_dR_MCPDG",                     "title":"MC PDG of neutral hadrons with dR > 0.06 to there MC",          "bin":800,"xmin":-400 ,"xmax":400},
#    "NHadron_high_dR_MCPDG_2":                     {"name":"NHadron_high_dR_MCPDG",                     "title":"MC PDG of neutral hadrons with dR > 0.06 to there MC",          "bin":200,"xmin":2000 ,"xmax":2200},


#    "TagJet_kt2_e":                {"name":"TagJet_kt2_e",                   "title":"kt2 jet energy [GeV]",                   "bin":50,"xmin":0 ,"xmax":100},   
#    "TagJet_kt2_p":                {"name":"TagJet_kt2_p",                   "title":"kt2 jet p [GeV]",                        "bin":50,"xmin":0 ,"xmax":100},
#    "TagJet_kt2_pt":               {"name":"TagJet_kt2_pt",                  "title":"kt2 jet p_{T} [GeV]",                    "bin":50,"xmin":0 ,"xmax":100},
#    "TagJet_kt2_px":               {"name":"TagJet_kt2_px",                  "title":"kt2 jet p_{x} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "TagJet_kt2_py":               {"name":"TagJet_kt2_py",                  "title":"kt2 jet p_{y} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "TagJet_kt2_pz":               {"name":"TagJet_kt2_pz",                  "title":"kt2 jet p_{z} [GeV]",                    "bin":50,"xmin":-100 ,"xmax":100},
#    "TagJet_kt2_eta":              {"name":"TagJet_kt2_eta",                 "title":"kt2 jet #eta",                           "bin":32, "xmin":-3.2,"xmax":3.2},
#    "TagJet_kt2_theta":            {"name":"TagJet_kt2_theta",               "title":"kt2 jet #theta",                         "bin":16, "xmin":0,"xmax":3.2},
#    "TagJet_kt2_phi":              {"name":"TagJet_kt2_phi",                 "title":"kt2 jet #phi",                           "bin":32, "xmin":-3.2,"xmax":3.2},
#    "TagJet_kt2_mass":             {"name":"TagJet_kt2_mass",                "title":"kt2 jet mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},
#    "TagJet_kt2_charge":             {"name":"TagJet_kt2_charge",                "title":"kt2 jet charge",                     "bin":10, "xmin":-5., "xmax":5.},
#    "n_TagJet_kt2":                {"name":"n_TagJet_kt2",                   "title":"Number of kt2 jet",                     "bin":5, "xmin":-0.5, "xmax":4.5},
#    "n_TagJet_kt2_constituents":             {"name":"n_TagJet_kt2_constituents",               "title":"kt2 jet constituents",                   "bin":20, "xmin":0., "xmax":20.},
#    "n_TagJet_kt2_charged_constituents":             {"name":"n_TagJet_kt2_charged_constituents",               "title":"kt2 jet charged constituents",                   "bin":20, "xmin":0., "xmax":20.},
#    "n_TagJet_kt2_neutral_constituents":             {"name":"n_TagJet_kt2_neutral_constituents",               "title":"kt2 jet neutral constituents",                   "bin":20, "xmin":0., "xmax":20.},
#    "Dijet_mass":             {"name":"Dijet_mass",                "title":"Dijet mass [GeV]",                     "bin":1000, "xmin":80., "xmax":140.}, 
    #"smeared_Dijet_mass":             {"name":"smeared_Dijet_mass",                "title":"Dijet mass [GeV]",                     "bin":100, "xmin":80., "xmax":140.},

    #"CHadron_p_res_total":             {"name":"CHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":5000, "xmin":-0.1, "xmax":0.1}, 
    #"NHadron_p_res_total":             {"name":"NHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":200, "xmin":-1, "xmax":1},
    #"NHadron_low_dR_p_res_total":             {"name":"NHadron_low_dR_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":200, "xmin":-1, "xmax":1},
    #"NHadron_high_dR_p_res_total":             {"name":"NHadron_high_dR_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":200, "xmin":-1, "xmax":1},
    "jet_reso":                         {"name":"jet_reso",             "title":"p_{jet}-p_{genbquark}/p_{genbquark}",    "bin":2000, "xmin":-0.5, "xmax":0.5},
}