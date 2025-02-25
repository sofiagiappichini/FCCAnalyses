#Input directory where the files produced at the stage1 level are
inputDir = "/" 

#Optional: output directory, default is local running directory
outputDir   = "/" 

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 10.8e6 #pb^-1 #to be checked again for 240 gev

#Scale event yields by intLumi and cross section (optional)
# if scaling, both the number of events in the table and in the histograms will be scaled
doScale = False

#Save event yields in a table (optional)
saveTabular = True


#produces ROOT TTrees, default is False
doTree = False

processList = {
    
}

###Dictionary for prettier names of processes (optional)
#change them if you want but they don't do anything
processLabels = {}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd = {
    'ee_Htautau':{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 1, "kfactor": 1.0, "matchingEfficiency": 1.0},
    
}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### no selection, just builds the histograms, it will not be shown in the latex table
    "selNone":"true",
}

# Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well, it's only for the table ###
cutLabels = {
}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    
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
    "RecoElectron_mass":                {"name":"RecoElectron_mass",                "title":"Reco electron mass [GeV]",                     "bin":20, "xmin":0., "xmax":2.},
      
}