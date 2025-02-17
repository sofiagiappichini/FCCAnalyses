import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    #'noISR_e+e-_noCuts_EWonly':{},
    #'noISR_e+e-_noCuts_cehim_m1':{},
    #'noISR_e+e-_noCuts_cehim_p1':{},
    #'noISR_e+e-_noCuts_cehre_m1':{},
    #'noISR_e+e-_noCuts_cehre_p1':{},
    
    #'EWonly_taudecay_2Pi2Nu':{},
    'cehim_m1_taudecay_2Pi2Nu':{},
    'cehim_p1_taudecay_2Pi2Nu':{},
    'cehre_m1_taudecay_2Pi2Nu':{},
    'cehre_p1_taudecay_2Pi2Nu':{},

    #'cehim_m5_taudecay_2Pi2Nu':{},
    #'cehim_p5_taudecay_2Pi2Nu':{},
    #'cehre_m5_taudecay_2Pi2Nu':{},
    #'cehre_p5_taudecay_2Pi2Nu':{},

    #'cehim_m2_taudecay_2Pi2Nu':{},
    #'cehim_p2_taudecay_2Pi2Nu':{},
    #'cehre_m2_taudecay_2Pi2Nu':{},
    #'cehre_p2_taudecay_2Pi2Nu':{},

    #'wzp6_ee_eeH_Htautau_ecm240': {},
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

inputDir = "/ceph/sgiappic/HiggsCP/CPGen/stage1_pinu"

outputDir = "/ceph/sgiappic/HiggsCP/CPGen/stage2_pinu"

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

                .Filter("OnePairGen==1")

                .Filter("(FSGenZDaughter_charge.at(0) + FSGenZDaughter_charge.at(1))==0")

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
                .Define("FSGenZDaughter_cos",      "FSGenZDaughter_scalar/(FSGenZLead_p*FSGenZSub_p)")
                .Define("FSGenZDaughter_DEta",    "(FSGenZLead_eta - FSGenZSub_eta)")
                .Define("FSGenZDaughter_DPhi",    "FCCAnalyses::ZHfunctions::deltaPhi(FSGenZLead_phi, FSGenZSub_phi)")
                .Define("FSGenZDaughter_DEta_y",    "if (FSGenZLead_y>FSGenZSub_y) return (FSGenZLead_eta - FSGenZSub_eta); \
                                        else if (FSGenZLead_y<FSGenZSub_y) return (FSGenZSub_eta - FSGenZLead_eta); else return double(-10.);")
                .Define("FSGenZDaughter_DPhi_y",    "if (FSGenZLead_y>FSGenZSub_y) return (FSGenZLead_phi - FSGenZSub_phi); \
                                        else if (FSGenZLead_y<FSGenZSub_y) return (FSGenZSub_phi - FSGenZLead_phi); else return double(-10.);")

                .Define("HiggsGenTau_p4",     "FCCAnalyses::ZHfunctions::build_p4(HiggsGenTau_px, HiggsGenTau_py, HiggsGenTau_pz, HiggsGenTau_e)")
                .Define("GenTauLead_p4",     "if (HiggsGenTau_p4.at(0).Pt()>HiggsGenTau_p4.at(1).Pt()) return HiggsGenTau_p4.at(0); else return HiggsGenTau_p4.at(1);")
                .Define("GenTauLead_px",    "GenTauLead_p4.Px()")
                .Define("GenTauLead_py",    "GenTauLead_p4.Py()")
                .Define("GenTauLead_pz",    "GenTauLead_p4.Pz()")
                .Define("GenTauLead_p",    "GenTauLead_p4.P()")
                .Define("GenTauLead_pt",    "GenTauLead_p4.Pt()")
                .Define("GenTauLead_e",     "GenTauLead_p4.E()")
                .Define("GenTauLead_eta",    "GenTauLead_p4.Eta()")
                .Define("GenTauLead_phi",    "GenTauLead_p4.Phi()")
                .Define("GenTauLead_theta",    "GenTauLead_p4.Theta()")
                .Define("GenTauLead_y",     "GenTauLead_p4.Rapidity()")
                .Define("GenTauLead_mass",    "GenTauLead_p4.M()")
                
                .Define("GenTauSub_p4",     "if (HiggsGenTau_p4.at(0).Pt()>HiggsGenTau_p4.at(1).Pt()) return HiggsGenTau_p4.at(1); else return HiggsGenTau_p4.at(0);")
                .Define("GenTauSub_px",    "GenTauSub_p4.Px()")
                .Define("GenTauSub_py",    "GenTauSub_p4.Py()")
                .Define("GenTauSub_pz",    "GenTauSub_p4.Pz()")
                .Define("GenTauSub_p",    "GenTauSub_p4.P()")
                .Define("GenTauSub_pt",    "GenTauSub_p4.Pt()")
                .Define("GenTauSub_e",     "GenTauSub_p4.E()")
                .Define("GenTauSub_eta",    "GenTauSub_p4.Eta()")
                .Define("GenTauSub_phi",    "GenTauSub_p4.Phi()")
                .Define("GenTauSub_theta",    "GenTauSub_p4.Theta()")
                .Define("GenTauSub_y",     "GenTauSub_p4.Rapidity()")
                .Define("GenTauSub_mass",    "GenTauSub_p4.M()")

                .Define("GenTauP_p4",     "if (HiggsGenTau_charge.at(0)==1) return HiggsGenTau_p4.at(0); else return HiggsGenTau_p4.at(1);")
                .Define("GenTauP_px",    "GenTauP_p4.Px()")
                .Define("GenTauP_py",    "GenTauP_p4.Py()")
                .Define("GenTauP_pz",    "GenTauP_p4.Pz()")
                .Define("GenTauP_p",    "GenTauP_p4.P()")
                .Define("GenTauP_pt",    "GenTauP_p4.Pt()")
                .Define("GenTauP_e",     "GenTauP_p4.E()")
                .Define("GenTauP_eta",    "GenTauP_p4.Eta()")
                .Define("GenTauP_phi",    "GenTauP_p4.Phi()")
                .Define("GenTauP_theta",    "GenTauP_p4.Theta()")
                .Define("GenTauP_y",     "GenTauP_p4.Rapidity()")
                .Define("GenTauP_mass",    "GenTauP_p4.M()")
                
                .Define("GenTauM_p4",     "if (HiggsGenTau_charge.at(0)==1) return HiggsGenTau_p4.at(1); else return HiggsGenTau_p4.at(0);")
                .Define("GenTauM_px",    "GenTauM_p4.Px()")
                .Define("GenTauM_py",    "GenTauM_p4.Py()")
                .Define("GenTauM_pz",    "GenTauM_p4.Pz()")
                .Define("GenTauM_p",    "GenTauM_p4.P()")
                .Define("GenTauM_pt",    "GenTauM_p4.Pt()")
                .Define("GenTauM_e",     "GenTauM_p4.E()")
                .Define("GenTauM_eta",    "GenTauM_p4.Eta()")
                .Define("GenTauM_phi",    "GenTauM_p4.Phi()")
                .Define("GenTauM_theta",    "GenTauM_p4.Theta()")
                .Define("GenTauM_y",     "GenTauM_p4.Rapidity()")
                .Define("GenTauM_mass",    "GenTauM_p4.M()")

                .Define("GenTau_scalar", "(HiggsGenTau_px.at(0)*HiggsGenTau_px.at(1) + HiggsGenTau_py.at(0)*HiggsGenTau_py.at(1) + HiggsGenTau_pz.at(0)*HiggsGenTau_pz.at(1))")
                .Define("HiggsGenTau_cos", "GenTau_scalar/(HiggsGenTau_p.at(0)*HiggsGenTau_p.at(1))")
                
                .Define("HiggsGenTau_DEta","GenTauLead_eta - GenTauSub_eta")
                .Define("HiggsGenTau_DPhi","FCCAnalyses::ZHfunctions::deltaPhi(GenTauLead_phi, GenTauSub_phi)")
                .Define("HiggsGenTau_DEta_y",    "if (GenTauLead_y>GenTauSub_y) return (GenTauLead_eta - GenTauSub_eta); \
                                        else if (GenTauLead_y<GenTauSub_y) return (GenTauSub_eta - GenTauLead_eta); else return double(-10.);")
                .Define("HiggsGenTau_DPhi_y",    "if (GenTauLead_y>GenTauSub_y) return (GenTauLead_phi - GenTauSub_phi); \
                                        else if (GenTauLead_y<GenTauSub_y) return (GenTauSub_phi - GenTauLead_phi); else return double(-10.);")
                .Define("HiggsGenTau_DR","FCCAnalyses::ZHfunctions::deltaR(HiggsGenTau_phi.at(0), HiggsGenTau_phi.at(1), HiggsGenTau_eta.at(0), HiggsGenTau_eta.at(1))")

                #####################
                ######## CP #########
                #####################

                .Define("GenHiggs_p4",      "FCCAnalyses::ZHfunctions::build_p4(GenHiggs_px, GenHiggs_py, GenHiggs_pz, GenHiggs_e)")

                #following CMS paper
                .Define("ZMF_p4",     "GenTauP_p4+GenTauM_p4")#"GenRhoP_p4+GenRhoM_p4")
                #.Define("ZMF_GenPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, GenPiP_p4)")
                #.Define("ZMF_GenPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, GenPiM_p4)")
                #.Define("ZMF_GenPi0P_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, GenPi0P_p4)")
                #.Define("ZMF_GenPi0M_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, GenPi0M_p4)")

                #.Define("yplus",        "(GenPiP_e.at(0) - GenPi0P_e)/(GenPiP_e.at(0) + GenPi0P_e)")
                #.Define("yminus",        "(GenPiM_e.at(0) - GenPi0M_e)/(GenPiM_e.at(0) + GenPi0M_e)")
                #.Define("ytau",            "yplus * yminus")

                #.Define("ZMF_LambdaP",      "ZMF_GenPi0P_p4.Vect()")
                #.Define("ZMF_LambdaM",      "ZMF_GenPi0M_p4.Vect()")
                #.Define("ZMF_qP",      "(ZMF_GenPiP_p4.Vect()).Unit()")
                #.Define("ZMF_qM",      "(ZMF_GenPiM_p4.Vect()).Unit()")

                #.Define("ZMF_HatLambdaP",       "(ZMF_LambdaP - (ZMF_LambdaP.Dot(ZMF_qP) * ZMF_qP)).Unit()") #transverse component with respect to q normalised 
                #.Define("ZMF_HatLambdaM",       "(ZMF_LambdaM - (ZMF_LambdaM.Dot(ZMF_qM) * ZMF_qM)).Unit()")

                #.Define("GenPhiCP_pre",     "acos(ZMF_HatLambdaP.Dot(ZMF_HatLambdaM))")

                #.Define("GenPhiCP",     "if (ytau>0) return GenPhiCP_pre; else return (2*3.1415 - GenPhiCP_pre);")

                #########

                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("HRF_GenTau_p4",    "FCCAnalyses::ZHfunctions::boosted_p4(- GenHiggs_p4.at(0), HiggsGenTau_p4)")
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

                .Define("HRF_GenTauP_p4",     "if (HiggsGenTau_charge.at(0)==1) return HRF_GenTau_p4.at(0); else return HRF_GenTau_p4.at(1);")
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
                
                .Define("HRF_GenTauM_p4",     "if (HiggsGenTau_charge.at(0)==1) return HRF_GenTau_p4.at(1); else return HRF_GenTau_p4.at(0);")
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

                ### angles visualisation in figure 1 (2) at pag 8 of https://arxiv.org/pdf/2205.07715, changed some of the names around
                #may be interesting to simnply keep the cosine of thetas (John Hopkins)
                #angle between H vector in lab frame and tau in H rest frame
                .Define("GenTheta2_cos",      "(GenHiggs_px.at(0)*HRF_GenTauM_px + GenHiggs_py.at(0)*HRF_GenTauM_py + GenHiggs_pz.at(0)*HRF_GenTauM_pz)/(GenHiggs_p.at(0)*HRF_GenTauM_p)")
                .Define("GenTheta2",        "acos(GenTheta2_cos)")
                .Define("Total_p4",     "FCCAnalyses::ZHfunctions::build_p4_single(0.,0.,0.,240.)")
                .Define("GenRecoil",       "(Total_p4-GenZ_p4).M()")

                #########
                # polarimetric vector from ILC paper

                .Define("TauPRF_GenPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenTauP_p4, GenPiP_p4)")
                .Define("TauPRF_GenPi0P_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenTauP_p4, GenPi0P_p4)")
                .Define("TauPRF_GenNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenTauP_p4, GenNuP_p4)")

                .Define("TauMRF_GenPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenTauM_p4, GenPiM_p4)")
                .Define("TauMRF_GenPi0M_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenTauM_p4, GenPi0M_p4)")
                .Define("TauMRF_GenNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenTauM_p4, GenNuM_p4)")


                #.Define("hP_p3",       "if (GenPi0P_e>0) return (1.777 * (TauPRF_GenPiP_p4.E() - TauPRF_GenPi0P_p4.E()) * (TauPRF_GenPiP_p4.Vect() - TauPRF_GenPi0P_p4.Vect()) + 0.5 * (TauPRF_GenPiP_p4.P() - TauPRF_GenPi0P_p4.P()) * (TauPRF_GenPiP_p4.P() - TauPRF_GenPi0P_p4.P()) * TauPRF_GenNuP_p4.Vect()); \
                #                        else return TauPRF_GenPiP_p4.Vect();")
                #.Define("hM_p3",       "if (GenPi0M_e>0) return  (1.777 * (TauMRF_GenPiM_p4.E() - TauMRF_GenPi0M_p4.E()) * (TauMRF_GenPiM_p4.Vect() - TauMRF_GenPi0M_p4.Vect()) + 0.5 * (TauMRF_GenPiM_p4.P() - TauMRF_GenPi0M_p4.P()) * (TauMRF_GenPiM_p4.P() - TauMRF_GenPi0M_p4.P()) * TauMRF_GenNuM_p4.Vect()); \
                #                        else return TauMRF_GenPiM_p4.Vect();")
                .Define("hP_p3",        "TauPRF_GenPiP_p4.Vect()")
                .Define("hM_p3",        "TauMRF_GenPiM_p4.Vect()")

                .Define("hPnorm",       "(( HRF_GenTauM_p4.Vect() ).Cross( hP_p3 )).Unit()")
                .Define("hMnorm",       "(( HRF_GenTauM_p4.Vect() ).Cross( hM_p3 )).Unit()")

                .Define("hh_norm",       "hPnorm.Cross(hMnorm)")
                .Define("CosDeltaPhi",        "hPnorm.Dot(hMnorm)")
                .Define("SinDeltaPhi",       "hh_norm.Dot( (HRF_GenTauM_p4.Vect()).Unit() )")
                .Define("GenDeltaPhi",     "atan2(SinDeltaPhi, CosDeltaPhi)")

                #########
                # gen reconstruction of the angle between decay planes in higgs rest frame

                .Define("HRF_GenNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4.at(0), GenNuP_p4)")
                .Define("HRF_GenNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4.at(0), GenNuM_p4)")

                .Define("HRF_GenPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4.at(0), GenPiP_p4)")
                .Define("HRF_GenPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4.at(0), GenPiM_p4)")
                #defined ad pi+pi0 so when there is no pi0 it's just pi so it works for both
                .Define("HRF_GenRhoP_p4",    "if (GenPi0P_e>0) return FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4.at(0), -GenRhoP_p4); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4.at(0), GenPiP_p4);")
                .Define("HRF_GenRhoM_p4",    "if (GenPi0M_e>0) return FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4.at(0), -GenRhoM_p4); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4.at(0), GenPiM_p4);")

                .Define("HRF_Pnorm",        "((( HRF_GenTauM_p4.Vect() ).Cross( HRF_GenPiP_p4.Vect() )).Unit());")
                .Define("HRF_Mnorm",        "((( HRF_GenTauM_p4.Vect() ).Cross( HRF_GenPiM_p4.Vect() )).Unit());")

                .Define("Cross_norm",       "HRF_Pnorm.Cross(HRF_Mnorm)")
                .Define("CosPhi",        "HRF_Pnorm.Dot(HRF_Mnorm)")
                .Define("SinPhi",       "Cross_norm.Dot( (HRF_GenTauM_p4.Vect()).Unit() )")
                .Define("GenPhi_decay",     "atan2(SinPhi, CosPhi)")


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
  
            "GenNuP_e",
            "GenNuP_p",
            "GenNuP_pt",
            "GenNuP_px",
            "GenNuP_py",
            "GenNuP_pz",
            "GenNuP_y",
            "GenNuP_eta",
            "GenNuP_theta",
            "GenNuP_phi",
            "GenNuP_charge",
            "GenNuP_mass",
            "GenNuP_p4",

            "GenNuM_e",
            "GenNuM_p",
            "GenNuM_pt",
            "GenNuM_px",
            "GenNuM_py",
            "GenNuM_pz",
            "GenNuM_y",
            "GenNuM_eta",
            "GenNuM_theta",
            "GenNuM_phi",
            "GenNuM_charge",
            "GenNuM_mass",
            "GenNuM_p4",

            "GenPiP_e",
            "GenPiP_p",
            "GenPiP_pt",
            "GenPiP_px",
            "GenPiP_py",
            "GenPiP_pz",
            "GenPiP_y",
            "GenPiP_eta",
            "GenPiP_theta",
            "GenPiP_phi",
            "GenPiP_charge",
            "GenPiP_mass",
            "GenPiP_p4",

            "GenPiM_e",
            "GenPiM_p",
            "GenPiM_pt",
            "GenPiM_px",
            "GenPiM_py",
            "GenPiM_pz",
            "GenPiM_y",
            "GenPiM_eta",
            "GenPiM_theta",
            "GenPiM_phi",
            "GenPiM_charge",
            "GenPiM_mass",
            "GenPiM_p4",

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

            "GenTauLead_px",    
            "GenTauLead_py",   
            "GenTauLead_pz",   
            "GenTauLead_p",   
            "GenTauLead_pt",   
            "GenTauLead_e",    
            "GenTauLead_eta",    
            "GenTauLead_phi",    
            "GenTauLead_theta",    
            "GenTauLead_y",    
            "GenTauLead_mass",

            "GenTauSub_px",    
            "GenTauSub_py",   
            "GenTauSub_pz",   
            "GenTauSub_p",   
            "GenTauSub_pt",   
            "GenTauSub_e",    
            "GenTauSub_eta",    
            "GenTauSub_phi",    
            "GenTauSub_theta",    
            "GenTauSub_y",    
            "GenTauSub_mass",

            "GenTauP_px",    
            "GenTauP_py",   
            "GenTauP_pz",   
            "GenTauP_p",   
            "GenTauP_pt",   
            "GenTauP_e",    
            "GenTauP_eta",    
            "GenTauP_phi",    
            "GenTauP_theta",    
            "GenTauP_y",    
            "GenTauP_mass",

            "GenTauM_px",    
            "GenTauM_py",   
            "GenTauM_pz",   
            "GenTauM_p",   
            "GenTauM_pt",   
            "GenTauM_e",    
            "GenTauM_eta",    
            "GenTauM_phi",    
            "GenTauM_theta",    
            "GenTauM_y",    
            "GenTauM_mass",
        
            "HiggsGenTau_DR",
            "HiggsGenTau_cos",
            "HiggsGenTau_DEta", 
            "HiggsGenTau_DPhi",
            
            "FSGenZDaughter_DR", 
            "FSGenZDaughter_cos", 
            "FSGenZDaughter_DEta", 
            "FSGenZDaughter_DPhi", 

            "HiggsGenTau_DEta_y", 
            "HiggsGenTau_DPhi_y", 
            
            "FSGenZDaughter_DEta_y", 
            "FSGenZDaughter_DPhi_y", 

            #"ytau", 
            #"GenPhiCP_pre",   
            #"GenPhiCP",   

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

            #"HRF_GenTau_DEta", 
            #"HRF_GenTau_DPhi",
            #"HRF_GenTau_DEta_y", 
            #"HRF_GenTau_DPhi_y", 

            "GenTheta2",
            "GenTheta2_cos",

            "GenRecoil",

            "TauPRF_GenPiP_p4",
            "TauMRF_GenPiM_p4",
            "TauPRF_GenNuP_p4",
            "TauMRF_GenNuM_p4",

            "hh_norm",
            "CosDeltaPhi",  
            "SinDeltaPhi",    
            "GenDeltaPhi",

            "HRF_GenPiP_p4",
            "HRF_GenPiM_p4",

            "Cross_norm",
            "CosPhi",  
            "SinPhi",    
            "GenPhi_decay",

            "Emiss_totKin",
            "Kin_TauP_p4", 
            "Kin_TauM_p4", 
            "Kin_NuP_p4", 
            "Kin_NuM_p4",   
            "CosDeltaPhiKin",   
            "SinDeltaPhiKin",   
            "DeltaPhiKin",

        ]

        return branchList