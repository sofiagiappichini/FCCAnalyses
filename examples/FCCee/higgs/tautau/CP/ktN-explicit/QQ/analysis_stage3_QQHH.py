import os, copy # tagging
import ROOT

### it's best to process stage3 in batch because some files will be empty and it will abort everything but in batch it aborts only the respective jobs

inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/stage1_250530/ktN-explicit/QQ/HH"

#Optional: output directory, default is local running directory
outputDir   = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/BDT_250530/ktN-explicit/QQ/HH" 

#Mandatory: List of processes

processList = {

    "p8_ee_bbH_Htautau_CPeven":{},
    "p8_ee_bbH_Htautau_CPodd":{},
    "p8_ee_bbH_Htautau_CPmix":{},
    "p8_ee_ccH_Htautau_CPeven":{},
    "p8_ee_ccH_Htautau_CPodd":{},
    "p8_ee_ccH_Htautau_CPmix":{},
    "p8_ee_eeH_Htautau_CPeven":{},
    "p8_ee_eeH_Htautau_CPodd":{},
    "p8_ee_eeH_Htautau_CPmix":{},
    "p8_ee_mumuH_Htautau_CPeven":{},
    "p8_ee_mumuH_Htautau_CPodd":{},
    "p8_ee_mumuH_Htautau_CPmix":{},
    "p8_ee_ssH_Htautau_CPeven":{},
    "p8_ee_ssH_Htautau_CPodd":{},
    "p8_ee_ssH_Htautau_CPmix":{},
    "p8_ee_qqH_Htautau_CPeven":{},
    "p8_ee_qqH_Htautau_CPodd":{},
    "p8_ee_qqH_Htautau_CPmix":{},

    'p8_ee_WW_ecm240':{'chunks':3740},
    'p8_ee_Zqq_ecm240':{'chunks':1007},
    'p8_ee_ZZ_ecm240':{'chunks':1000},
    
    'wzp6_ee_tautau_ecm240':{'chunks':1000},
    'wzp6_ee_mumu_ecm240':{'chunks':1000},
    'wzp6_ee_ee_Mee_30_150_ecm240':{'chunks':1000},

    'wzp6_ee_tautauH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_HZZ_ecm240': {'chunks':100},

    'wzp6_egamma_eZ_Zmumu_ecm240': {'chunks':1000},
    'wzp6_egamma_eZ_Zee_ecm240': {'chunks':1000},
    'wzp6_gammae_eZ_Zmumu_ecm240': {'chunks':1000},
    'wzp6_gammae_eZ_Zee_ecm240': {'chunks':1000},

    'wzp6_gaga_tautau_60_ecm240': {'chunks':1000},
    'wzp6_gaga_mumu_60_ecm240': {'chunks':1000},
    'wzp6_gaga_ee_60_ecm240': {'chunks':1000},

    'wzp6_ee_nuenueZ_ecm240': {'chunks':1000},
    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_eeH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_eeH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_eeH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_eeH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_eeH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_eeH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_eeH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_bbH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_bbH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_bbH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_bbH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_bbH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_bbH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_bbH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_ccH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_ccH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_ccH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_ccH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_ccH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_ccH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_ccH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_ssH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_ssH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_ssH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_ssH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_ssH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_ssH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_ssH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_qqH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_qqH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_qqH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_qqH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_qqH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_qqH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_qqH_HZZ_ecm240': {'chunks':100},
}

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional running on HTCondor, default is False
runBatch = True

nCPUS = 6

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RBDT<> bdt("Htautau", "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/BDT_250502/ktN-explicit/xgb_bdt_ktN-explicit_QQHH.root");
                                computeModel = TMVA::Experimental::Compute<23, float>(bdt);''') #needs to be passed the number of variables

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):
        df2 = (df

                .Filter("Collinear_mass>100 && Collinear_mass<150")

                #recast some of the varibales to be all the same type
                .Define("fRecoEmiss_costheta",       "static_cast<float>(RecoEmiss_costheta)")
                .Define("fRecoZ_pz",       "static_cast<float>(RecoZ_pz)")
                .Define("fRecoZ_pt",       "static_cast<float>(RecoZ_pt)")
                .Define("fRecoZ_p",       "static_cast<float>(RecoZ_p)")
                .Define("fRecoZ_e",       "static_cast<float>(RecoZ_e)")
                .Define("fRecoZ_eta",       "static_cast<float>(RecoZ_eta)")
                .Define("fRecoZ_mass",       "static_cast<float>(RecoZ_mass)")
                .Define("fRecoH_pz",       "static_cast<float>(RecoH_pz)")
                .Define("fRecoH_pt",       "static_cast<float>(RecoH_pt)")
                .Define("fRecoH_p",       "static_cast<float>(RecoH_p)")
                .Define("fRecoH_e",       "static_cast<float>(RecoH_e)")
                .Define("fRecoH_eta",       "static_cast<float>(RecoH_eta)")
                .Define("fRecoH_mass",       "static_cast<float>(RecoH_mass)")
                #.Define("fTauLead_type",       "static_cast<float>(TauLead_type)")
                #.Define("fn_TauLead_charged_constituents",       "static_cast<float>(n_TauLead_charged_constituents)")
                #.Define("fn_TauLead_neutral_constituents",       "static_cast<float>(n_TauLead_neutral_constituents)")
                #.Define("fTauSub_type",       "static_cast<float>(TauSub_type)")
                #.Define("fn_TauSub_charged_constituents",       "static_cast<float>(n_TauSub_charged_constituents)")
                #.Define("fn_TauSub_neutral_constituents",       "static_cast<float>(n_TauSub_neutral_constituents)")
                .Define("fTau_DPhi",       "static_cast<float>(Tau_DPhi)")
                .Define("fTau_DR",       "static_cast<float>(Tau_DR)")
                .Define("fTau_cos",       "static_cast<float>(Tau_cos)")
                .Define("fTau_DEta",       "static_cast<float>(Tau_DEta)")
                .Define("fRecoil_mass",       "static_cast<float>(Recoil_mass)")
                .Define("fCollinear_mass",       "static_cast<float>(Collinear_mass)")

                ##### variable lists need to have the same order of variables used in the training to work properly, renaming them is ok
                .Define("BDT_pred", ROOT.computeModel, ["RecoEmiss_pz",
                                                        "RecoEmiss_pt",
                                                        "RecoEmiss_p",
                                                        "RecoEmiss_e",
                                                        "fRecoEmiss_costheta",
                                                        "fRecoZ_pz",
                                                        "fRecoZ_p",
                                                        "fRecoZ_pt",
                                                        "fRecoZ_e",
                                                        "fRecoZ_eta",
                                                        "fRecoZ_mass",
                                                        "fRecoH_pz",
                                                        "fRecoH_p",
                                                        "fRecoH_pt",
                                                        "fRecoH_e",
                                                        "fRecoH_eta",
                                                        "fRecoH_mass",
                                                        #"fTauLead_type",
                                                        #"fn_TauLead_charged_constituents",
                                                        #"fn_TauLead_neutral_constituents",
                                                        #"fTauSub_type",
                                                        #"fn_TauSub_charged_constituents",
                                                        #"fn_TauSub_neutral_constituents",
                                                        "fTau_DPhi",
                                                        "fTau_DR",
                                                        "fTau_cos",
                                                        "fTau_DEta",
                                                        "fRecoil_mass",
                                                        "fCollinear_mass"])

                .Define("BDT_score",        "BDT_pred.at(0)")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        #branches from stage1 to be kept for histogram booking in final and plotting
        branchList = [

            ######## Reconstructed particles #######

            "n_RecoElectrons",
            "RecoElectron_e",
            "RecoElectron_p",
            "RecoElectron_pt",
            "RecoElectron_px",
            "RecoElectron_py",
            "RecoElectron_pz",
            "RecoElectron_y",
            "RecoElectron_eta",
            "RecoElectron_theta",
            "RecoElectron_phi",
            "RecoElectron_charge",
            "RecoElectron_mass",
            "RecoElectronTrack_absD0",
            "RecoElectronTrack_absZ0",
            "RecoElectronTrack_absD0sig",
            "RecoElectronTrack_absZ0sig",
            "RecoElectronTrack_D0cov",
            "RecoElectronTrack_Z0cov",

            "n_RecoElectrons_sel",
            "RecoElectron_sel_e",
            "RecoElectron_sel_p",
            "RecoElectron_sel_pt",
            "RecoElectron_sel_px",
            "RecoElectron_sel_py",
            "RecoElectron_sel_pz",
            "RecoElectron_sel_y",
            "RecoElectron_sel_eta",
            "RecoElectron_sel_theta",
            "RecoElectron_sel_phi",
            "RecoElectron_sel_charge",
            "RecoElectron_sel_mass",
            "RecoElectronTrack_sel_absD0",
            "RecoElectronTrack_sel_absZ0",
            "RecoElectronTrack_sel_absD0sig",
            "RecoElectronTrack_sel_absZ0sig",
            "RecoElectronTrack_sel_D0cov",
            "RecoElectronTrack_sel_Z0cov",

            "n_RecoMuons",
            "RecoMuon_e",
            "RecoMuon_p",
            "RecoMuon_pt",
            "RecoMuon_px",
            "RecoMuon_py",
            "RecoMuon_pz",
            "RecoMuon_y",
            "RecoMuon_eta",
            "RecoMuon_theta",
            "RecoMuon_phi",
            "RecoMuon_charge",
            "RecoMuon_mass",
            "RecoMuonTrack_absD0",
            "RecoMuonTrack_absZ0",
            "RecoMuonTrack_absD0sig",
            "RecoMuonTrack_absZ0sig",
            "RecoMuonTrack_D0cov",
            "RecoMuonTrack_Z0cov",

            "n_RecoMuons_sel",
            "RecoMuon_sel_e",
            "RecoMuon_sel_p",
            "RecoMuon_sel_pt",
            "RecoMuon_sel_px",
            "RecoMuon_sel_py",
            "RecoMuon_sel_pz",
            "RecoMuon_sel_y",
            "RecoMuon_sel_eta",
            "RecoMuon_sel_theta",
            "RecoMuon_sel_phi",
            "RecoMuon_sel_charge",
            "RecoMuon_sel_mass",
            "RecoMuonTrack_sel_absD0",
            "RecoMuonTrack_sel_absZ0",
            "RecoMuonTrack_sel_absD0sig",
            "RecoMuonTrack_sel_absZ0sig",
            "RecoMuonTrack_sel_D0cov",
            "RecoMuonTrack_sel_Z0cov",

            "n_RecoLeptons",
            "RecoLepton_e",
            "RecoLepton_p",
            "RecoLepton_pt",
            "RecoLepton_px",
            "RecoLepton_py",
            "RecoLepton_pz",
            "RecoLepton_y",
            "RecoLepton_eta",
            "RecoLepton_theta",
            "RecoLepton_phi",
            "RecoLepton_charge",
            "RecoLepton_mass",
            "RecoLeptonTrack_absD0",
            "RecoLeptonTrack_absZ0",
            "RecoLeptonTrack_absD0sig",
            "RecoLeptonTrack_absZ0sig",
            "RecoLeptonTrack_D0cov",
            "RecoLeptonTrack_Z0cov",

            "n_RecoLeptons_sel",
            "RecoLepton_sel_e",
            "RecoLepton_sel_p",
            "RecoLepton_sel_pt",
            "RecoLepton_sel_px",
            "RecoLepton_sel_py",
            "RecoLepton_sel_pz",
            "RecoLepton_sel_y",
            "RecoLepton_sel_eta",
            "RecoLepton_sel_theta",
            "RecoLepton_sel_phi",
            "RecoLepton_sel_charge",
            "RecoLepton_sel_mass",
            "RecoLeptonTrack_sel_absD0",
            "RecoLeptonTrack_sel_absZ0",
            "RecoLeptonTrack_sel_absD0sig",
            "RecoLeptonTrack_sel_absZ0sig",
            "RecoLeptonTrack_sel_D0cov",
            "RecoLeptonTrack_sel_Z0cov",

            "n_RecoPhotons",
            "RecoPhoton_e",
            "RecoPhoton_p",
            "RecoPhoton_pt",
            "RecoPhoton_px",
            "RecoPhoton_py",
            "RecoPhoton_pz",
            "RecoPhoton_y",
            "RecoPhoton_eta",
            "RecoPhoton_theta",
            "RecoPhoton_phi",
            "RecoPhoton_charge",
            "RecoPhoton_mass",

            "RecoEmiss_px",
            "RecoEmiss_py",
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",
            "RecoEmiss_eta",
            "RecoEmiss_phi",
            "RecoEmiss_theta",
            "RecoEmiss_y",
            "RecoEmiss_costheta",

            #"Jets_kt4_px", 
            #"Jets_kt4_py",    
            #"Jets_kt4_pz",      
            #"Jets_kt4_p",  
            #"Jets_kt4_pt",    
            #"Jets_kt4_phi", 
            #"Jets_kt4_eta",     
            #"Jets_kt4_theta",          
            #"Jets_kt4_e",     
            #"Jets_kt4_mass",   
            #"n_Jets_kt4_constituents",   
            #"n_Jets_kt4_charged_constituents",   
            #"n_Jets_kt4_neutral_constituents",   
            #"n_Jets_kt4",      

            "TauFromJet_kt4_p",
            "TauFromJet_kt4_pt",
            "TauFromJet_kt4_px",
            "TauFromJet_kt4_py",
            "TauFromJet_kt4_pz",
            "TauFromJet_kt4_theta",
            "TauFromJet_kt4_phi",
            "TauFromJet_kt4_e",
            "TauFromJet_kt4_eta",
            "TauFromJet_kt4_y",
            "TauFromJet_kt4_charge",
            "TauFromJet_kt4_type",
            "TauFromJet_kt4_mass",
            "n_TauFromJet_kt4",

            #"Jets_kt4_sel_e",     
            #"Jets_kt4_sel_p",     
            #"Jets_kt4_sel_pt",     
            #"Jets_kt4_sel_px",   
            #"Jets_kt4_sel_py",   
            #"Jets_kt4_sel_pz",     
            #"Jets_kt4_sel_eta",    
            #"Jets_kt4_sel_theta",   
            #"Jets_kt4_sel_phi",     
            #"Jets_kt4_sel_mass",      
            #"n_Jets_kt4_sel",

        ]
        #complex variables added here at stage2
        branchList += [


            "RecoZ_px",
            "RecoZ_py",
            "RecoZ_pz",
            "RecoZ_p",
            "RecoZ_pt",
            "RecoZ_e",
            "RecoZ_eta",
            "RecoZ_phi",
            "RecoZ_theta",
            "RecoZ_y",
            "RecoZ_mass",
            "RecoZ1_consituents", 
            "RecoZ2_consituents", 
            "RecoZ1_charged_consituents",   
            "RecoZ2_charged_consituents",  
            "RecoZ1_neutral_consituents",   
            "RecoZ2_neutral_consituents",   

            "RecoZLead_px", 
            "RecoZLead_py",   
            "RecoZLead_pz",   
            "RecoZLead_p",    
            "RecoZLead_pt",   
            "RecoZLead_e",    
            "RecoZLead_eta",    
            "RecoZLead_phi",    
            "RecoZLead_theta",   
            "RecoZLead_y",     
            "RecoZLead_mass",   

            "RecoZSub_px",    
            "RecoZSub_py",   
            "RecoZSub_pz",   
            "RecoZSub_p",   
            "RecoZSub_pt",  
            "RecoZSub_e",     
            "RecoZSub_eta",   
            "RecoZSub_phi",   
            "RecoZSub_theta",    
            "RecoZSub_y",    
            "RecoZSub_mass",   

            "RecoH_px",
            "RecoH_py",
            "RecoH_pz",
            "RecoH_p",
            "RecoH_pt",
            "RecoH_e",
            "RecoH_eta",
            "RecoH_phi",
            "RecoH_theta",
            "RecoH_y",
            "RecoH_mass",

            "TauLead_px",    
            "TauLead_py",   
            "TauLead_pz",   
            "TauLead_p",   
            "TauLead_pt",   
            "TauLead_e",    
            "TauLead_eta",    
            "TauLead_phi",    
            "TauLead_theta",    
            "TauLead_y",    
            "TauLead_mass",
            "TauLead_type",

            "TauSub_px",    
            "TauSub_py",   
            "TauSub_pz",   
            "TauSub_p",   
            "TauSub_pt",   
            "TauSub_e",    
            "TauSub_eta",    
            "TauSub_phi",    
            "TauSub_theta",    
            "TauSub_y",    
            "TauSub_mass",
            "TauSub_type",

            "TauP_px",    
            "TauP_py",   
            "TauP_pz",   
            "TauP_p",   
            "TauP_pt",   
            "TauP_e",    
            "TauP_eta",    
            "TauP_phi",    
            "TauP_theta",    
            "TauP_y",    
            "TauP_mass",
            "TauP_type",

            "TauM_px",    
            "TauM_py",   
            "TauM_pz",   
            "TauM_p",   
            "TauM_pt",   
            "TauM_e",    
            "TauM_eta",    
            "TauM_phi",    
            "TauM_theta",    
            "TauM_y",    
            "TauM_mass",
            "TauM_type",

            "Recoil_mass",
            "Collinear_mass", 
            #"Collinear_mass_3d",
        
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta", 
            "Tau_DPhi",
            
            "RecoZDaughter_DR", 
            "RecoZDaughter_cos", 
            "RecoZDaughter_DEta", 
            "RecoZDaughter_DPhi", 
        ]
        branchList += [

            "RecoPiP_px",
            "RecoPiP_py",
            "RecoPiP_pz",
            "RecoPiP_e",
            "RecoPiP_phi",
            "RecoPiP_eta",
            "RecoPiP_theta",
            "RecoPiP_dx",
            "RecoPiP_dy",
            "RecoPiP_dz",
            "RecoPiP_D0",
            "RecoPiP_Z0",
            "RecoPiP_p",
            "RecoPiP_D0sig",
            "RecoPiP_Z0sig",
            "RecoPiP_charge",

            "RecoPiM_px",
            "RecoPiM_py",
            "RecoPiM_pz",
            "RecoPiM_dx",
            "RecoPiM_dy",
            "RecoPiM_dz",
            "RecoPiM_e",
            "RecoPiM_p",
            "RecoPiM_phi",
            "RecoPiM_eta",
            "RecoPiM_theta",
            "RecoPiM_D0",
            "RecoPiM_Z0",
            "RecoPiM_D0sig",
            "RecoPiM_Z0sig",
            "RecoPiM_charge",

            "RecoPi0P_px",
            "RecoPi0P_py",
            "RecoPi0P_pz",
            "RecoPi0P_e",
            "RecoPi0P_phi",
            "RecoPi0P_eta",
            "RecoPi0P_theta",

            "RecoPi0M_px",
            "RecoPi0M_py",
            "RecoPi0M_pz",
            "RecoPi0M_e",
            "RecoPi0M_phi",
            "RecoPi0M_eta",
            "RecoPi0M_theta",

            "ZMF_px",
            "ZMF_py",
            "ZMF_pz",
            "ZMF_e",

            "OP_ImpactP_px",
            "OP_ImpactP_py",
            "OP_ImpactP_pz",
            "OP_ImpactP_e",

            "OP_ImpactM_px",
            "OP_ImpactM_py",
            "OP_ImpactM_pz",
            "OP_ImpactM_e",

            "ZMF_RecoPiP_px",
            "ZMF_RecoPiP_py",
            "ZMF_RecoPiP_pz",
            "ZMF_RecoPiP_e",

            "ZMF_RecoPiM_px",
            "ZMF_RecoPiM_py",
            "ZMF_RecoPiM_pz",
            "ZMF_RecoPiM_e",

            "ZMF_LambdaP_px",
            "ZMF_LambdaP_py",
            "ZMF_LambdaP_pz",
            "ZMF_LambdaP_e",

            "ZMF_LambdaP_perp_x",
            "ZMF_LambdaP_perp_y",
            "ZMF_LambdaP_perp_z",

            "ZMF_LambdaM_px",
            "ZMF_LambdaM_py",
            "ZMF_LambdaM_pz",
            "ZMF_LambdaM_e",

            "ZMF_LambdaM_perp_x",
            "ZMF_LambdaM_perp_y",
            "ZMF_LambdaM_perp_z",

            "y_tau",
            "y_plus",
            "y_min",
            "Phi_ZMF",
            "O_ZMF",   
            "PhiCP_y",   
            "PhiCP_CMS",

            #"CosDeltaPhiILC", 
            #"SinDeltaPhiILC", 
            #"DeltaPhiILC",
            #"KinILC_chi2",
            #"ILC_Filter", 

            #"KinILC_H_mass",

            "BDT_score",

        ]

        return branchList