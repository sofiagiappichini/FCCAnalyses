import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    #'p8_ee_WW_ecm240':{'chunks':100},
    #'p8_ee_Zqq_ecm240':{'chunks':100},
    #'p8_ee_ZZ_ecm240':{'chunks':100},
    #'wzp6_ee_tautau_ecm240':{'chunks':100},

    #'wzp6_ee_eeH_Htautau_ecm240': {'chunks':10},
    #'wzp6_ee_eeH_Hbb_ecm240': {'chunks':10},
    #'wzp6_ee_eeH_Hcc_ecm240': {'chunks':10},
    #'wzp6_ee_eeH_Huu_ecm240': {'chunks':10},
    #'wzp6_ee_eeH_Hdd_ecm240': {'chunks':10},
    #'wzp6_ee_eeH_Hss_ecm240': {'chunks':10},
    #'wzp6_ee_eeH_Hgg_ecm240': {'chunks':10},
    #'wzp6_ee_eeH_HWW_ecm240': {'chunks':10},
    #'wzp6_ee_eeH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':10},
    #'wzp6_ee_mumuH_Hbb_ecm240': {'chunks':10},
    #'wzp6_ee_mumuH_Hcc_ecm240': {'chunks':10},
    #'wzp6_ee_mumuH_Huu_ecm240': {'chunks':10},
    #'wzp6_ee_mumuH_Hdd_ecm240': {'chunks':10},
    #'wzp6_ee_mumuH_Hss_ecm240': {'chunks':10},
    #'wzp6_ee_mumuH_Hgg_ecm240': {'chunks':10},
    #'wzp6_ee_mumuH_HWW_ecm240': {'chunks':10},
    #'wzp6_ee_mumuH_HZZ_ecm240': {'chunks':10},

    #'wzp6_ee_tautauH_Htautau_ecm240': {'chunks':10},
    #'wzp6_ee_tautauH_Hbb_ecm240': {'chunks':10},
    #'wzp6_ee_tautauH_Hcc_ecm240': {'chunks':10},
    #'wzp6_ee_tautauH_Huu_ecm240': {'chunks':10},
    #'wzp6_ee_tautauH_Hdd_ecm240': {'chunks':10},
    #'wzp6_ee_tautauH_Hss_ecm240': {'chunks':10},
    #'wzp6_ee_tautauH_Hgg_ecm240': {'chunks':10},
    #'wzp6_ee_tautauH_HWW_ecm240': {'chunks':10},
    #'wzp6_ee_tautauH_HZZ_ecm240': {'chunks':10},

    #'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Huu_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hdd_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hss_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hgg_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_HWW_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_HZZ_ecm240': {'chunks':10},

}

inputDir = "stage1/"

#Optional: output directory, default is local running directory
outputDir   = "output/" #your output directory

#Optional: ncpus, default is 4
nCPUS = 10

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional running on HTCondor, default is False
runBatch = False

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "microcentury"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):
        df2 = (df

                ### to find already made functions, this is where they are or where they can be added instead of writing them here
                ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

                ### defining filters for two hadronic taus

                .Filter("n_TauFromJet_R5==2 && n_Jets_R5_sel==0 && n_RecoLeptons==0 && (TauFromJet_R5_charge.at(0) + TauFromJet_R5_charge.at(1))==0") 

                ##################
                # Reco particles #
                ##################

                .Define("RecoEmiss_p4",  "FCCAnalyses::ZHfunctions::build_p4_single(RecoEmiss_px, RecoEmiss_py, RecoEmiss_pz, RecoEmiss_e)")
                .Define("RecoEmiss_eta",    "RecoEmiss_p4.Eta()")
                .Define("RecoEmiss_phi",    "RecoEmiss_p4.Phi()")
                .Define("RecoEmiss_theta",    "RecoEmiss_p4.Theta()")
                .Define("RecoEmiss_y",    "RecoEmiss_p4.Rapidity()")
                .Define("RecoEmiss_costheta",   "abs(std::cos(RecoEmiss_theta))")

                .Define("RecoLepton_p4",  "FCCAnalyses::ZHfunctions::build_p4(RecoLepton_px, RecoLepton_py, RecoLepton_pz, RecoLepton_e)")

                #.Define("RecoZH_idx",        "FCCAnalyses::ZHfunctions::FindBest_4(RecoLepton_p4, RecoLepton_charge, RecoLepton_mass, 91.188, 125.25)")

                #.Define("RecoZ1_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(RecoLepton_px.at(RecoZH_idx[0]), RecoLepton_py.at(RecoZH_idx[0]), RecoLepton_pz.at(RecoZH_idx[0]), RecoLepton_e.at(RecoZH_idx[0]))")
                #.Define("RecoZ2_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(RecoLepton_px.at(RecoZH_idx[1]), RecoLepton_py.at(RecoZH_idx[1]), RecoLepton_pz.at(RecoZH_idx[1]), RecoLepton_e.at(RecoZH_idx[1]))")
                
                .Define("RecoTau1_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(TauFromJet_R5_px.at(0), TauFromJet_R5_py.at(0), TauFromJet_R5_pz.at(0), TauFromJet_R5_e.at(0))")
                .Define("RecoTau2_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(TauFromJet_R5_px.at(1), TauFromJet_R5_py.at(1), TauFromJet_R5_pz.at(1), TauFromJet_R5_e.at(1))")

                #.Define("RecoZ_p4",          "RecoZ1_p4+RecoZ2_p4")
                .Define("RecoH_p4",         "RecoTau1_p4+RecoTau2_p4")

                #.Define("RecoZ_px",    "RecoZ_p4.Px()")
                #.Define("RecoZ_py",    "RecoZ_p4.Py()")
                #.Define("RecoZ_pz",    "RecoZ_p4.Pz()")
                #.Define("RecoZ_p",    "RecoZ_p4.P()")
                #.Define("RecoZ_pt",    "RecoZ_p4.Pt()")
                #.Define("RecoZ_e",     "RecoZ_p4.E()")
                #.Define("RecoZ_eta",    "RecoZ_p4.Eta()")
                #.Define("RecoZ_phi",    "RecoZ_p4.Phi()")
                #.Define("RecoZ_theta",    "RecoZ_p4.Theta()")
                #.Define("RecoZ_y",     "RecoZ_p4.Rapidity()")
                #.Define("RecoZ_mass",    "RecoZ_p4.M()")

                .Define("RecoH_px",    "RecoH_p4.Px()")
                .Define("RecoH_py",    "RecoH_p4.Py()")
                .Define("RecoH_pz",    "RecoH_p4.Pz()")
                .Define("RecoH_p",    "RecoH_p4.P()")
                .Define("RecoH_pt",    "RecoH_p4.Pt()")
                .Define("RecoH_e",     "RecoH_p4.E()")
                .Define("RecoH_eta",    "RecoH_p4.Eta()")
                .Define("RecoH_phi",    "RecoH_p4.Phi()")
                .Define("RecoH_theta",    "RecoH_p4.Theta()")
                .Define("RecoH_y",     "RecoH_p4.Rapidity()")
                .Define("RecoH_mass",    "RecoH_p4.M()")

                .Define("TauLead_p4",       "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau1_p4; else return RecoTau2_p4;")
                .Define("TauLead_px",    "TauLead_p4.Px()")
                .Define("TauLead_py",    "TauLead_p4.Py()")
                .Define("TauLead_pz",    "TauLead_p4.Pz()")
                .Define("TauLead_p",    "TauLead_p4.P()")
                .Define("TauLead_pt",    "TauLead_p4.Pt()")
                .Define("TauLead_e",     "TauLead_p4.E()")
                .Define("TauLead_eta",    "TauLead_p4.Eta()")
                .Define("TauLead_phi",    "TauLead_p4.Phi()")
                .Define("TauLead_theta",    "TauLead_p4.Theta()")
                .Define("TauLead_y",     "TauLead_p4.Rapidity()")
                .Define("TauLead_mass",    "TauLead_p4.M()")

                .Define("TauSub_p4",       "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau2_p4; else return RecoTau1_p4;")
                .Define("TauSub_px",    "TauSub_p4.Px()")
                .Define("TauSub_py",    "TauSub_p4.Py()")
                .Define("TauSub_pz",    "TauSub_p4.Pz()")
                .Define("TauSub_p",    "TauSub_p4.P()")
                .Define("TauSub_pt",    "TauSub_p4.Pt()")
                .Define("TauSub_e",     "TauSub_p4.E()")
                .Define("TauSub_eta",    "TauSub_p4.Eta()")
                .Define("TauSub_phi",    "TauSub_p4.Phi()")
                .Define("TauSub_theta",    "TauSub_p4.Theta()")
                .Define("TauSub_y",     "TauSub_p4.Rapidity()")
                .Define("TauSub_mass",    "TauSub_p4.M()")

                #.Define("Total_p4",     "FCCAnalyses::ZHfunctions::build_p4_single(0.,0.,0.,240.)")
                #.Define("Recoil",       "(Total_p4-RecoZ_p4).M()")

                .Define("p12",      "(TauLead_py*TauSub_px-TauLead_px*TauSub_py)")
                .Define("r0",       "abs((RecoEmiss_py*TauLead_px-RecoEmiss_px*TauLead_py)/p12)")
                .Define("f0",       "1./(1.+r0)")
                .Define("r1",       "abs((RecoEmiss_py*TauSub_px-RecoEmiss_px*TauSub_py)/p12)")
                .Define("f1",       "1./(1.+r1)")
                .Define("Collinear_mass",       "RecoH_mass/sqrt(f0*f1)")

                .Define("Visible_mass",     "return RecoH_mass;")

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

            #"n_ZFSGenMuon",
            #"ZFSGenMuon_e",
            #"ZFSGenMuon_p",
            #"ZFSGenMuon_pt",
            #"ZFSGenMuon_px",
            #"ZFSGenMuon_py",
            #"ZFSGenMuon_pz",
            #"ZFSGenMuon_y",
            #"ZFSGenMuon_eta",
            #"ZFSGenMuon_theta",
            #"ZFSGenMuon_phi",
            #"ZFSGenMuon_charge",
            #"ZFSGenMuon_mass",
            #"ZFSGenMuon_parentPDG",
            #"ZFSGenMuon_vertex_x",
            #"ZFSGenMuon_vertex_y",
            #"ZFSGenMuon_vertex_z",

            #"n_AllGenTau",
            #"AllGenTau_e",
            #"AllGenTau_p",
            #"AllGenTau_pt",
            #"AllGenTau_px",
            #"AllGenTau_py",
            #"AllGenTau_pz",
            #"AllGenTau_y",
            #"AllGenTau_eta",
            #"AllGenTau_theta",
            #"AllGenTau_phi",
            #"AllGenTau_charge",
            #"AllGenTau_mass",
            #"AllGenTau_parentPDG",
            #"AllGenTau_vertex_x",
            #"AllGenTau_vertex_y",
            #"AllGenTau_vertex_z",

            #"noFSRGenTau_parentPDG",

            "n_FSRGenTau",
            "FSRGenTau_e",
            "FSRGenTau_p",
            "FSRGenTau_pt",
            "FSRGenTau_px",
            "FSRGenTau_py",
            "FSRGenTau_pz",
            "FSRGenTau_y",
            "FSRGenTau_eta",
            "FSRGenTau_theta",
            "FSRGenTau_phi",
            "FSRGenTau_charge",
            "FSRGenTau_mass",
            "FSRGenTau_parentPDG",
            "FSRGenTau_vertex_x",
            "FSRGenTau_vertex_y",
            "FSRGenTau_vertex_z",

            "n_TauNeg_MuNuNu",       
            "n_TauNeg_MuNuNu_Phot",  
            "n_TauNeg_ENuNu",        
            "n_TauNeg_ENuNu_Phot",   
            "n_TauNeg_PiNu",         
            "n_TauNeg_PiNu_Phot",    
            "n_TauNeg_KNu",          
            "n_TauNeg_KNu_Phot",     
            "n_TauNeg_PiK0Nu",       
            "n_TauNeg_PiK0Nu_Phot",  
            "n_TauNeg_KK0Nu",        
            "n_TauNeg_KK0Nu_Phot",   
            "n_TauNeg_3PiNu",        
            "n_TauNeg_3PiNu_Phot",   
            "n_TauNeg_PiKKNu",       
            "n_TauNeg_PiKKNu_Phot",  

            "n_TauPos_MuNuNu",       
            "n_TauPos_MuNuNu_Phot",  
            "n_TauPos_ENuNu",        
            "n_TauPos_ENuNu_Phot",   
            "n_TauPos_PiNu",         
            "n_TauPos_PiNu_Phot",    
            "n_TauPos_KNu",          
            "n_TauPos_KNu_Phot",     
            "n_TauPos_PiK0Nu",       
            "n_TauPos_PiK0Nu_Phot",  
            "n_TauPos_KK0Nu",        
            "n_TauPos_KK0Nu_Phot",   
            "n_TauPos_3PiNu",        
            "n_TauPos_3PiNu_Phot",   
            "n_TauPos_PiKKNu",       
            "n_TauPos_PiKKNu_Phot", 

            "n_FSGenNeutrino",
            "FSGenNeutrino_e",
            "FSGenNeutrino_p",
            "FSGenNeutrino_pt",
            "FSGenNeutrino_px",
            "FSGenNeutrino_py",
            "FSGenNeutrino_pz",
            "FSGenNeutrino_y",
            "FSGenNeutrino_eta",
            "FSGenNeutrino_theta",
            "FSGenNeutrino_phi",
            "FSGenNeutrino_charge",
            #"FSGenNeutrino_parentPDG",

            "n_FSGenPhoton",
            "FSGenPhoton_e",
            "FSGenPhoton_p",
            "FSGenPhoton_pt",
            "FSGenPhoton_px",
            "FSGenPhoton_py",
            "FSGenPhoton_pz",
            "FSGenPhoton_y",
            "FSGenPhoton_eta",
            "FSGenPhoton_theta",
            "FSGenPhoton_phi",
            "FSGenPhoton_charge",
            #"FSGenPhoton_parentPDG",

            #"n_GenZ",
            #"n_GenW",
            "n_GenHiggs",
            "GenHiggs_e",
            "GenHiggs_p", 
            "GenHiggs_pt", 
            "GenHiggs_px", 
            "GenHiggs_py", 
            "GenHiggs_pz", 
            "GenHiggs_y", 
            "GenHiggs_eta", 
            "GenHiggs_theta", 
            "GenHiggs_phi", 
            "GenHiggs_charge", 

            ######## Reconstructed particles #######
            #"RecoMC_PID",

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
            "RecoElectron_PID",
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
            "RecoElectron_sel_PID",
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
            "RecoMuon_PID",
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
            "RecoMuon_sel_PID",
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
            "RecoLepton_PID",
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
            "RecoLepton_sel_PID",
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

            "RecoEmiss_px",
            "RecoEmiss_py",
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",

            "n_RecoTracks",
            #"n_RecoVertex",
            "RecoVertexObject",
            "RecoVertex",
            "n_PrimaryTracks",
            "PrimaryVertexObject",
            "PrimaryVertex", 
            "PrimaryVertex_xyz",
            "PrimaryVertes_xy",
            "n_SecondaryTracks",
            "SecondaryVertexObject",
            "SecondaryVertex",
            "SecondaryVertex_xyz",
            "SecondaryVertes_xy",
            #"VertexObject", 
            #"RecoPartPID" ,
            #"RecoPartPIDAtVertex",

            "Jets_R5_e",     
            "Jets_R5_p",     
            "Jets_R5_pt",     
            "Jets_R5_px",   
            "Jets_R5_py",   
            "Jets_R5_pz",     
            "Jets_R5_eta",    
            "Jets_R5_theta",   
            "Jets_R5_phi",     
            "Jets_R5_mass",      
            "Jets_R5_flavor",      
            "n_Jets_R5", 

            "Jets_excl4_e",     
            "Jets_excl4_p",     
            "Jets_excl4_pt",     
            "Jets_excl4_px",   
            "Jets_excl4_py",   
            "Jets_excl4_pz",     
            "Jets_excl4_eta",    
            "Jets_excl4_theta",   
            "Jets_excl4_phi",     
            "Jets_excl4_mass",      
            "Jets_excl4_flavor",      
            "n_Jets_excl4", 

            "TauFromJet_R5_tau", 
            "TauFromJet_R5_pt",
            "TauFromJet_R5_px",
            "TauFromJet_R5_py",
            "TauFromJet_R5_pz",
            "TauFromJet_R5_theta",
            "TauFromJet_R5_phi",
            "TauFromJet_R5_e",
            "TauFromJet_R5_charge",
            "TauFromJet_R5_type",
            "TauFromJet_R5_mass",
            "n_TauFromJet_R5",

            "TauFromJet_tau", 
            "TauFromJet_pt",
            "TauFromJet_px",
            "TauFromJet_py",
            "TauFromJet_pz",
            "TauFromJet_theta",
            "TauFromJet_phi",
            "TauFromJet_e",
            "TauFromJet_charge",
            "TauFromJet_type",
            "TauFromJet_mass",
            "n_TauFromJet",

            "Jets_R5_sel_e",     
            "Jets_R5_sel_p",     
            "Jets_R5_sel_pt",     
            "Jets_R5_sel_px",   
            "Jets_R5_sel_py",   
            "Jets_R5_sel_pz",     
            "Jets_R5_sel_eta",    
            "Jets_R5_sel_theta",   
            "Jets_R5_sel_phi",     
            "Jets_R5_sel_mass",      
            "Jets_R5_sel_flavor",      
            "n_Jets_R5_sel",

        ]
        #complex variables added here at stage2
        branchList += [
                "RecoEmiss_eta",
                "RecoEmiss_phi",
                "RecoEmiss_theta",
                "RecoEmiss_y",
                "RecoEmiss_costheta",

                #"RecoZ_px",
                #"RecoZ_py",
                #"RecoZ_pz",
                #"RecoZ_p",
                #"RecoZ_pt",
                #"RecoZ_e",
                #"RecoZ_eta",
                #"RecoZ_phi",
                #"RecoZ_theta",
                #"RecoZ_y",
                #"RecoZ_mass",

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

                #"Recoil",
                "Collinear_mass",
                "Visible_mass",

            ]
        return branchList