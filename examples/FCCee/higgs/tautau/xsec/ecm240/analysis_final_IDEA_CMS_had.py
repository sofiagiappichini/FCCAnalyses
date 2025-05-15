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
    'IDEA_events_002119867': {},
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
    "IDEA_events_002119867":{"numberOfEvents": 100000, "sumOfWeights": 100000, "crossSection": 0.0269, "kfactor": 1.0, "matchingEfficiency": 1.0},
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

    "CHadron_p_res_total":             {"name":"CHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":2000, "xmin":-0.01, "xmax":0.01}, 
    #"NHadron_p_res_total":             {"name":"NHadron_p_res_total",             "title":"p_{reco}-p_{gen}/p_{gen}",    "bin":2000, "xmin":-0.4290948288251621, "xmax":0.4290948288251621}, 

}