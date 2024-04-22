#Input directory where the files produced at the stage1 level are
#inputDir = "output_stage1/"
inputDir = "/eos/user/s/sgiappic/2HNL_ana/signals_stage1/"

#Output directory where the files produced at the final-selection level are
#outputDir  = "output_finalSel/"
outputDir = "/eos/user/s/sgiappic/2HNL_ana/signals_final/"

#Integrated luminosity for scaling number of events (required only if setting doScale to true)
intLumi = 180e6 #pb^-1

#Scale event yields by intLumi and cross section (optional)
doScale = True

#Save event yields in a table (optional)
saveTabular = True

#Number of CPUs to use
nCPUS = 6

#produces ROOT TTrees, default is False
doTree = False

processList = {
    #run over the full statistics from stage1

    #backgrounds
    #'p8_ee_Zee_ecm91':{},
    #'p8_ee_Zmumu_ecm91':{},
    #'p8_ee_Ztautau_ecm91':{},
    #'p8_ee_Zbb_ecm91':{},
    #'p8_ee_Zcc_ecm91':{},
    #'p8_ee_Zud_ecm91':{},
    #'p8_ee_Zss_ecm91':{},
        
    ### privately produced backgrounds ###
    #'emununu':{},
    #'tatanunu':{},

    #signals
    #'HNL_4e-8_10gev':{},
    #'HNL_1.33e-9_20gev':{},
    #'HNL_2.86e-12_30gev':{},
    #'HNL_2.86e-7_30gev':{},
    #'HNL_5e-12_40gev':{},
    #'HNL_4e-12_50gev':{},
    #'HNL_6.67e-8_60gev':{},
    #'HNL_4e-8_60gev':{},
    #'HNL_2.86e-9_70gev':{},
    #'HNL_2.86e-8_80gev':{},

    'HNL_4e-10_10gev':{},
    'HNL_4e-10_20gev':{},
    'HNL_4e-10_30gev':{},
    'HNL_4e-10_40gev':{},
    'HNL_4e-10_50gev':{},
    'HNL_4e-10_60gev':{},
    'HNL_4e-10_70gev':{},
    'HNL_4e-10_80gev':{},

    'HNL_1.33e-7_10gev':{},
    'HNL_1.33e-7_20gev':{},
    'HNL_1.33e-7_30gev':{},
    'HNL_1.33e-7_40gev':{},
    'HNL_1.33e-7_50gev':{},
    'HNL_1.33e-7_60gev':{},
    'HNL_1.33e-7_70gev':{},
    'HNL_1.33e-7_80gev':{},

    'HNL_2.86e-12_10gev':{},
    'HNL_2.86e-12_20gev':{},
    'HNL_2.86e-12_30gev':{},
    'HNL_2.86e-12_40gev':{},
    'HNL_2.86e-12_50gev':{},
    'HNL_2.86e-12_60gev':{},
    'HNL_2.86e-12_70gev':{},
    'HNL_2.86e-12_80gev':{},

    'HNL_5e-12_10gev':{},
    'HNL_5e-12_20gev':{},
    'HNL_5e-12_30gev':{},
    'HNL_5e-12_40gev':{},
    'HNL_5e-12_50gev':{},
    'HNL_5e-12_60gev':{},
    'HNL_5e-12_70gev':{},
    'HNL_5e-12_80gev':{},

    'HNL_6.67e-10_10gev':{},
    'HNL_6.67e-10_20gev':{},
    'HNL_6.67e-10_30gev':{},
    'HNL_6.67e-10_40gev':{},
    'HNL_6.67e-10_50gev':{},
    'HNL_6.67e-10_60gev':{},
    'HNL_6.67e-10_70gev':{},
    'HNL_6.67e-10_80gev':{},

    'HNL_2.86e-7_10gev':{},
    'HNL_2.86e-7_20gev':{},
    'HNL_2.86e-7_30gev':{},
    'HNL_2.86e-7_40gev':{},
    'HNL_2.86e-7_50gev':{},
    'HNL_2.86e-7_60gev':{},
    'HNL_2.86e-7_70gev':{},
    'HNL_2.86e-7_80gev':{},

}

###Dictionary for prettier names of processes (optional)
processLabels = {
    #backgrounds
    'p8_ee_Zee_ecm91':"Z $\rightarrow$ ee",
    'p8_ee_Zmumu_ecm91':"Z $\rightarrow \mu \mu$",
    'p8_ee_Ztautau_ecm91':"Z $\rightarrow \tau \tau$",
    'p8_ee_Zbb_ecm91':"Z $\rightarrow$ bb",
    'p8_ee_Zcc_ecm91':"Z $\rightarrow$ cc",
    'p8_ee_Zud_ecm91':"Z $\rightarrow$ ud",
    'p8_ee_Zss_ecm91':"Z $\rightarrow$ ss",
    
    'emununu':"e $\mu \nu \nu$",
    'tatanunu':"$\tau \tau \nu \nu$",

    #signals
    'HNL_4e-8_10gev':"$U^{2}=4e-8, M_{N}=10 GeV$",
    'HNL_1.33e-9_20gev':"$U^{2}=1.33e-9, M_{N}=20 GeV$",
    'HNL_2.86e-12_30gev':"$U^{2}=2.86e-12, M_{N}=30 GeV$",
    'HNL_2.86e-7_30gev':"$U^{2}=2.86e-7, M_{N}=30 GeV$",
    'HNL_5e-12_40gev':"$U^{2}=5e-12, M_{N}=40 GeV$",
    'HNL_4e-12_50gev':"$U^{2}=4e-12, M_{N}=50 GeV$",
    'HNL_6.67e-8_60gev':"$U^{2}=6.67e-8, M_{N}=60 GeV$",
    'HNL_4e-8_60gev':"$U^{2}=4e-8, M_{N}=60 GeV$",
    'HNL_2.86e-9_70gev':"$U^{2}=2.86e-9, M_{N}=70 GeV$",
    'HNL_2.86e-8_80gev':"$U^{2}=2.86e-8, M_{N}=80 GeV$",
}

#Link to the dictonary that contains all the cross section information etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Add provate samples as it is not an offical process
procDictAdd={
    
    'HNL_4e-8_10gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 7.388e-7, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_1.33e-9_20gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 2.342e-6, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_2.86e-12_30gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.490e-9, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_2.86e-7_30gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.502e-4, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_5e-12_40gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 6.708e-09, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_4e-12_50gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.25e-09, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_6.67e-8_60gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.965e-05, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_4e-8_60gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 2.995e-5, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_2.86e-9_70gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.23e-06, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'HNL_2.86e-8_80gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.881e-6, "kfactor": 1.0, "matchingEfficiency": 1.0},

    'tatanunu':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 2.855e-4, "kfactor": 1.0, "matchingEfficiency": 1.0},
    'emununu':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 7.619e-4, "kfactor": 1.0, "matchingEfficiency": 1.0},

    'HNL_4e-10_10gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 7.373e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_4e-10_20gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 7.000724999999999e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_4e-10_30gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 6.287075999999998e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_4e-10_40gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 5.378329e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_4e-10_50gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.252068e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_4e-10_60gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 2.990813e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_4e-10_70gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.7100332083008976e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_4e-10_80gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 6.2352593649e-08, "kfactor": 1.0, "matchingEfficiency":1.0},

    'HNL_1.33e-7_10gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.0002469, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_1.33e-7_20gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.000234401213, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_1.33e-7_30gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.00021036747599999998, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_1.33e-7_40gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.00017939637900000002, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_1.33e-7_50gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.000141897971, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_1.33e-7_60gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.00010003114599999999, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_1.33e-7_70gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 5.7150938853135514e-05, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_1.33e-7_80gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 2.2710092322419997e-05, "kfactor": 1.0, "matchingEfficiency":1.0},

    'HNL_2.86e-12_10gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 5.253e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-12_20gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 5.00190734e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-12_30gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.489800359999999e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-12_40gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 3.835910050000001e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-12_50gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 3.03469279e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-12_60gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 2.13112403e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-12_70gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.222465083392036e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-12_80gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.868731152004e-10, "kfactor": 1.0, "matchingEfficiency":1.0},

    'HNL_5e-12_10gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 9.222e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_5e-12_20gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 8.7699219e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_5e-12_30gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 7.8813284e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_5e-12_40gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 6.732171200000001e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_5e-12_50gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 5.32185986e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_5e-12_60gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 3.7530712800000005e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_5e-12_70gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 2.1454398529731456e-09, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_5e-12_80gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 8.549538810180001e-10, "kfactor": 1.0, "matchingEfficiency":1.0},

    'HNL_6.67e-10_10gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.224e-06 , "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_6.67e-10_20gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.1627825000000002e-06, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_6.67e-10_30gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.0435742000000003e-06, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_6.67e-10_40gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 8.911107e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_6.67e-10_50gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 7.045306e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_6.67e-10_60gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 4.9556041e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_6.67e-10_70gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 2.8476787930121774e-07, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_6.67e-10_80gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 1.5594530748200004e-07, "kfactor": 1.0, "matchingEfficiency":1.0},

    'HNL_2.86e-7_10gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.0005235, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-7_20gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.00050087251, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-7_30gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.00045116999, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-7_40gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.00038436751799999987, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-7_50gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.000304519009, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-7_60gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.00021460306999999997, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-7_70gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 0.0001232450573009338, "kfactor": 1.0, "matchingEfficiency":1.0},
    'HNL_2.86e-7_80gev':{"numberOfEvents": 50000, "sumOfWeights": 50000, "crossSection": 5.365835313916999e-05, "kfactor": 1.0, "matchingEfficiency":1.0},
}

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
    ### n_RecoJets==0 useless right now with zero jet in clusters ###
    ### basic selection is vetoes on leptons, charge, photons, jets ###

    ### to be used for signal plots with no distintion between flavors ###
    #"sel2Reco_vetoes": "(  (n_RecoElectrons==2 && n_RecoMuons==0 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                        #|| (n_RecoMuons==2 && n_RecoElectrons==0 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1))) \
                        #|| (n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1))) ) \
                        #&& n_RecoPhotons==0",


    #"selNone": "n_RecoTracks > -1",

    #"sel2RecoSF_vetoes": "((n_RecoElectrons==2 && n_RecoMuons==0 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                        #|| (n_RecoMuons==2 && n_RecoElectrons==0 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) && n_RecoPhotons==0", 
    #"sel2RecoSF_vetoes_15-80M": "((n_RecoElectrons==2 && n_RecoMuons==0 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1)) ) \
                            #|| (n_RecoMuons==2 && n_RecoElectrons==0 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) \
                            #&& n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80", 
    #"sel2RecoSF_vetoes_15-80M_42p": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<42 && RecoElectron_p.at(1)<42 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                            #|| (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<42 && RecoMuon_p.at(1)<42 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) \
                            #&& n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80", 
    #"sel2RecoSF_vetoes_15-80M_42p_10ME": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<42 && RecoElectron_p.at(1)<42 &&((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                            #|| (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<42 && RecoMuon_p.at(1)<42 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) \
                            #&& n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80 && RecoMissingEnergy_e.at(0)>10", 
    #"sel2RecoSF_vetoes_15-80M_42p_10ME_cos": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<42 && RecoElectron_p.at(1)<42 &&((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                            #|| (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<42 && RecoMuon_p.at(1)<42 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) \
                            #&& n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80 && RecoMissingEnergy_e.at(0)>10 && Reco_cos>(-0.8)",
    #"sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<42 && RecoElectron_p.at(1)<42 &&((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                            #|| (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<42 && RecoMuon_p.at(1)<42 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) \
                            #&& n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80 && RecoMissingEnergy_e.at(0)>10 && RecoMissingEnergy_theta.at(0)>0.2 && RecoMissingEnergy_theta.at(0)<3 && Reco_cos>(-0.8)",
    #"sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt_L3.9": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<42 && RecoElectron_p.at(1)<42 &&((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                            #|| (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<42 && RecoMuon_p.at(1)<42 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) \
                            #&& n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80 && RecoMissingEnergy_e.at(0)>10 && RecoMissingEnergy_theta.at(0)>0.2 && RecoMissingEnergy_theta.at(0)<3 && Reco_cos>(-0.8) && Reco_Lxyz>3.9",

    #"sel2RecoSF_vetoes_tracks": "((n_RecoElectrons==2 && n_RecoMuons==0 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                        #|| (n_RecoMuons==2 && n_RecoElectrons==0 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) && n_RecoPhotons==0 && n_RecoTracks == 2",
    #"sel2RecoSF_vetoes_tracks_M80": "((n_RecoElectrons==2 && n_RecoMuons==0 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                        #|| (n_RecoMuons==2 && n_RecoElectrons==0 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                        #&& Reco_invMass<80",
    #"sel2RecoSF_vetoes_tracks_M80_p40": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<40 && RecoElectron_p.at(1)<40 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                        #|| (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<40 && RecoMuon_p.at(1)<40 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                        #&& Reco_invMass<80",
    #"sel2RecoSF_vetoes_tracks_M80_5MEpt_p40": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<40 && RecoElectron_p.at(1)<40 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                        #|| (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<40 && RecoMuon_p.at(1)<40 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                        #&& Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>5",
    #"sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<40 && RecoElectron_p.at(1)<40 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                        #|| (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<40 && RecoMuon_p.at(1)<40 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                        #&& Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>11.5",
    "sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt_0.8cos_0.04Lxy": "((n_RecoElectrons==2 && n_RecoMuons==0 && RecoElectron_p.at(0)<40 && RecoElectron_p.at(1)<40 && ((RecoElectron_charge.at(0)==1 && RecoElectron_charge.at(1)==-1) || (RecoElectron_charge.at(0)==-1 && RecoElectron_charge.at(1)==1))) \
                        || (n_RecoMuons==2 && n_RecoElectrons==0 && RecoMuon_p.at(0)<40 && RecoMuon_p.at(1)<40 && ((RecoMuon_charge.at(0)==1 && RecoMuon_charge.at(1)==-1) || (RecoMuon_charge.at(0)==-1 && RecoMuon_charge.at(1)==1)))) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                        && Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>11.5 && Reco_cos>(-0.8) && Reco_Lxy>0.04",

    #"sel2RecoDF_vetoes": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0",
    #"sel2RecoDF_vetoes_15-80M": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80", 
    #"sel2RecoDF_vetoes_15-80M_39p": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80 && RecoElectron_p.at(0)<39 && RecoMuon_p.at(0)<39 ", 
    #"sel2RecoDF_vetoes_15-80M_39p_10ME43": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80 && RecoElectron_p.at(0)<39 && RecoMuon_p.at(0)<39 \
                            #&& RecoMissingEnergy_e.at(0)>10 && RecoMissingEnergy_e.at(0)<43 ", 
    #"sel2RecoDF_vetoes_15-80M_39p_10ME43_cos": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80 && RecoElectron_p.at(0)<39 && RecoMuon_p.at(0)<39 \
                            #&& RecoMissingEnergy_e.at(0)>10 && RecoMissingEnergy_e.at(0)<43 && Reco_cos>(-0.8)", 
    #"sel2RecoDF_vetoes_15-80M_39p_10ME43_cos_L5.3": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && Reco_invMass>15 && Reco_invMass<80 && RecoElectron_p.at(0)<39 && RecoMuon_p.at(0)<39 \
                            #&& RecoMissingEnergy_e.at(0)>10 && RecoMissingEnergy_e.at(0)<43 && Reco_cos>(-0.8) && Reco_Lxyz>5.3", 
    
    #"sel2RecoDF_vetoes_tracks": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && n_RecoTracks == 2",
    #"sel2RecoDF_vetoes_tracks_M80": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                                   # && Reco_invMass<80",
    #"sel2RecoDF_vetoes_tracks_M80_5MEpt": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                                    #&& Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>5",
    #"sel2RecoDF_vetoes_tracks_M80_7MEpt": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                                    #&& Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>7",
    "sel2RecoDF_vetoes_tracks_M80_7MEpt_0.8cos_0.04Lxy": "n_RecoElectrons==1 && n_RecoMuons==1 && ((RecoElectron_charge.at(0)==1 && RecoMuon_charge.at(0)==-1) || (RecoElectron_charge.at(0)==-1 && RecoMuon_charge.at(0)==1)) && n_RecoPhotons==0 && n_RecoTracks == 2 \
                                    && Reco_invMass<80 && RecoMissingEnergy_pt.at(0)>7 && Reco_cos>(-0.8) && Reco_Lxy>0.04",
}

###Dictionary for prettier names of cuts (optional)
### needs to be in the same order as cutList or the table won't be organised well ###
cutLabels = {
    #"selNone": "Before selection",
    #"sel2Reco_vetoes":"Two leptons, no photons and jets",

    #"sel2RecoSF_vetoes":"Two same flavor leptons, no photons and jets",
    #"sel2RecoSF_vetoes_15-80M":"Two same flavor leptons, no photons and jets, 15<M(l,l)<80 GeV",
    #"sel2RecoSF_vetoes_15-80M_42p":"Two same flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<42 GeV",
    #"sel2RecoSF_vetoes_15-80M_42p_10ME":"Two same flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<42 GeV, E_{miss}>10 Gev",
    #"sel2RecoSF_vetoes_15-80M_42p_10ME_cos":"Two same flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<42 GeV, E_{miss}>10 Gev, cos#theta>-0.8",
    #"sel2RecoSF_vetoes_15-80M_42p_10ME_cos_MEt":"Two same flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<42 GeV, E_{miss}>10 Gev, cos#theta>-0.8, 0.2<#theta_{miss}<3",
    #"sel2RecoSF_vetoes_15-80M_10ME_cos_L3.9":"Two same flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<42 GeV, E_{miss}>10 Gev, cos#theta>-0.8, 0.2<#theta_{miss}<3, L_{xyz}>3.9 mm",
    
    #"sel2RecoSF_vetoes_tracks_M80":"sel2RecoSF_vetoes_tracks_M80",
    #"sel2RecoSF_vetoes_tracks_M80_p40":"sel2RecoSF_vetoes_tracks_M80__p40",
    #"sel2RecoSF_vetoes_tracks_M80_5MEp_p40":"sel2RecoSF_vetoes_tracks_M80_5MEp_p40",
    #"sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt":"sel2RecoSF_vetoes_tracks_M80_p40_11.5MEpt",
    "sel2RecoSF_vetoes_tracks_M80_11.5MEpt_p40_0.8cos":"sel2RecoSF_vetoes_tracks_M80_11.5MEpt_p40_0.8cos",

    #"sel2RecoDF_vetoes":"Two different flavor leptons, no photons and jets",
    #"sel2RecoDF_vetoes_15-80M":"Two different flavor leptons, no photons and jets, 15<M(l,l)<80 GeV",
    #"sel2RecoDF_vetoes_15-80M_39p":"Two different flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<39 GeV",
    #"sel2RecoDF_vetoes_15-80M_39p_10ME43":"Two different flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<39 GeV, 10<E_{miss}<43 Gev",
    #"sel2RecoDF_vetoes_15-80M_39p_10ME43_cos":"Two different flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<39 GeV, 10<E_{miss}<43 Gev, cos#theta>-0.8",
    #"sel2RecoDF_vetoes_15-80M_10MEcos_L5.3":"Two different flavor leptons, no photons and jets, 15<M(l,l)<80 GeV, p<39 GeV, 10<E_{miss}<43 Gev, cos#theta>-0.8, L_{xyz}>5.3 mm",
    
    #"sel2RecoDF_vetoes_tracks_M80":"sel2RecoDF_vetoes_tracks_M80",
    #"sel2RecoDF_vetoes_tracks_M80_5MEpt":"sel2RecoDF_vetoes_tracks_M80_5MEpt",
    #"sel2RecoDF_vetoes_tracks_M80_7MEpt":"sel2RecoDF_vetoes_tracks_M80_7MEpt",
    "sel2RecoDF_vetoes_tracks_M80_7MEpt_0.8cos":"sel2RecoDF_vetoes_tracks_M80_7MEpt_0.8cos",
}

###Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {

    #gen variables
    "n_FSGenElectron":                   {"name":"n_FSGenElectron",                  "title":"Number of final state gen electrons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    #"FSGenElectron_e":                   {"name":"FSGenElectron_e",                  "title":"Final state gen electrons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenElectron_p":                   {"name":"FSGenElectron_p",                  "title":"Final state gen electrons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenElectron_pt":                  {"name":"FSGenElectron_pt",                 "title":"Final state gen electrons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenElectron_pz":                  {"name":"FSGenElectron_pz",                 "title":"Final state gen electrons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenElectron_eta":                 {"name":"FSGenElectron_eta",                "title":"Final state gen electrons #eta",             "bin":60, "xmin":-3,"xmax":3},
    #"FSGenElectron_theta":               {"name":"FSGenElectron_theta",              "title":"Final state gen electrons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    #"FSGenElectron_phi":                 {"name":"FSGenElectron_phi",                "title":"Final state gen electrons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},
    #"FSGenElectron_charge":              {"name":"FSGenElectron_charge",             "title":"Final state gen electrons charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    #"FSGenElectron_vertex_x": {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    #"FSGenElectron_vertex_y": {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    #"FSGenElectron_vertex_z": {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    #"FSGenElectron_vertex_x_prompt": {"name":"FSGenElectron_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    #"FSGenElectron_vertex_y_prompt": {"name":"FSGenElectron_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    #"FSGenElectron_vertex_z_prompt": {"name":"FSGenElectron_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},

    "n_FSGenMuon":                   {"name":"n_FSGenMuon",                  "title":"Number of final state gen Muons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    #"FSGenMuon_e":                   {"name":"FSGenMuon_e",                  "title":"Final state gen Muons energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenMuon_p":                   {"name":"FSGenMuon_p",                  "title":"Final state gen Muons p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenMuon_pt":                  {"name":"FSGenMuon_pt",                 "title":"Final state gen Muons p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenMuon_pz":                  {"name":"FSGenMuon_pz",                 "title":"Final state gen Muons p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenMuon_eta":                 {"name":"FSGenMuon_eta",                "title":"Final state gen Muons #eta",             "bin":60, "xmin":-3,"xmax":3},
    #"FSGenMuon_theta":               {"name":"FSGenMuon_theta",              "title":"Final state gen Muons #theta",           "bin":64, "xmin":0,"xmax":3.2},
    #"FSGenMuon_phi":                 {"name":"FSGenMuon_phi",                "title":"Final state gen Muons #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},
    #"FSGenMuon_charge":              {"name":"FSGenMuon_charge",             "title":"Final state gen Muons charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    #"FSGenMuon_vertex_x": {"name":"FSGenMuon_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    #"FSGenMuon_vertex_y": {"name":"FSGenMuon_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},
    #"FSGenMuon_vertex_z": {"name":"FSGenMuon_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-1000 ,"xmax":1000},

    #"FSGenMuon_vertex_x_prompt": {"name":"FSGenMuon_vertex_x", "title":"Final state gen e^{#font[122]{\55}} production vertex x [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    #"FSGenMuon_vertex_y_prompt": {"name":"FSGenMuon_vertex_y", "title":"Final state gen e^{#font[122]{\55}} production vertex y [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},
    #"FSGenMuon_vertex_z_prompt": {"name":"FSGenMuon_vertex_z", "title":"Final state gen e^{#font[122]{\55}} production vertex z [mm]",      "bin":100,"xmin":-0.01 ,"xmax":0.01},

    #"FSGen_Lxy":      {"name":"FSGen_Lxy",      "title":"Gen L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":2000},
    #"FSGen_Lxyz":     {"name":"FSGen_Lxyz",     "title":"Gen L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":2000},
    #"FSGen_Lxyz_prompt":     {"name":"FSGen_Lxyz",     "title":"Gen L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":10},

    #"n_FSGenNeutrino":                   {"name":"n_FSGenNeutrino",                  "title":"Number of final state gen neutrinos",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    #"FSGenNeutrino_e":                   {"name":"FSGenNeutrino_e",                  "title":"Final state gen neutrinos energy [GeV]",     "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenNeutrino_p":                   {"name":"FSGenNeutrino_p",                  "title":"Final state gen neutrinos p [GeV]",          "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenNeutrino_pt":                  {"name":"FSGenNeutrino_pt",                 "title":"Final state gen neutrinos p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenNeutrino_pz":                  {"name":"FSGenNeutrino_pz",                 "title":"Final state gen neutrinos p_{z} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenNeutrino_eta":                 {"name":"FSGenNeutrino_eta",                "title":"Final state gen neutrinos #eta",             "bin":60, "xmin":-3,"xmax":3},
    #"FSGenNeutrino_theta":               {"name":"FSGenNeutrino_theta",              "title":"Final state gen neutrinos #theta",           "bin":64, "xmin":0,"xmax":3.2},
    #"FSGenNeutrino_phi":                 {"name":"FSGenNeutrino_phi",                "title":"Final state gen neutrinos #phi",             "bin":64, "xmin":-3.2,"xmax":3.2},
    #"FSGenNeutrino_charge":              {"name":"FSGenNeutrino_charge",             "title":"Final state gen neutrinos charge",           "bin":3, "xmin":-1.5,"xmax":1.5},

    #"FSGen_ee_invMass":   {"name":"FSGen_ee_invMass",   "title":"Gen M(e,e) [GeV]",           "bin":100,"xmin":0, "xmax":100},
    #"FSGen_eenu_invMass": {"name":"FSGen_eenu_invMass", "title":"Gen m_{ee#nu} [GeV]",           "bin":100,"xmin":0, "xmax":100},
    #"FSGen_mumu_invMass":   {"name":"FSGen_mumu_invMass",   "title":"Gen M(#mu,#mu) [GeV]",           "bin":100,"xmin":0, "xmax":100},
    #"FSGen_emu_invMass":   {"name":"FSGen_emu_invMass",   "title":"Gen M(e,#mu) [GeV]",           "bin":100,"xmin":0, "xmax":100},
    #"FSGen_invMass":   {"name":"FSGen_invMass",   "title":"Gen M(l,l') [GeV]",           "bin":100,"xmin":0, "xmax":100},

    #"n_FSGenN":                      {"name":"n_FSGenN",                  "title":"Number of final state gen n",        "bin":5,"xmin":-0.5 ,"xmax":4.5},
    #"FSGenN_mass":                   {"name":"FSGenN_mass",                  "title":"Gen N mass [Gev]",        "bin":100,"xmin":0 ,"xmax":90},
    #"FSGenN_time":                   {"name":"FSGenN_time",                  "title":"Gen N time [s]",        "bin":100,"xmin":0 ,"xmax":1e-8},
    #"FSGenN_tau":                    {"name":"FSGenN_tau",                  "title":"Gen N #tau [s]",        "bin":100,"xmin":0 ,"xmax":1e-8},

    "n_FSGenPhoton":                   {"name":"n_FSGenPhoton",                  "title":"Number of final state gen photons",          "bin":10,"xmin":-0.5 ,"xmax":9.5},
    #"FSGenPhoton_e":                   {"name":"FSGenPhoton_e",                  "title":"Final state gen photons energy [GeV]",       "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenPhoton_p":                   {"name":"FSGenPhoton_p",                  "title":"Final state gen photons p [GeV]",            "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenPhoton_pt":                  {"name":"FSGenPhoton_pt",                 "title":"Final state gen photons p_{T} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenPhoton_pz":                  {"name":"FSGenPhoton_pz",                 "title":"Final state gen photons p_{z} [GeV]",        "bin":100,"xmin":0 ,"xmax":50},
    #"FSGenPhoton_eta":                 {"name":"FSGenPhoton_eta",                "title":"Final state gen photons #eta",               "bin":60, "xmin":-3,"xmax":3},
    #"FSGenPhoton_theta":               {"name":"FSGenPhoton_theta",              "title":"Final state gen photons #theta",             "bin":64, "xmin":0,"xmax":3.2},
    #"FSGenPhoton_phi":                 {"name":"FSGenPhoton_phi",                "title":"Final state gen photons #phi",               "bin":64, "xmin":-3.2,"xmax":3.2},
    #"FSGenPhoton_charge":              {"name":"FSGenPhoton_charge",             "title":"Final state gen photons charge",             "bin":3, "xmin":-1.5,"xmax":1.5},

    #reco variables
    "n_RecoTracks":                    {"name":"n_RecoTracks",                   "title":"Total number of reco tracks",           "bin":10,"xmin":-0.5 ,"xmax":9.5},
    #"n_PrimaryTracks":                 {"name":"n_PrimaryTracks",                "title":"Total number of primary tracks",           "bin":10,"xmin":-0.5 ,"xmax":9.5},
    #"n_SecondaryTracks":               {"name":"n_SecondaryTracks",              "title":"Total number of secondary tracks",           "bin":10,"xmin":-0.5 ,"xmax":9.5},
    "n_RecoJets":       {"name":"n_RecoJets",      "title":"Total number of reco jets",         "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoPhotons":    {"name":"n_RecoPhotons",   "title":"Total number of reco photons",      "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoElectrons":  {"name":"n_RecoElectrons", "title":"Total number of reco electrons",    "bin":5,"xmin":-0.5 ,"xmax":4.5},
    "n_RecoMuons":      {"name":"n_RecoMuons",     "title":"Total number of reco muons",        "bin":5,"xmin":-0.5 ,"xmax":4.5},

    #"jets_e":        {"name":"jets_e",        "title":"Reco jet energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_e":        {"name":"RecoJet_e",        "title":"Reco jet energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_p":        {"name":"RecoJet_p",        "title":"Reco jet p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_pt":       {"name":"RecoJet_pt",       "title":"Reco jet p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_pz":       {"name":"RecoJet_pz",       "title":"Reco jet p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoJet_eta":      {"name":"RecoJet_eta",      "title":"Reco jet #eta",         "bin":60, "xmin":-3,"xmax":3},
    #"RecoJet_theta":    {"name":"RecoJet_theta",    "title":"Reco jet #theta",       "bin":64, "xmin":0,"xmax":3.2},
    #"RecoJet_phi":      {"name":"RecoJet_phi",      "title":"Reco jet #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    #"RecoJet_charge":   {"name":"RecoJet_charge",   "title":"Reco jet charge",       "bin":3, "xmin":-1.5,"xmax":1.5},
    #"RecoJetTrack_absD0":             {"name":"RecoJetTrack_absD0",     "title":"Reco jet tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    #"RecoJetTrack_absD0_prompt":      {"name":"RecoJetTrack_absD0",     "title":"Reco jet tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    #"RecoJetTrack_absZ0":             {"name":"RecoJetTrack_absZ0",     "title":"Reco jet tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    #"RecoJetTrack_absZ0_prompt":      {"name":"RecoJetTrack_absZ0",     "title":"Reco jet tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    #"RecoJetTrack_absD0sig":          {"name":"RecoJetTrack_absD0sig",  "title":"Reco jet tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    #"RecoJetTrack_absD0sig_prompt":   {"name":"RecoJetTrack_absD0sig",  "title":"Reco jet tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    #"RecoJetTrack_absZ0sig":          {"name":"RecoJetTrack_absZ0sig",  "title":"Reco jet tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    #"RecoJetTrack_absZ0sig_prompt":   {"name":"RecoJetTrack_absZ0sig",  "title":"Reco jet tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    #"RecoJetTrack_D0cov":      {"name":"RecoJetTrack_D0cov",     "title":"Reco jet tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    #"RecoJetTrack_Z0cov":      {"name":"RecoJetTrack_Z0cov",     "title":"Reco jet tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    "RecoElectron_e":        {"name":"RecoElectron_e",        "title":"Reco electron energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_p":        {"name":"RecoElectron_p",        "title":"Reco electron p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_pt":       {"name":"RecoElectron_pt",       "title":"Reco electron p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoElectron_px":       {"name":"RecoElectron_px",       "title":"Reco electron p_{x} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    "RecoElectron_py":       {"name":"RecoElectron_py",       "title":"Reco electron p_{y} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    "RecoElectron_pz":       {"name":"RecoElectron_pz",       "title":"Reco electron p_{z} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    "RecoElectron_eta":      {"name":"RecoElectron_eta",      "title":"Reco electron #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoElectron_theta":    {"name":"RecoElectron_theta",    "title":"Reco electron #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoElectron_phi":      {"name":"RecoElectron_phi",      "title":"Reco electron #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    #"RecoElectron_charge":   {"name":"RecoElectron_charge",   "title":"Reco electron charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoElectronTrack_absD0":             {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_absD0_med":         {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":10},
    "RecoElectronTrack_absD0_prompt":      {"name":"RecoElectronTrack_absD0",     "title":"Reco electron tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoElectronTrack_absZ0":             {"name":"RecoElectronTrack_absZ0",     "title":"Reco electron tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoElectronTrack_absZ0_prompt":      {"name":"RecoElectronTrack_absZ0",     "title":"Reco electron tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoElectronTrack_absD0sig":          {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_absD0sig_med":      {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    "RecoElectronTrack_absD0sig_prompt":   {"name":"RecoElectronTrack_absD0sig",  "title":"Reco electron tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoElectronTrack_absZ0sig":          {"name":"RecoElectronTrack_absZ0sig",  "title":"Reco electron tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoElectronTrack_absZ0sig_prompt":   {"name":"RecoElectronTrack_absZ0sig",  "title":"Reco electron tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoElectronTrack_D0cov":      {"name":"RecoElectronTrack_D0cov",     "title":"Reco electron tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoElectronTrack_Z0cov":      {"name":"RecoElectronTrack_Z0cov",     "title":"Reco electron tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    #"RecoPhoton_e":        {"name":"RecoPhoton_e",        "title":"Reco photon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    #"RecoPhoton_p":        {"name":"RecoPhoton_p",        "title":"Reco photon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    #"RecoPhoton_pt":       {"name":"RecoPhoton_pt",       "title":"Reco photon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoPhoton_pz":       {"name":"RecoPhoton_pz",       "title":"Reco photon p_{z} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    #"RecoPhoton_eta":      {"name":"RecoPhoton_eta",      "title":"Reco photon #eta",         "bin":60, "xmin":-3,"xmax":3},
    #"RecoPhoton_theta":    {"name":"RecoPhoton_theta",    "title":"Reco photon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    #"RecoPhoton_phi":      {"name":"RecoPhoton_phi",      "title":"Reco photon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    #"RecoPhoton_charge":   {"name":"RecoPhoton_charge",   "title":"Reco photon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMuon_e":        {"name":"RecoMuon_e",        "title":"Reco muon energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_p":        {"name":"RecoMuon_p",        "title":"Reco muon p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_pt":       {"name":"RecoMuon_pt",       "title":"Reco muon p_{T} [GeV]",  "bin":100,"xmin":0 ,"xmax":50},
    "RecoMuon_px":       {"name":"RecoMuon_px",       "title":"Reco muon p_{x} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    "RecoMuon_py":       {"name":"RecoMuon_py",       "title":"Reco muon p_{y} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    "RecoMuon_pz":       {"name":"RecoMuon_pz",       "title":"Reco muon p_{z} [GeV]",  "bin":100,"xmin":-50 ,"xmax":50},
    "RecoMuon_eta":      {"name":"RecoMuon_eta",      "title":"Reco muon #eta",         "bin":60, "xmin":-3,"xmax":3},
    "RecoMuon_theta":    {"name":"RecoMuon_theta",    "title":"Reco muon #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "RecoMuon_phi":      {"name":"RecoMuon_phi",      "title":"Reco muon #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},
    #"RecoMuon_charge":   {"name":"RecoMuon_charge",   "title":"Reco muon charge",       "bin":3, "xmin":-1.5,"xmax":1.5},

    "RecoMuonTrack_absD0":             {"name":"RecoMuonTrack_absD0",     "title":"Reco muon tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonnTrack_absD0_med":        {"name":"RecoMuonTrack_absD0",     "title":"Reco muon tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":10},
    "RecoMuonTrack_absD0_prompt":      {"name":"RecoMuonTrack_absD0",     "title":"Reco muon tracks |d_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoMuonTrack_absZ0":             {"name":"RecoMuonTrack_absZ0",     "title":"Reco muon tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":2000},
    "RecoMuonTrack_absZ0_prompt":      {"name":"RecoMuonTrack_absZ0",     "title":"Reco muon tracks |z_{0}| [mm]",      "bin":100,"xmin":0, "xmax":1},
    "RecoMuonTrack_absD0sig":          {"name":"RecoMuonTrack_absD0sig",  "title":"Reco muon tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_absD0sig_prompt":   {"name":"RecoMuonTrack_absD0sig",  "title":"Reco muon tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoMuonTrack_absD0sig_med":      {"name":"RecoMuonTrack_absD0sig",  "title":"Reco muon tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    "RecoMuonTrack_absZ0sig":          {"name":"RecoMuonTrack_absZ0sig",  "title":"Reco muon tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "RecoMuonTrack_absZ0sig_prompt":   {"name":"RecoMuonTrack_absZ0sig",  "title":"Reco muon tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "RecoMuonTrack_D0cov":      {"name":"RecoMuonTrack_D0cov",     "title":"Reco muon tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "RecoMuonTrack_Z0cov":      {"name":"RecoMuonTrack_Z0cov",     "title":"Reco muon tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    
    "Reco_DecayVertexLepton_x":           {"name":"RecoDecayVertexLepton.position.x",  "title":"Reco decay lepton vertex x [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "Reco_DecayVertexLepton_y":           {"name":"RecoDecayVertexLepton.position.y",  "title":"Reco decay lepton vertex y [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "Reco_DecayVertexLepton_z":           {"name":"RecoDecayVertexLepton.position.z",  "title":"Reco decay lepton vertex z [mm]",            "bin":100,"xmin":-1000 ,"xmax":1000},
    "Reco_DecayVertexLepton_x_prompt":    {"name":"RecoDecayVertexLepton.position.x",  "title":"Reco decay lepton vertex x [mm]",            "bin":100,"xmin":-1 ,"xmax":1},
    "Reco_DecayVertexLepton_y_prompt":    {"name":"RecoDecayVertexLepton.position.y",  "title":"Reco decay lepton vertex y [mm]",            "bin":100,"xmin":-1 ,"xmax":1},
    "Reco_DecayVertexLepton_z_prompt":    {"name":"RecoDecayVertexLepton.position.z",  "title":"Reco decay lepton vertex z [mm]",            "bin":100,"xmin":-1 ,"xmax":1},
    "Reco_DecayVertexLepton_chi2":        {"name":"RecoDecayVertexLepton.chi2",        "title":"Reco decay lepton vertex #chi^{2}",          "bin":100,"xmin":0 ,"xmax":3},
    "Reco_DecayVertexLepton_probability": {"name":"RecoDecayVertexLepton.probability", "title":"Reco decay lepton vertex probability",       "bin":100,"xmin":0 ,"xmax":10},

    "Reco_Lxy":                     {"name":"Reco_Lxy",                    "title":"Reco L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":2000},
    "Reco_Lxy_prompt":              {"name":"Reco_Lxy",                    "title":"Reco L_{xy} [mm]",     "bin":100,"xmin":0 ,"xmax":2},
    "Reco_Lxyz":                    {"name":"Reco_Lxyz",                   "title":"Reco L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":2000},
    "Reco_Lxyz_prompt":             {"name":"Reco_Lxyz",                   "title":"Reco L_{xyz} [mm]",    "bin":100,"xmin":0 ,"xmax":10},
    
    "Reco_invMass":   {"name":"Reco_invMass",   "title":"Reco M(l,l') [GeV]",           "bin":100,"xmin":0, "xmax":100},

    ### range and binning of cos and DR changed to do combine analysis ###
    #"Reco_cos":   {"name":"Reco_cos",   "title":"Reco cos#theta(l,l')",           "bin":20,"xmin":-0.8, "xmax":0.8},
    #"Reco_DR":   {"name":"Reco_DR",   "title":"Reco #Delta R(l,l')",           "bin":20,"xmin":0.5, "xmax":7},
    "Reco_cos":   {"name":"Reco_cos",   "title":"Reco cos#theta(l,l')",           "bin":100,"xmin":-1., "xmax":1.},
    "Reco_DR":   {"name":"Reco_DR",   "title":"Reco #Delta R(l,l')",           "bin":100,"xmin":0, "xmax":10},

    "Reco_e":                   {"name":"Reco_e",        "title":"Reco lepton energy [GeV]", "bin":100,"xmin":0 ,"xmax":50},
    "Reco_p":                   {"name":"Reco_p",        "title":"Reco lepton p [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "Reco_pt":                  {"name":"Reco_pt",        "title":"Reco lepton p_{T} [GeV]",      "bin":100,"xmin":0 ,"xmax":50},
    "Reco_px":                  {"name":"Reco_px",        "title":"Reco lepton p_{x} [GeV]",      "bin":100,"xmin":-50 ,"xmax":50},
    "Reco_py":                  {"name":"Reco_py",        "title":"Reco lepton p_{y} [GeV]",      "bin":100,"xmin":-50 ,"xmax":50},
    "Reco_pz":                  {"name":"Reco_pz",        "title":"Reco lepton p_{z} [GeV]",      "bin":100,"xmin":-50 ,"xmax":50},
    "Reco_eta":                 {"name":"Reco_eta",      "title":"Reco lepton #eta",         "bin":60, "xmin":-3,"xmax":3},
    "Reco_theta":               {"name":"Reco_theta",    "title":"Reco lepton #theta",       "bin":64, "xmin":0,"xmax":3.2},
    "Reco_phi":                 {"name":"Reco_phi",      "title":"Reco lepton #phi",         "bin":64, "xmin":-3.2,"xmax":3.2},

    "Reco_absD0_prompt":        {"name":"Reco_absD0",        "title":"Reco lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":1},
    "Reco_absZ0_prompt":        {"name":"Reco_absZ0",        "title":"Reco lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":1},
    "Reco_absD0_med":           {"name":"Reco_absD0",        "title":"Reco lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":10},
    "Reco_absZ0_med":           {"name":"Reco_absZ0",        "title":"Reco lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":10},
    "Reco_absD0":               {"name":"Reco_absD0",        "title":"Reco lepton |d_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":2000},
    "Reco_absZ0":               {"name":"Reco_absZ0",        "title":"Reco lepton |z_{0}| [mm]",      "bin":100,"xmin":0 ,"xmax":2000},
    "Reco_absD0sig":          {"name":"Reco_absD0sig",  "title":"Reco lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "Reco_absD0sig_med":      {"name":"Reco_absD0sig",  "title":"Reco lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    "Reco_absD0sig_prompt":   {"name":"Reco_absD0sig",  "title":"Reco lepton tracks |d_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "Reco_absZ0sig":          {"name":"Reco_absZ0sig",  "title":"Reco lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":600000},
    "Reco_absZ0sig_prompt":   {"name":"Reco_absZ0sig",  "title":"Reco lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":5},
    "Reco_absZ0sig_med":      {"name":"Reco_absZ0sig",  "title":"Reco lepton tracks |z_{0} significance|",      "bin":100,"xmin":0, "xmax":1000},
    "Reco_D0cov":      {"name":"Reco_D0cov",     "title":"Reco lepton tracks d_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},
    "Reco_Z0cov":      {"name":"Reco_Z0cov",     "title":"Reco lepton tracks z_{0} #sigma^{2}",      "bin":100,"xmin":0, "xmax":0.5},

    "RecoMissingEnergy_e":       {"name":"RecoMissingEnergy_e",       "title":"Reco Total Missing Energy [GeV]",    "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_p":       {"name":"RecoMissingEnergy_p",       "title":"Reco Total Missing p [GeV]",         "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_pt":      {"name":"RecoMissingEnergy_pt",      "title":"Reco Missing p_{T} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_px":      {"name":"RecoMissingEnergy_px",      "title":"Reco Missing p_{x} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_py":      {"name":"RecoMissingEnergy_py",      "title":"Reco Missing p_{y} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_pz":      {"name":"RecoMissingEnergy_pz",      "title":"Reco Missing p_{z} [GeV]",           "bin":100,"xmin":0 ,"xmax":50},
    "RecoMissingEnergy_eta":     {"name":"RecoMissingEnergy_eta",     "title":"Reco Missing Energy #eta",           "bin":60,"xmin":-3 ,"xmax":3},
    "RecoMissingEnergy_theta":   {"name":"RecoMissingEnergy_theta",   "title":"Reco Missing Energy #theta",         "bin":64,"xmin":0 , "xmax":3.2},
    "RecoMissingEnergy_phi":     {"name":"RecoMissingEnergy_phi",     "title":"Reco Missing Energy #phi",           "bin":64,"xmin":-3.2 ,"xmax":3.2},

}
