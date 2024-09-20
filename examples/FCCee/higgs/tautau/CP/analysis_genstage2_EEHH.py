import os, copy # tagging
import ROOT

EFT = True

#Mandatory: List of processes
processList_EFT = {
    'noISR_e+e-_noCuts_EWonly':{},
    'noISR_e+e-_noCuts_cehim_m1':{},
    'noISR_e+e-_noCuts_cehim_p1':{},
    'noISR_e+e-_noCuts_cehre_m1':{},
    'noISR_e+e-_noCuts_cehre_p1':{},
}

processList_xsec = {
    'p8_ee_WW_ecm240':{'chunks':100},
    'p8_ee_Zqq_ecm240':{'chunks':100},
    'p8_ee_ZZ_ecm240':{'chunks':100},
    
    'wzp6_ee_tautau_ecm240':{'chunks':100},
    'wzp6_ee_mumu_ecm240':{'chunks':100},
    'wzp6_ee_ee_Mee_30_150_ecm240':{'chunks':100},

    'wzp6_ee_tautauH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_tautauH_HZZ_ecm240': {'chunks':10},

    'wzp6_egamma_eZ_Zmumu_ecm240': {'chunks':10},
    'wzp6_egamma_eZ_Zee_ecm240': {'chunks':10},
    'wzp6_gammae_eZ_Zmumu_ecm240': {'chunks':10},
    'wzp6_gammae_eZ_Zee_ecm240': {'chunks':10},

    'wzp6_gaga_tautau_60_ecm240': {'chunks':100},
    'wzp6_gaga_mumu_60_ecm240': {'chunks':100},
    'wzp6_gaga_ee_60_ecm240': {'chunks':100},

    'wzp6_ee_nuenueZ_ecm240': {'chunks':10},

    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_eeH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_eeH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_eeH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_eeH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_eeH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_eeH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_eeH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_mumuH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_bbH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_bbH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_bbH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_bbH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_bbH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_bbH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_bbH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_ccH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_ccH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_ccH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_ccH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_ccH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_ccH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_ccH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_ssH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_ssH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_ssH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_ssH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_ssH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_ssH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_ssH_HZZ_ecm240': {'chunks':10},

    'wzp6_ee_qqH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_qqH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_qqH_Hcc_ecm240': {'chunks':10},
    'wzp6_ee_qqH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_qqH_Hgg_ecm240': {'chunks':10},
    'wzp6_ee_qqH_HWW_ecm240': {'chunks':10},
    'wzp6_ee_qqH_HZZ_ecm240': {'chunks':10},

}

inputr_xsec = "/ceph/awiedl/FCCee/HiggsCP/stage1/"

outputr_xsec   = "/ceph/awiedl/FCCee/HiggsCP/stage2/"

inputr_EFT = "/ceph/sgiappic/HiggsCP/CP/stage1"

outputr_EFT = "/ceph/sgiappic/HiggsCP/CP/stage2_Gen"

#Optional: ncpus, default is 4
nCPUS = 10

if EFT :
    processList = processList_EFT
    inputDir = inputr_EFT
    outputDir = outputr_EFT
else:
    processList = processList_xsec
    inputDir = inputDir_xsec
    outputDir = outputDir_xsec

#Optional: ncpus, default is 4
nCPUS = 10

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional running on HTCondor, default is False
runBatch = False

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "microcentury"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_Gen
compGroup = "group_u_FCC.local_Gen"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):
        df2 = (df

                ### to find already made functions, this is where they are or where they can be added instead of writing them here
                ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

                .Define("FSGenZDaughter_p4",     "FCCAnalyses::ZHfunctions::build_p4(FSGenElectron_px[abs(FSGenElectron_parentPDG)!=15], FSGenElectron_py[abs(FSGenElectron_parentPDG)!=15], FSGenElectron_pz[abs(FSGenElectron_parentPDG)!=15], FSGenElectron_e[abs(FSGenElectron_parentPDG)!=15])")
                .Define("FSGenZDaughter_charge",        "FSGenElectron_charge[abs(FSGenElectron_parentPDG)!=15]")
                .Define("n_FSGenZDaughter",     "FSGenZDaughter_charge.size()")

                .Define("FSGenMuon_size",   "FSGenMuon_vertex_z[abs(FSGenMuon_parentPDG)!=15]")
                .Define("n_FSGenMuon_sel",     "FSGenMuon_size.size()")
                

                ######################
                ##### FILTERING ######
                ######################
                .Define("OnePairGen",     "(n_FSGenZDaughter==2 and n_FSGenMuon_sel==0)*1.0")

                .Filter("OnePairGen==1 && n_FSRGenTau==2")

                .Filter("(FSGenZDaughter_charge.at(0) + FSGenZDaughter_charge.at(1))==0")

                .Filter("(FSRGenTau_charge.at(0) + FSRGenTau_charge.at(1))==0")

                #################
                # Gen particles #
                #################

                .Define("GenZ_p4",     "(FSGenZDaughter_p4.at(0)+FSGenZDaughter_p4.at(1))")
                .Define("GenZ_px",    "GenZ_p4.Px()")
                .Define("GenZ_py",    "GenZ_p4.Py()")
                .Define("GenZ_pz",    "GenZ_p4.Pz()")
                .Define("GenZ_p",    "GenZ_p4.P()")
                .Define("GenZ_pt",    "GenZ_p4.Pt()")
                .Define("GenZ_e",     "GenZ_p4.E()")
                .Define("GenZ_eta",    "GenZ_p4.Eta()")
                .Define("GenZ_phi",    "GenZ_p4.Phi()")
                .Define("GenZ_theta",    "GenZ_p4.Theta()")
                .Define("GenZ_y",     "GenZ_p4.Rapidity()")
                .Define("GenZ_mass",    "GenZ_p4.M()")

                .Define("FSGenZLead_p4",     "if (FSGenZDaughter_p4.at(0).Pt()>FSGenZDaughter_p4.at(1).Pt()) return FSGenZDaughter_p4.at(0); else return FSGenZDaughter_p4.at(1);")
                .Define("FSGenZLead_px",    "FSGenZLead_p4.Px()")
                .Define("FSGenZLead_py",    "FSGenZLead_p4.Py()")
                .Define("FSGenZLead_pz",    "FSGenZLead_p4.Pz()")
                .Define("FSGenZLead_p",    "FSGenZLead_p4.P()")
                .Define("FSGenZLead_pt",    "FSGenZLead_p4.Pt()")
                .Define("FSGenZLead_e",     "FSGenZLead_p4.E()")
                .Define("FSGenZLead_eta",    "FSGenZLead_p4.Eta()")
                .Define("FSGenZLead_phi",    "FSGenZLead_p4.Phi()")
                .Define("FSGenZLead_theta",    "FSGenZLead_p4.Theta()")
                .Define("FSGenZLead_y",     "FSGenZLead_p4.Rapidity()")
                .Define("FSGenZLead_mass",    "FSGenZLead_p4.M()")
                
                .Define("FSGenZSub_p4",     "if (FSGenZDaughter_p4.at(0).Pt()>FSGenZDaughter_p4.at(1).Pt()) return FSGenZDaughter_p4.at(1); else return FSGenZDaughter_p4.at(0);")
                .Define("FSGenZSub_px",    "FSGenZSub_p4.Px()")
                .Define("FSGenZSub_py",    "FSGenZSub_p4.Py()")
                .Define("FSGenZSub_pz",    "FSGenZSub_p4.Pz()")
                .Define("FSGenZSub_p",    "FSGenZSub_p4.P()")
                .Define("FSGenZSub_pt",    "FSGenZSub_p4.Pt()")
                .Define("FSGenZSub_e",     "FSGenZSub_p4.E()")
                .Define("FSGenZSub_eta",    "FSGenZSub_p4.Eta()")
                .Define("FSGenZSub_phi",    "FSGenZSub_p4.Phi()")
                .Define("FSGenZSub_theta",    "FSGenZSub_p4.Theta()")
                .Define("FSGenZSub_y",     "FSGenZSub_p4.Rapidity()")
                .Define("FSGenZSub_mass",    "FSGenZSub_p4.M()")

                .Define("FSGenZP_p4",     "if (FSGenZDaughter_charge.at(0)==1) return FSGenZDaughter_p4.at(0); else return FSGenZDaughter_p4.at(1);")
                .Define("FSGenZP_px",    "FSGenZP_p4.Px()")
                .Define("FSGenZP_py",    "FSGenZP_p4.Py()")
                .Define("FSGenZP_pz",    "FSGenZP_p4.Pz()")
                .Define("FSGenZP_p",    "FSGenZP_p4.P()")
                .Define("FSGenZP_pt",    "FSGenZP_p4.Pt()")
                .Define("FSGenZP_e",     "FSGenZP_p4.E()")
                .Define("FSGenZP_eta",    "FSGenZP_p4.Eta()")
                .Define("FSGenZP_phi",    "FSGenZP_p4.Phi()")
                .Define("FSGenZP_theta",    "FSGenZP_p4.Theta()")
                .Define("FSGenZP_y",     "FSGenZP_p4.Rapidity()")
                .Define("FSGenZP_mass",    "FSGenZP_p4.M()")
                
                .Define("FSGenZM_p4",     "if (FSGenZDaughter_charge.at(0)==1) return FSGenZDaughter_p4.at(1); else return FSGenZDaughter_p4.at(0);")
                .Define("FSGenZM_px",    "FSGenZM_p4.Px()")
                .Define("FSGenZM_py",    "FSGenZM_p4.Py()")
                .Define("FSGenZM_pz",    "FSGenZM_p4.Pz()")
                .Define("FSGenZM_p",    "FSGenZM_p4.P()")
                .Define("FSGenZM_pt",    "FSGenZM_p4.Pt()")
                .Define("FSGenZM_e",     "FSGenZM_p4.E()")
                .Define("FSGenZM_eta",    "FSGenZM_p4.Eta()")
                .Define("FSGenZM_phi",    "FSGenZM_p4.Phi()")
                .Define("FSGenZM_theta",    "FSGenZM_p4.Theta()")
                .Define("FSGenZM_y",     "FSGenZM_p4.Rapidity()")
                .Define("FSGenZM_mass",    "FSGenZM_p4.M()")

                .Define("FSGenZDaughter_DR",       "FCCAnalyses::ZHfunctions::deltaR(FSGenZLead_phi, FSGenZSub_phi, FSGenZLead_eta, FSGenZSub_eta)")
                .Define("FSGenZDaughter_scalar",      "(FSGenZLead_px*FSGenZSub_px + FSGenZLead_py*FSGenZSub_py + FSGenZLead_pz*FSGenZSub_pz)")
                .Define("FSGenZDaughter_cos",      "GenZ_p/FSGenZDaughter_scalar")
                .Define("FSGenZDaughter_DEta",    "(FSGenZLead_eta - FSGenZSub_eta)")
                .Define("FSGenZDaughter_DPhi",    "(FSGenZLead_phi - FSGenZSub_phi)")
                .Define("FSGenZDaughter_DEta_y",    "if (FSGenZLead_y>FSGenZSub_y) return (FSGenZLead_eta - FSGenZSub_eta); \
                                        else if (FSGenZLead_y<FSGenZSub_y) return (FSGenZSub_eta - FSGenZLead_eta); else return double(-10.);")
                .Define("FSGenZDaughter_DPhi_y",    "if (FSGenZLead_y>FSGenZSub_y) return (FSGenZLead_phi - FSGenZSub_phi); \
                                        else if (FSGenZLead_y<FSGenZSub_y) return (FSGenZSub_phi - FSGenZLead_phi); else return double(-10.);")

                .Define("FSRGenTau_p4",     "FCCAnalyses::ZHfunctions::build_p4(FSRGenTau_px, FSRGenTau_py, FSRGenTau_pz, FSRGenTau_e)")
                .Define("FSRGenTauLead_p4",     "if (FSRGenTau_p4.at(0).Pt()>FSRGenTau_p4.at(1).Pt()) return FSRGenTau_p4.at(0); else return FSRGenTau_p4.at(1);")
                .Define("FSRGenTauLead_px",    "FSRGenTauLead_p4.Px()")
                .Define("FSRGenTauLead_py",    "FSRGenTauLead_p4.Py()")
                .Define("FSRGenTauLead_pz",    "FSRGenTauLead_p4.Pz()")
                .Define("FSRGenTauLead_p",    "FSRGenTauLead_p4.P()")
                .Define("FSRGenTauLead_pt",    "FSRGenTauLead_p4.Pt()")
                .Define("FSRGenTauLead_e",     "FSRGenTauLead_p4.E()")
                .Define("FSRGenTauLead_eta",    "FSRGenTauLead_p4.Eta()")
                .Define("FSRGenTauLead_phi",    "FSRGenTauLead_p4.Phi()")
                .Define("FSRGenTauLead_theta",    "FSRGenTauLead_p4.Theta()")
                .Define("FSRGenTauLead_y",     "FSRGenTauLead_p4.Rapidity()")
                .Define("FSRGenTauLead_mass",    "FSRGenTauLead_p4.M()")
                
                .Define("FSRGenTauSub_p4",     "if (FSRGenTau_p4.at(0).Pt()>FSRGenTau_p4.at(1).Pt()) return FSRGenTau_p4.at(1); else return FSRGenTau_p4.at(0);")
                .Define("FSRGenTauSub_px",    "FSRGenTauSub_p4.Px()")
                .Define("FSRGenTauSub_py",    "FSRGenTauSub_p4.Py()")
                .Define("FSRGenTauSub_pz",    "FSRGenTauSub_p4.Pz()")
                .Define("FSRGenTauSub_p",    "FSRGenTauSub_p4.P()")
                .Define("FSRGenTauSub_pt",    "FSRGenTauSub_p4.Pt()")
                .Define("FSRGenTauSub_e",     "FSRGenTauSub_p4.E()")
                .Define("FSRGenTauSub_eta",    "FSRGenTauSub_p4.Eta()")
                .Define("FSRGenTauSub_phi",    "FSRGenTauSub_p4.Phi()")
                .Define("FSRGenTauSub_theta",    "FSRGenTauSub_p4.Theta()")
                .Define("FSRGenTauSub_y",     "FSRGenTauSub_p4.Rapidity()")
                .Define("FSRGenTauSub_mass",    "FSRGenTauSub_p4.M()")

                .Define("FSRGenTauP_p4",     "if (FSRGenTau_charge.at(0)==1) return FSRGenTau_p4.at(0); else return FSRGenTau_p4.at(1);")
                .Define("FSRGenTauP_px",    "FSRGenTauP_p4.Px()")
                .Define("FSRGenTauP_py",    "FSRGenTauP_p4.Py()")
                .Define("FSRGenTauP_pz",    "FSRGenTauP_p4.Pz()")
                .Define("FSRGenTauP_p",    "FSRGenTauP_p4.P()")
                .Define("FSRGenTauP_pt",    "FSRGenTauP_p4.Pt()")
                .Define("FSRGenTauP_e",     "FSRGenTauP_p4.E()")
                .Define("FSRGenTauP_eta",    "FSRGenTauP_p4.Eta()")
                .Define("FSRGenTauP_phi",    "FSRGenTauP_p4.Phi()")
                .Define("FSRGenTauP_theta",    "FSRGenTauP_p4.Theta()")
                .Define("FSRGenTauP_y",     "FSRGenTauP_p4.Rapidity()")
                .Define("FSRGenTauP_mass",    "FSRGenTauP_p4.M()")
                
                .Define("FSRGenTauM_p4",     "if (FSRGenTau_charge.at(0)==1) return FSRGenTau_p4.at(1); else return FSRGenTau_p4.at(0);")
                .Define("FSRGenTauM_px",    "FSRGenTauM_p4.Px()")
                .Define("FSRGenTauM_py",    "FSRGenTauM_p4.Py()")
                .Define("FSRGenTauM_pz",    "FSRGenTauM_p4.Pz()")
                .Define("FSRGenTauM_p",    "FSRGenTauM_p4.P()")
                .Define("FSRGenTauM_pt",    "FSRGenTauM_p4.Pt()")
                .Define("FSRGenTauM_e",     "FSRGenTauM_p4.E()")
                .Define("FSRGenTauM_eta",    "FSRGenTauM_p4.Eta()")
                .Define("FSRGenTauM_phi",    "FSRGenTauM_p4.Phi()")
                .Define("FSRGenTauM_theta",    "FSRGenTauM_p4.Theta()")
                .Define("FSRGenTauM_y",     "FSRGenTauM_p4.Rapidity()")
                .Define("FSRGenTauM_mass",    "FSRGenTauM_p4.M()")

                .Define("GenTau_e", "if (n_FSRGenTau>1) return (FSRGenTau_e.at(0) + FSRGenTau_e.at(1)); else return float(-1000.);")
                .Define("GenTau_px", "if (n_FSRGenTau>1) return (FSRGenTau_px.at(0) + FSRGenTau_px.at(1)); else return float(-1000.);")
                .Define("GenTau_py", "if (n_FSRGenTau>1) return (FSRGenTau_py.at(0) + FSRGenTau_py.at(1)); else return float(-1000.);")
                .Define("GenTau_pz", "if (n_FSRGenTau>1) return (FSRGenTau_pz.at(0) + FSRGenTau_pz.at(1)); else return float(-1000.);")
                .Define("FSRGenTau_invMass", "if (n_FSRGenTau>1) return sqrt(GenTau_e*GenTau_e - GenTau_px*GenTau_px - GenTau_py*GenTau_py - GenTau_pz*GenTau_pz ); else return float(-1000.);")
                
                .Define("GenTau_p", "if (n_FSRGenTau>1) return sqrt(GenTau_px*GenTau_px + GenTau_py*GenTau_py + GenTau_pz*GenTau_pz); else return float(-1.);")
                .Define("GenTau_scalar", "if (n_FSRGenTau>1) return (FSRGenTau_px.at(0)*FSRGenTau_px.at(1) + FSRGenTau_py.at(0)*FSRGenTau_py.at(1) + FSRGenTau_pz.at(0)*FSRGenTau_pz.at(1)); else return float(-1000.);")
                .Define("FSRGenTau_cos", "if (n_FSRGenTau>1) return (GenTau_scalar/(FSRGenTau_p.at(0)*FSRGenTau_p.at(1))); else return float(-2.);")
                
                .Define("FSRGenTau_DEta","FSRGenTauLead_eta - FSRGenTauSub_eta")
                .Define("FSRGenTau_DPhi","FSRGenTauLead_phi - FSRGenTauSub_phi")
                .Define("FSRGenTau_DEta_y",    "if (FSRGenTauLead_y>FSRGenTauSub_y) return (FSRGenTauLead_eta - FSRGenTauSub_eta); \
                                        else if (FSRGenTauLead_y<FSRGenTauSub_y) return (FSRGenTauSub_eta - FSRGenTauLead_eta); else return double(-10.);")
                .Define("FSRGenTau_DPhi_y",    "if (FSRGenTauLead_y>FSRGenTauSub_y) return (FSRGenTauLead_phi - FSRGenTauSub_phi); \
                                        else if (FSRGenTauLead_y<FSRGenTauSub_y) return (FSRGenTauSub_phi - FSRGenTauLead_phi); else return double(-10.);")
                .Define("FSRGenTau_DR","myUtils::deltaR(FSRGenTau_phi.at(0), FSRGenTau_phi.at(1), FSRGenTau_eta.at(0), FSRGenTau_eta.at(1))")

                .Define("GenHiggs_p4",      "FCCAnalyses::ZHfunctions::build_p4(GenHiggs_px, GenHiggs_py, GenHiggs_pz, GenHiggs_e)")
                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("HRF_GenTau_p4",    "myUtils::boosted_p4(- GenHiggs_p4.at(0), FSRGenTau_p4)")
                .Define("HRF_GenTauLead_p4",     "if (HRF_GenTau_p4.at(0).Pt()>HRF_GenTau_p4.at(1).Pt()) return HRF_GenTau_p4.at(0); else return HRF_GenTau_p4.at(1);")
                .Define("HRF_GenTauLead_px",    "HRF_GenTauLead_p4.Px()")
                .Define("HRF_GenTauLead_py",    "HRF_GenTauLead_p4.Py()")
                .Define("HRF_GenTauLead_pz",    "HRF_GenTauLead_p4.Pz()")
                .Define("HRF_GenTauLead_p",    "HRF_GenTauLead_p4.P()")
                .Define("HRF_GenTauLead_pt",    "HRF_GenTauLead_p4.Pt()")
                .Define("HRF_GenTauLead_e",     "HRF_GenTauLead_p4.E()")
                .Define("HRF_GenTauLead_eta",    "HRF_GenTauLead_p4.Eta()")
                .Define("HRF_GenTauLead_phi",    "HRF_GenTauLead_p4.Phi()")
                .Define("HRF_GenTauLead_theta",    "HRF_GenTauLead_p4.Theta()")
                .Define("HRF_GenTauLead_y",     "HRF_GenTauLead_p4.Rapidity()")
                .Define("HRF_GenTauLead_mass",    "HRF_GenTauLead_p4.M()")
                
                .Define("HRF_GenTauSub_p4",     "if (HRF_GenTau_p4.at(0).Pt()>HRF_GenTau_p4.at(1).Pt()) return HRF_GenTau_p4.at(1); else return HRF_GenTau_p4.at(0);")
                .Define("HRF_GenTauSub_px",    "HRF_GenTauSub_p4.Px()")
                .Define("HRF_GenTauSub_py",    "HRF_GenTauSub_p4.Py()")
                .Define("HRF_GenTauSub_pz",    "HRF_GenTauSub_p4.Pz()")
                .Define("HRF_GenTauSub_p",    "HRF_GenTauSub_p4.P()")
                .Define("HRF_GenTauSub_pt",    "HRF_GenTauSub_p4.Pt()")
                .Define("HRF_GenTauSub_e",     "HRF_GenTauSub_p4.E()")
                .Define("HRF_GenTauSub_eta",    "HRF_GenTauSub_p4.Eta()")
                .Define("HRF_GenTauSub_phi",    "HRF_GenTauSub_p4.Phi()")
                .Define("HRF_GenTauSub_theta",    "HRF_GenTauSub_p4.Theta()")
                .Define("HRF_GenTauSub_y",     "HRF_GenTauSub_p4.Rapidity()")
                .Define("HRF_GenTauSub_mass",    "HRF_GenTauSub_p4.M()")

                .Define("HRF_GenTauP_p4",     "if (FSRGenTau_charge.at(0)==1) return HRF_GenTau_p4.at(0); else return HRF_GenTau_p4.at(1);")
                .Define("HRF_GenTauP_px",    "HRF_GenTauP_p4.Px()")
                .Define("HRF_GenTauP_py",    "HRF_GenTauP_p4.Py()")
                .Define("HRF_GenTauP_pz",    "HRF_GenTauP_p4.Pz()")
                .Define("HRF_GenTauP_p",    "HRF_GenTauP_p4.P()")
                .Define("HRF_GenTauP_pt",    "HRF_GenTauP_p4.Pt()")
                .Define("HRF_GenTauP_e",     "HRF_GenTauP_p4.E()")
                .Define("HRF_GenTauP_eta",    "HRF_GenTauP_p4.Eta()")
                .Define("HRF_GenTauP_phi",    "HRF_GenTauP_p4.Phi()")
                .Define("HRF_GenTauP_theta",    "HRF_GenTauP_p4.Theta()")
                .Define("HRF_GenTauP_y",     "HRF_GenTauP_p4.Rapidity()")
                .Define("HRF_GenTauP_mass",    "HRF_GenTauP_p4.M()")
                
                .Define("HRF_GenTauM_p4",     "if (FSRGenTau_charge.at(0)==1) return HRF_GenTau_p4.at(1); else return HRF_GenTau_p4.at(0);")
                .Define("HRF_GenTauM_px",    "HRF_GenTauM_p4.Px()")
                .Define("HRF_GenTauM_py",    "HRF_GenTauM_p4.Py()")
                .Define("HRF_GenTauM_pz",    "HRF_GenTauM_p4.Pz()")
                .Define("HRF_GenTauM_p",    "HRF_GenTauM_p4.P()")
                .Define("HRF_GenTauM_pt",    "HRF_GenTauM_p4.Pt()")
                .Define("HRF_GenTauM_e",     "HRF_GenTauM_p4.E()")
                .Define("HRF_GenTauM_eta",    "HRF_GenTauM_p4.Eta()")
                .Define("HRF_GenTauM_phi",    "HRF_GenTauM_p4.Phi()")
                .Define("HRF_GenTauM_theta",    "HRF_GenTauM_p4.Theta()")
                .Define("HRF_GenTauM_y",     "HRF_GenTauM_p4.Rapidity()")
                .Define("HRF_GenTauM_mass",    "HRF_GenTauM_p4.M()")

                .Define("HRF_GenTau_DEta_y",    "if (HRF_GenTauLead_y>HRF_GenTauSub_y) return (HRF_GenTauLead_eta - HRF_GenTauSub_eta); \
                                        else if (HRF_GenTauLead_y<HRF_GenTauSub_y) return (HRF_GenTauSub_eta - HRF_GenTauLead_eta); else return double(-10.);")
                .Define("HRF_GenTau_DPhi_y",    "if (HRF_GenTauLead_y>HRF_GenTauSub_y) return (HRF_GenTauLead_phi - HRF_GenTauSub_phi); \
                                        else if (HRF_GenTauLead_y<HRF_GenTauSub_y) return (HRF_GenTauSub_phi - HRF_GenTauLead_phi); else return double(-10.);")
                .Define("HRF_GenTau_DEta","HRF_GenTauLead_eta - HRF_GenTauSub_eta")
                .Define("HRF_GenTau_DPhi","HRF_GenTauLead_phi - HRF_GenTauSub_phi")

                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 

                .Define("ZRF_GenZDaughter_p4",    "return myUtils::boosted_p4(- GenZ_p4, FSGenZDaughter_p4);")
                .Define("ZRF_GenZLead_p4",     "if (ZRF_GenZDaughter_p4.at(0).Pt()>ZRF_GenZDaughter_p4.at(1).Pt()) return ZRF_GenZDaughter_p4.at(0); else return ZRF_GenZDaughter_p4.at(1);")
                .Define("ZRF_GenZLead_px",    "ZRF_GenZLead_p4.Px()")
                .Define("ZRF_GenZLead_py",    "ZRF_GenZLead_p4.Py()")
                .Define("ZRF_GenZLead_pz",    "ZRF_GenZLead_p4.Pz()")
                .Define("ZRF_GenZLead_p",    "ZRF_GenZLead_p4.P()")
                .Define("ZRF_GenZLead_pt",    "ZRF_GenZLead_p4.Pt()")
                .Define("ZRF_GenZLead_e",     "ZRF_GenZLead_p4.E()")
                .Define("ZRF_GenZLead_eta",    "ZRF_GenZLead_p4.Eta()")
                .Define("ZRF_GenZLead_phi",    "ZRF_GenZLead_p4.Phi()")
                .Define("ZRF_GenZLead_theta",    "ZRF_GenZLead_p4.Theta()")
                .Define("ZRF_GenZLead_y",     "ZRF_GenZLead_p4.Rapidity()")
                .Define("ZRF_GenZLead_mass",    "ZRF_GenZLead_p4.M()")
                
                .Define("ZRF_GenZSub_p4",     "if (ZRF_GenZDaughter_p4.at(0).Pt()>ZRF_GenZDaughter_p4.at(1).Pt()) return ZRF_GenZDaughter_p4.at(1); else return ZRF_GenZDaughter_p4.at(0);")
                .Define("ZRF_GenZSub_px",    "ZRF_GenZSub_p4.Px()")
                .Define("ZRF_GenZSub_py",    "ZRF_GenZSub_p4.Py()")
                .Define("ZRF_GenZSub_pz",    "ZRF_GenZSub_p4.Pz()")
                .Define("ZRF_GenZSub_p",    "ZRF_GenZSub_p4.P()")
                .Define("ZRF_GenZSub_pt",    "ZRF_GenZSub_p4.Pt()")
                .Define("ZRF_GenZSub_e",     "ZRF_GenZSub_p4.E()")
                .Define("ZRF_GenZSub_eta",    "ZRF_GenZSub_p4.Eta()")
                .Define("ZRF_GenZSub_phi",    "ZRF_GenZSub_p4.Phi()")
                .Define("ZRF_GenZSub_theta",    "ZRF_GenZSub_p4.Theta()")
                .Define("ZRF_GenZSub_y",     "ZRF_GenZSub_p4.Rapidity()")
                .Define("ZRF_GenZSub_mass",    "ZRF_GenZSub_p4.M()")

                .Define("ZRF_GenZP_p4",     "if (FSGenZDaughter_charge.at(0)==1) return ZRF_GenZDaughter_p4.at(0); else return ZRF_GenZDaughter_p4.at(1);")
                .Define("ZRF_GenZP_px",    "ZRF_GenZP_p4.Px()")
                .Define("ZRF_GenZP_py",    "ZRF_GenZP_p4.Py()")
                .Define("ZRF_GenZP_pz",    "ZRF_GenZP_p4.Pz()")
                .Define("ZRF_GenZP_p",    "ZRF_GenZP_p4.P()")
                .Define("ZRF_GenZP_pt",    "ZRF_GenZP_p4.Pt()")
                .Define("ZRF_GenZP_e",     "ZRF_GenZP_p4.E()")
                .Define("ZRF_GenZP_eta",    "ZRF_GenZP_p4.Eta()")
                .Define("ZRF_GenZP_phi",    "ZRF_GenZP_p4.Phi()")
                .Define("ZRF_GenZP_theta",    "ZRF_GenZP_p4.Theta()")
                .Define("ZRF_GenZP_y",     "ZRF_GenZP_p4.Rapidity()")
                .Define("ZRF_GenZP_mass",    "ZRF_GenZP_p4.M()")
                
                .Define("ZRF_GenZM_p4",     "if (FSGenZDaughter_charge.at(0)==1) return ZRF_GenZDaughter_p4.at(1); else return ZRF_GenZDaughter_p4.at(0);")
                .Define("ZRF_GenZM_px",    "ZRF_GenZM_p4.Px()")
                .Define("ZRF_GenZM_py",    "ZRF_GenZM_p4.Py()")
                .Define("ZRF_GenZM_pz",    "ZRF_GenZM_p4.Pz()")
                .Define("ZRF_GenZM_p",    "ZRF_GenZM_p4.P()")
                .Define("ZRF_GenZM_pt",    "ZRF_GenZM_p4.Pt()")
                .Define("ZRF_GenZM_e",     "ZRF_GenZM_p4.E()")
                .Define("ZRF_GenZM_eta",    "ZRF_GenZM_p4.Eta()")
                .Define("ZRF_GenZM_phi",    "ZRF_GenZM_p4.Phi()")
                .Define("ZRF_GenZM_theta",    "ZRF_GenZM_p4.Theta()")
                .Define("ZRF_GenZM_y",     "ZRF_GenZM_p4.Rapidity()")
                .Define("ZRF_GenZM_mass",    "ZRF_GenZM_p4.M()")

                .Define("ZRF_GenZDaughter_DR",       "FCCAnalyses::ZHfunctions::deltaR(ZRF_GenZLead_phi, ZRF_GenZSub_phi, ZRF_GenZLead_eta, ZRF_GenZSub_eta)")
                .Define("ZRF_GenZDaughter_scalar",      "(ZRF_GenZLead_px*ZRF_GenZSub_px + ZRF_GenZLead_py*ZRF_GenZSub_py + ZRF_GenZLead_pz*ZRF_GenZSub_pz)")
                .Define("ZRF_GenZDaughter_cos",      "GenZ_p/ZRF_GenZDaughter_scalar")
                .Define("ZRF_GenZDaughter_DEta",    "(ZRF_GenZLead_eta - ZRF_GenZSub_eta)")
                .Define("ZRF_GenZDaughter_DPhi",    "(ZRF_GenZLead_phi - ZRF_GenZSub_phi)")
                .Define("ZRF_GenZDaughter_DEta_y",    "if (ZRF_GenZLead_y>ZRF_GenZSub_y) return (ZRF_GenZLead_eta - ZRF_GenZSub_eta); \
                                        else if (ZRF_GenZLead_y<ZRF_GenZSub_y) return (ZRF_GenZSub_eta - ZRF_GenZLead_eta); else return double(-10.);")
                .Define("ZRF_GenZDaughter_DPhi_y",    "if (ZRF_GenZLead_y>ZRF_GenZSub_y) return (ZRF_GenZLead_phi - ZRF_GenZSub_phi); \
                                        else if (ZRF_GenZLead_y<ZRF_GenZSub_y) return (ZRF_GenZSub_phi - ZRF_GenZLead_phi); else return double(-10.);")

                ### angles visualisation in figure 1 (2) at pag 8 of https://arxiv.org/pdf/2205.07715, changed some of the names around
                #may be interesting to simnply keep the cosine of thetas (John Hopkins)
                #angle between H vector in lab frame and tau in H rest frame
                .Define("GenTheta2",      "acos(FCCAnalyses::ZHfunctions::get_scalar(GenHiggs_p4.at(0), HRF_GenTauM_p4)/(GenHiggs_p.at(0)*HRF_GenTauM_p))")
                #angle between Z vector in lab frame and Muon in Z rest frame
                .Define("GenTheta1",      "acos(FCCAnalyses::ZHfunctions::get_scalar(GenZ_p4, ZRF_GenZM_p4)/(GenZ_p*ZRF_GenZM_p))")
                #angle between decay planes of H and Z
                .Define("GenPhi",      "acos(FCCAnalyses::ZHfunctions::get_scalar(HRF_GenTauM_p4, ZRF_GenZM_p4)/(HRF_GenTauM_p*ZRF_GenZM_p))")
                #angle between beam line and Z decay plane
                .Define("Beam_vec",     "FCCAnalyses::ZHfunctions::build_p4_single(0, 0, 1, 0)") #unitary vector of beam axis along z
                .Define("Beam_p",       "float(1.)") #magnitude

                .Define("GenPhi1",      "acos(FCCAnalyses::ZHfunctions::get_scalar(Beam_vec, ZRF_GenZM_p4)/(Beam_p*ZRF_GenZM_p))")
                .Define("GenThetastar",      "acos(FCCAnalyses::ZHfunctions::get_scalar(Beam_vec, GenZ_p4)/(Beam_p*GenZ_p))")

                .Define("GenThetastar_cos",        "(cos(GenThetastar))")
                .Define("GenTheta1_cos",        "(cos(GenTheta1))")
                .Define("GenTheta2_cos",        "(cos(GenTheta2))")
                .Define("GenPhi_cos",        "(cos(GenPhi))")
                .Define("GenPhi1_cos",        "(cos(GenPhi1))")

                .Define("Total_p4",     "FCCAnalyses::ZHfunctions::build_p4_single(0.,0.,0.,240.)")
                .Define("GenRecoil",       "(Total_p4-GenZ_p4).M()")
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
            "FSGenElectron_vertex_x",
            "FSGenElectron_vertex_y",
            "FSGenElectron_vertex_z",

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
            "FSRGenTau_vertex_x",
            "FSRGenTau_vertex_y",
            "FSRGenTau_vertex_z",

            #"n_TauNeg_MuNuNu",       
            #"n_TauNeg_MuNuNu_Phot",  
            #"n_TauNeg_ENuNu",        
            #"n_TauNeg_ENuNu_Phot",   
            #"n_TauNeg_PiNu",         
            #"n_TauNeg_PiNu_Phot",    
            #"n_TauNeg_KNu",          
            #"n_TauNeg_KNu_Phot",     
            #"n_TauNeg_PiK0Nu",       
            #"n_TauNeg_PiK0Nu_Phot",  
            #"n_TauNeg_KK0Nu",        
            #"n_TauNeg_KK0Nu_Phot",   
            #"n_TauNeg_3PiNu",        
            #"n_TauNeg_3PiNu_Phot",   
            #"n_TauNeg_PiKKNu",       
            #"n_TauNeg_PiKKNu_Phot",  

            #"n_TauPos_MuNuNu",       
            #"n_TauPos_MuNuNu_Phot",  
            #"n_TauPos_ENuNu",        
            #"n_TauPos_ENuNu_Phot",   
            #"n_TauPos_PiNu",         
            #"n_TauPos_PiNu_Phot",    
            #"n_TauPos_KNu",          
            #"n_TauPos_KNu_Phot",     
            #"n_TauPos_PiK0Nu",       
            #"n_TauPos_PiK0Nu_Phot",  
            #"n_TauPos_KK0Nu",        
            #"n_TauPos_KK0Nu_Phot",   
            #"n_TauPos_3PiNu",        
            #"n_TauPos_3PiNu_Phot",   
            #"n_TauPos_PiKKNu",       
            #"n_TauPos_PiKKNu_Phot", 

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
            "GenHiggs_mass",
            "GenHiggs_eta", 
            "GenHiggs_theta", 
            "GenHiggs_phi", 
            "GenHiggs_charge", 
        ]
        #complex variables added here at stage2
        branchList += [
            ######## Monte-Carlo particles #######
            
            "GenZ_px",
            "GenZ_py",
            "GenZ_pz",
            "GenZ_p",
            "GenZ_pt",
            "GenZ_e",
            "GenZ_eta",
            "GenZ_phi",
            "GenZ_theta",
            "GenZ_y",
            "GenZ_mass",

            "FSGenZLead_px", 
            "FSGenZLead_py",   
            "FSGenZLead_pz",   
            "FSGenZLead_p",    
            "FSGenZLead_pt",   
            "FSGenZLead_e",    
            "FSGenZLead_eta",    
            "FSGenZLead_phi",    
            "FSGenZLead_theta",   
            "FSGenZLead_y",     
            "FSGenZLead_mass",   

            "FSGenZSub_px",    
            "FSGenZSub_py",   
            "FSGenZSub_pz",   
            "FSGenZSub_p",   
            "FSGenZSub_pt",  
            "FSGenZSub_e",     
            "FSGenZSub_eta",   
            "FSGenZSub_phi",   
            "FSGenZSub_theta",    
            "FSGenZSub_y",    
            "FSGenZSub_mass",   

            "FSGenZP_px", 
            "FSGenZP_py",   
            "FSGenZP_pz",   
            "FSGenZP_p",    
            "FSGenZP_pt",   
            "FSGenZP_e",    
            "FSGenZP_eta",    
            "FSGenZP_phi",    
            "FSGenZP_theta",   
            "FSGenZP_y",     
            "FSGenZP_mass",   

            "FSGenZM_px",    
            "FSGenZM_py",   
            "FSGenZM_pz",   
            "FSGenZM_p",   
            "FSGenZM_pt",  
            "FSGenZM_e",     
            "FSGenZM_eta",   
            "FSGenZM_phi",   
            "FSGenZM_theta",    
            "FSGenZM_y",    
            "FSGenZM_mass", 

            "FSRGenTauLead_px",    
            "FSRGenTauLead_py",   
            "FSRGenTauLead_pz",   
            "FSRGenTauLead_p",   
            "FSRGenTauLead_pt",   
            "FSRGenTauLead_e",    
            "FSRGenTauLead_eta",    
            "FSRGenTauLead_phi",    
            "FSRGenTauLead_theta",    
            "FSRGenTauLead_y",    
            "FSRGenTauLead_mass",

            "FSRGenTauSub_px",    
            "FSRGenTauSub_py",   
            "FSRGenTauSub_pz",   
            "FSRGenTauSub_p",   
            "FSRGenTauSub_pt",   
            "FSRGenTauSub_e",    
            "FSRGenTauSub_eta",    
            "FSRGenTauSub_phi",    
            "FSRGenTauSub_theta",    
            "FSRGenTauSub_y",    
            "FSRGenTauSub_mass",

            "FSRGenTauP_px",    
            "FSRGenTauP_py",   
            "FSRGenTauP_pz",   
            "FSRGenTauP_p",   
            "FSRGenTauP_pt",   
            "FSRGenTauP_e",    
            "FSRGenTauP_eta",    
            "FSRGenTauP_phi",    
            "FSRGenTauP_theta",    
            "FSRGenTauP_y",    
            "FSRGenTauP_mass",

            "FSRGenTauM_px",    
            "FSRGenTauM_py",   
            "FSRGenTauM_pz",   
            "FSRGenTauM_p",   
            "FSRGenTauM_pt",   
            "FSRGenTauM_e",    
            "FSRGenTauM_eta",    
            "FSRGenTauM_phi",    
            "FSRGenTauM_theta",    
            "FSRGenTauM_y",    
            "FSRGenTauM_mass",
        
            "FSRGenTau_DR",
            "FSRGenTau_cos",
            "FSRGenTau_DEta", 
            "FSRGenTau_DPhi",
            
            "FSGenZDaughter_DR", 
            "FSGenZDaughter_cos", 
            "FSGenZDaughter_DEta", 
            "FSGenZDaughter_DPhi", 

            "FSRGenTau_DEta_y", 
            "FSRGenTau_DPhi_y", 
            
            "FSGenZDaughter_DEta_y", 
            "FSGenZDaughter_DPhi_y", 

            "HRF_GenTauLead_px",  
            "HRF_GenTauLead_py",  
            "HRF_GenTauLead_pz", 
            "HRF_GenTauLead_p", 
            "HRF_GenTauLead_pt",  
            "HRF_GenTauLead_e",   
            "HRF_GenTauLead_eta", 
            "HRF_GenTauLead_phi",  
            "HRF_GenTauLead_theta",    
            "HRF_GenTauLead_y", 

            "HRF_GenTauSub_px",  
            "HRF_GenTauSub_py",  
            "HRF_GenTauSub_pz", 
            "HRF_GenTauSub_p", 
            "HRF_GenTauSub_pt",  
            "HRF_GenTauSub_e",   
            "HRF_GenTauSub_eta", 
            "HRF_GenTauSub_phi",  
            "HRF_GenTauSub_theta",    
            "HRF_GenTauSub_y", 

            "HRF_GenTauP_px",  
            "HRF_GenTauP_py",  
            "HRF_GenTauP_pz", 
            "HRF_GenTauP_p", 
            "HRF_GenTauP_pt",  
            "HRF_GenTauP_e",   
            "HRF_GenTauP_eta", 
            "HRF_GenTauP_phi",  
            "HRF_GenTauP_theta",    
            "HRF_GenTauP_y", 

            "HRF_GenTauM_px",  
            "HRF_GenTauM_py",  
            "HRF_GenTauM_pz", 
            "HRF_GenTauM_p", 
            "HRF_GenTauM_pt",  
            "HRF_GenTauM_e",   
            "HRF_GenTauM_eta", 
            "HRF_GenTauM_phi",  
            "HRF_GenTauM_theta",    
            "HRF_GenTauM_y", 

            "HRF_GenTau_DEta", 
            "HRF_GenTau_DPhi",
            "HRF_GenTau_DEta_y", 
            "HRF_GenTau_DPhi_y", 

            "ZRF_GenZLead_px",  
            "ZRF_GenZLead_py",  
            "ZRF_GenZLead_pz", 
            "ZRF_GenZLead_p", 
            "ZRF_GenZLead_pt",  
            "ZRF_GenZLead_e",   
            "ZRF_GenZLead_eta", 
            "ZRF_GenZLead_phi",  
            "ZRF_GenZLead_theta",    
            "ZRF_GenZLead_y", 

            "ZRF_GenZSub_px",  
            "ZRF_GenZSub_py",  
            "ZRF_GenZSub_pz", 
            "ZRF_GenZSub_p", 
            "ZRF_GenZSub_pt",  
            "ZRF_GenZSub_e",   
            "ZRF_GenZSub_eta", 
            "ZRF_GenZSub_phi",  
            "ZRF_GenZSub_theta",    
            "ZRF_GenZSub_y", 

            "ZRF_GenZP_px",  
            "ZRF_GenZP_py",  
            "ZRF_GenZP_pz", 
            "ZRF_GenZP_p", 
            "ZRF_GenZP_pt",  
            "ZRF_GenZP_e",   
            "ZRF_GenZP_eta", 
            "ZRF_GenZP_phi",  
            "ZRF_GenZP_theta",    
            "ZRF_GenZP_y", 

            "ZRF_GenZM_px",  
            "ZRF_GenZM_py",  
            "ZRF_GenZM_pz", 
            "ZRF_GenZM_p", 
            "ZRF_GenZM_pt",  
            "ZRF_GenZM_e",   
            "ZRF_GenZM_eta", 
            "ZRF_GenZM_phi",  
            "ZRF_GenZM_theta",    
            "ZRF_GenZM_y", 

            "ZRF_GenZDaughter_DEta", 
            "ZRF_GenZDaughter_DPhi",
            "ZRF_GenZDaughter_DEta_y", 
            "ZRF_GenZDaughter_DPhi_y", 

            "GenThetastar",
            "GenTheta2",
            "GenPhi1", 
            "GenPhi", 
            "GenTheta1", 

            "GenThetastar_cos",
            "GenTheta2_cos",
            "GenPhi1_cos", 
            "GenPhi_cos", 
            "GenTheta1_cos",

            "GenRecoil",

        ]

        return branchList