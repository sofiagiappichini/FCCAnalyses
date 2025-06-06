import os, copy # tagging
import ROOT

### it's best to process stage3 in batch because some files will be empty and it will abort everything but in batch it aborts only the respective jobs

inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/stage1_250502/ktN-tag/LL/LL/"

#Optional: output directory, default is local running directory
outputDir   = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/BDT_250502/ktN-tag/stage3/LL/LL/" 

#Mandatory: List of processes
processList = {

    'p8_ee_WW_ecm365':{'chunks':100000},
    'p8_ee_WW_tautau_ecm365':{'chunks':100000},
    'p8_ee_Zqq_ecm365':{'chunks':10000},
    'p8_ee_ZZ_ecm365':{'chunks':1000},
    'p8_ee_Zbb_ecm365':{'chunks':1000},
    'p8_ee_Zcc_ecm365':{'chunks':1000},
    'p8_ee_Zss_ecm365':{'chunks':1000},
    'p8_ee_tt_ecm365':{'chunks':1000},
    
    'wzp6_ee_tautau_ecm365':{'chunks':1000},
    'wzp6_ee_mumu_ecm365':{'chunks':1000},
    'wzp6_ee_ee_Mee_30_150_ecm365':{'chunks':1000},

    'wzp6_ee_tautauH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_tautauH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_tautauH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_tautauH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_tautauH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_tautauH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_tautauH_HZZ_ecm365': {'chunks':100},

    'wzp6_egamma_eZ_Zmumu_ecm365': {'chunks':1000},
    'wzp6_egamma_eZ_Zee_ecm365': {'chunks':1000},
    'wzp6_gammae_eZ_Zmumu_ecm365': {'chunks':1000},
    'wzp6_gammae_eZ_Zee_ecm365': {'chunks':1000},

    'wzp6_gaga_tautau_60_ecm365': {'chunks':1000},
    'wzp6_gaga_mumu_60_ecm365': {'chunks':1000},
    'wzp6_gaga_ee_60_ecm365': {'chunks':1000},

    'wzp6_ee_nuenueZ_ecm365': {'chunks':1000},
    'wzp6_ee_nunuH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_nunuH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_nunuH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_nunuH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_nunuH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_nunuH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_nunuH_HZZ_ecm365': {'chunks':100},

    'wzp6_ee_eeH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_eeH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_eeH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_eeH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_eeH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_eeH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_eeH_HZZ_ecm365': {'chunks':100},

    'wzp6_ee_mumuH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_mumuH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_mumuH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_mumuH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_mumuH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_mumuH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_mumuH_HZZ_ecm365': {'chunks':100},

    'wzp6_ee_bbH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_bbH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_bbH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_bbH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_bbH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_bbH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_bbH_HZZ_ecm365': {'chunks':100},

    'wzp6_ee_ccH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_ccH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_ccH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_ccH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_ccH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_ccH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_ccH_HZZ_ecm365': {'chunks':100},

    'wzp6_ee_ssH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_ssH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_ssH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_ssH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_ssH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_ssH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_ssH_HZZ_ecm365': {'chunks':100},

    'wzp6_ee_qqH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_qqH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_qqH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_qqH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_qqH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_qqH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_qqH_HZZ_ecm365': {'chunks':100},

    'wzp6_ee_nuenueH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_nuenueH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_nuenueH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_nuenueH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_nuenueH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_nuenueH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_nuenueH_HZZ_ecm365': {'chunks':100},  

    'wzp6_ee_numunumuH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_numunumuH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_numunumuH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_numunumuH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_numunumuH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_numunumuH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_numunumuH_HZZ_ecm365': {'chunks':100},  

    'wzp6_ee_VBF_nunuH_Htautau_ecm365': {'chunks':100},
    'wzp6_ee_VBF_nunuH_Hbb_ecm365': {'chunks':100},
    'wzp6_ee_VBF_nunuH_Hcc_ecm365': {'chunks':100},
    'wzp6_ee_VBF_nunuH_Hss_ecm365': {'chunks':100},
    'wzp6_ee_VBF_nunuH_Hgg_ecm365': {'chunks':100},
    'wzp6_ee_VBF_nunuH_HWW_ecm365': {'chunks':100},
    'wzp6_ee_VBF_nunuH_HZZ_ecm365': {'chunks':100},
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
compGroup = "group_u_CMS.u_zh.users"

ROOT.gInterpreter.ProcessLine('''TMVA::Experimental::RBDT<> bdt("Htautau", "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/BDT_250502/ktN-tag/xgb_bdt_ktN-tag_LLLL.root");
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
                #.Define("fn_TauLead_charged_constituents",       "static_cast<float>(n_TauLead_charged_constituents)")
                #.Define("fn_TauLead_neutral_constituents",       "static_cast<float>(n_TauLead_neutral_constituents)")
                #.Define("fn_TauSub_charged_constituents",       "static_cast<float>(n_TauSub_charged_constituents)")
                #.Define("fn_TauSub_neutral_constituents",       "static_cast<float>(n_TauSub_neutral_constituents)")
                .Define("fTau_DPhi",       "static_cast<float>(Tau_DPhi)")
                .Define("fTau_DR",       "static_cast<float>(Tau_DR)")
                .Define("fTau_cos",       "static_cast<float>(Tau_cos)")
                .Define("fTau_DEta",       "static_cast<float>(Tau_DEta)")
                .Define("fRecoil",       "static_cast<float>(Recoil)")
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
                                                        "fTau_DPhi",
                                                        "fTau_DR",
                                                        "fTau_cos",
                                                        "fTau_DEta",
                                                        "fRecoil",
                                                        "fCollinear_mass"])

                .Define("BDT_score",        "BDT_pred.at(0)")
        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        #branches from stage1 to be kept for histogram booking in final and plotting
        branchList = [
            ######## Monte-Carlo particles #######
            "n_FSGenElectron",
            "FSGenElectron_e",
            "FSGenElectron_p",
            "FSGenElectron_pt",
            "FSGenElectron_px",
            "FSGenElectron_py",
            "FSGenElectron_pz",
            "FSGenElectron_y",
            "FSGenElectron_eta",
            "FSGenElectron_theta",
            "FSGenElectron_phi",
            "FSGenElectron_charge",
            "FSGenElectron_mass",
            "FSGenElectron_parentPDG",
            "FSGenElectron_vertex_x",
            "FSGenElectron_vertex_y",
            "FSGenElectron_vertex_z",

            "n_FSGenMuon",
            "FSGenMuon_e",
            "FSGenMuon_p",
            "FSGenMuon_pt",
            "FSGenMuon_px",
            "FSGenMuon_py",
            "FSGenMuon_pz",
            "FSGenMuon_y",
            "FSGenMuon_eta",
            "FSGenMuon_theta",
            "FSGenMuon_phi",
            "FSGenMuon_charge",
            "FSGenMuon_mass",
            "FSGenMuon_parentPDG",
            "FSGenMuon_vertex_x",
            "FSGenMuon_vertex_y",
            "FSGenMuon_vertex_z",

            "n_HiggsGenTau",
            "HiggsGenTau_e",
            "HiggsGenTau_p",
            "HiggsGenTau_pt",
            "HiggsGenTau_px",
            "HiggsGenTau_py",
            "HiggsGenTau_pz",
            "HiggsGenTau_y",
            "HiggsGenTau_eta",
            "HiggsGenTau_theta",
            "HiggsGenTau_phi",
            "HiggsGenTau_charge",
            "HiggsGenTau_mass",
            "HiggsGenTau_parentPDG",
            "HiggsGenTau_vertex_x",
            "HiggsGenTau_vertex_y",
            "HiggsGenTau_vertex_z",

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

            "TagJet_R5_px", 
            "TagJet_R5_py",    
            "TagJet_R5_pz",      
            "TagJet_R5_p",  
            "TagJet_R5_pt",    
            "TagJet_R5_phi", 
            "TagJet_R5_eta",     
            "TagJet_R5_theta",          
            "TagJet_R5_e",     
            "TagJet_R5_mass",        
            "TagJet_R5_charge",       
            "TagJet_R5_flavor", 
            "n_TagJet_R5_constituents",   
            "n_TagJet_R5_charged_constituents",   
            "n_TagJet_R5_neutral_constituents",   
            "n_TagJet_R5",    
            "TagJet_R5_cleanup",        

            "TagJet_R5_isG",  
            "TagJet_R5_isU",
            "TagJet_R5_isD",   
            "TagJet_R5_isS",  
            "TagJet_R5_isC",
            "TagJet_R5_isB",  
            "TagJet_R5_isTAU",

            "TauFromJet_R5_p",
            "TauFromJet_R5_pt",
            "TauFromJet_R5_px",
            "TauFromJet_R5_py",
            "TauFromJet_R5_pz",
            "TauFromJet_R5_theta",
            "TauFromJet_R5_phi",
            "TauFromJet_R5_e",
            "TauFromJet_R5_eta",
            "TauFromJet_R5_y",
            "TauFromJet_R5_charge",
            "TauFromJet_R5_type",
            "TauFromJet_R5_mass",
            "n_TauFromJet_R5",

            "TagJet_R5_sel_e",     
            "TagJet_R5_sel_p",     
            "TagJet_R5_sel_pt",     
            "TagJet_R5_sel_px",   
            "TagJet_R5_sel_py",   
            "TagJet_R5_sel_pz",     
            "TagJet_R5_sel_eta",    
            "TagJet_R5_sel_theta",   
            "TagJet_R5_sel_phi",     
            "TagJet_R5_sel_mass",      
            "n_TagJet_R5_sel", 
            

        ]
        #complex variables added here at stage2
        branchList += [
            "TauTag_px", 
            "TauTag_py",    
            "TauTag_pz",      
            "TauTag_p",  
            "TauTag_pt",    
            "TauTag_phi", 
            "TauTag_eta",     
            "TauTag_theta",          
            "TauTag_e",     
            "TauTag_mass",        
            "TauTag_charge",       
            "TauTag_flavor",       
            "n_TauTag",          
            "TauTag_isG",  
            "TauTag_isU",
            "TauTag_isD",   
            "TauTag_isS",  
            "TauTag_isC",
            "TauTag_isB",  
            "TauTag_isTAU",

            "QuarkTag_px", 
            "QuarkTag_py",    
            "QuarkTag_pz",      
            "QuarkTag_p",  
            "QuarkTag_pt",    
            "QuarkTag_phi", 
            "QuarkTag_eta",     
            "QuarkTag_theta",          
            "QuarkTag_e",     
            "QuarkTag_mass",        
            "QuarkTag_charge",       
            "QuarkTag_flavor",       
            "n_QuarkTag",          
            "QuarkTag_isG",  
            "QuarkTag_isU",
            "QuarkTag_isD",   
            "QuarkTag_isS",  
            "QuarkTag_isC",
            "QuarkTag_isB",  
            "QuarkTag_isTAU",

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
            "n_TauLead_constituents",
            "n_TauLead_charged_constituents",
            "n_TauLead_neutral_constituents",

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
            "n_TauSub_constituents",
            "n_TauSub_charged_constituents",
            "n_TauSub_neutral_constituents",

            "Recoil",
            "Collinear_mass", 
        
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta", 
            "Tau_DPhi",
            
            "RecoZDaughter_DR", 
            "RecoZDaughter_cos", 
            "RecoZDaughter_DEta", 
            "RecoZDaughter_DPhi", 

            "BDT_score",

        ]    

        return branchList