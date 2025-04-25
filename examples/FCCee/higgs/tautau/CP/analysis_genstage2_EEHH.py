import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    'noISR_e+e-_noCuts_EWonly':{},
    'noISR_e+e-_noCuts_cehim_m1':{},
    'noISR_e+e-_noCuts_cehim_p1':{},
    'noISR_e+e-_noCuts_cehre_m1':{},
    'noISR_e+e-_noCuts_cehre_p1':{},
    
    #'EWonly_taudecay_2Pi2Nu':{},
    #'cehim_m1_taudecay_2Pi2Nu':{},
    #'cehim_p1_taudecay_2Pi2Nu':{},
    #'cehre_m1_taudecay_2Pi2Nu':{},
    #'cehre_p1_taudecay_2Pi2Nu':{},

    #'EWonly_taudecay_PiPi0Nu':{},
    #'cehim_m1_taudecay_PiPi0Nu':{},
    #'cehim_p1_taudecay_PiPi0Nu':{},
    #'cehre_m1_taudecay_PiPi0Nu':{},
    #'cehre_p1_taudecay_PiPi0Nu':{},

    #'cehim_m5_taudecay_2Pi2Nu':{},
    #'cehim_p5_taudecay_2Pi2Nu':{},
    #'cehre_m5_taudecay_2Pi2Nu':{},
    #'cehre_p5_taudecay_2Pi2Nu':{},

    #'cehim_p0p1_taudecay_2Pi2Nu':{},
    #'cehim_m0p1_taudecay_2Pi2Nu':{},
    #'cehre_m0p1_taudecay_2Pi2Nu':{},
    #'cehre_p0p1_taudecay_2Pi2Nu':{},
    #'cehim_p10_taudecay_2Pi2Nu':{},
    #'cehim_m10_taudecay_2Pi2Nu':{},

    #'cehim_m2_taudecay_2Pi2Nu':{},
    #'cehim_p2_taudecay_2Pi2Nu':{},
    #'cehre_m2_taudecay_2Pi2Nu':{},
    #'cehre_p2_taudecay_2Pi2Nu':{},

    #'wzp6_ee_eeH_Htautau_ecm240': {},
}

inputDir = "/ceph/sgiappic/HiggsCP/CPReco/stage1/"

outputDir = "/ceph/sgiappic/HiggsCP/CPReco/stage2_gen/"

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

                .Filter("GenPi0P2_e>0 && GenPi0M2_e>0")
                
                ######################
                ##### FILTERING ######
                ######################
                .Define("OnePairGen",     "(n_FSGenZDaughter==2 and n_FSGenMuon_sel==0)*1.0")

                .Filter("OnePairGen==1")

                .Filter("(FSGenZDaughter_charge.at(0) + FSGenZDaughter_charge.at(1))==0")

                #################
                # Gen particles #
                #################

                .Define("GenPi0P_p4",        "GenPi0P1_p4+GenPi0P2_p4")
                .Define("GenPi0M_p4",        "GenPi0M1_p4+GenPi0M2_p4")

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

                .Define("ZMF_p4",     "GenTauP_p4+GenTauM_p4")

                .Define("GenPi_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(GenPiP_p4.at(0), GenPiM_p4.at(0))")
                .Define("GenNu_Impact_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(GenNuP_Impact_p4.at(0), GenNuM_Impact_p4.at(0))")
                .Define("GenPi0_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(GenPi0P_p4, GenPi0M_p4)")
                .Define("GenHiggs_p4",      "TLorentzVector(GenHiggs_px.at(0), GenHiggs_py.at(0), GenHiggs_pz.at(0), GenHiggs_e.at(0))")
                .Define("GenIP",        "TLorentzVector(FSGenElectron_vertex_x.at(0), FSGenElectron_vertex_y.at(0), FSGenElectron_vertex_z.at(0), 0.)")
                
                .Define("HadGenTau_p4",      "FCCAnalyses::ZHfunctions::build_p4(HadGenTau_px, HadGenTau_py, HadGenTau_pz, HadGenTau_e)")
                
                .Define("GenEmiss_p4",     "HadGenTau_p4.at(0) +  HadGenTau_p4.at(1) - GenPiP_p4.at(0) - GenPiM_p4.at(0)")
                .Define("GenEmiss_px", "GenEmiss_p4.Px()")
                .Define("GenEmiss_py", "GenEmiss_p4.Py()")
                .Define("GenEmiss_pz", "GenEmiss_p4.Pz()")
                .Define("GenEmiss_e", "GenEmiss_p4.E()")
                .Define("GenEmiss_y", "GenEmiss_p4.Rapidity()")
                .Define("GenEmiss_p", "GenEmiss_p4.P()")
                .Define("GenEmiss_pt", "GenEmiss_p4.Pt()")
                .Define("GenEmiss_eta", "GenEmiss_p4.Eta()")
                .Define("GenEmiss_phi", "GenEmiss_p4.Phi()")
                .Define("GenEmiss_theta", "GenEmiss_p4.Theta()")

                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("HRF_GenTau_p4",    "FCCAnalyses::ZHfunctions::boosted_p4(- GenHiggs_p4, HiggsGenTau_p4)")
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

                ################################################

                # polarimetric vector from ILC paper - full gen - acutally works
                # ILC paper https://arxiv.org/pdf/1804.01241

                .Define("TauPRF_GenPiP_p4",    "if (HadGenTau_charge.at(0)==1) return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(0), GenPiP_p4.at(0)); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(1), GenPiP_p4.at(0));")
                .Define("TauPRF_GenPi0P_p4",    "if (HadGenTau_charge.at(0)==1) return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(0), GenPi0P_p4); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(1), GenPi0P_p4);")
                .Define("TauPRF_GenNuP_p4",    "if (HadGenTau_charge.at(0)==1) return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(0), GenNuP_p4.at(0)); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(1), GenNuP_p4.at(0));")

                .Define("TauMRF_GenPiM_p4",    "if (HadGenTau_charge.at(0)==1) return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(1), GenPiM_p4.at(0)); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(0), GenPiM_p4.at(0));")
                .Define("TauMRF_GenPi0M_p4",    "if (HadGenTau_charge.at(0)==1) return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(1), GenPi0M_p4); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(0), GenPi0M_p4);")
                .Define("TauMRF_GenNuM_p4",    "if (HadGenTau_charge.at(0)==1) return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(1), GenNuM_p4.at(0)); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- HadGenTau_p4.at(0), GenNuM_p4.at(0));")

                #.Define("GenhP_p3",        "TauPRF_GenPiP_p4.Vect()")
                #.Define("GenhM_p3",        "TauMRF_GenPiM_p4.Vect()")
                .Define("GenhP_p3",       "if (GenPi0P_p4.E()>0) return (1.777 * (TauPRF_GenPiP_p4.E() - TauPRF_GenPi0P_p4.E()) * (TauPRF_GenPiP_p4.Vect() - TauPRF_GenPi0P_p4.Vect()) + 0.5 * (TauPRF_GenPiP_p4 + TauPRF_GenPi0P_p4).Mag2() * TauPRF_GenNuP_p4.Vect()); \
                                        else return TauPRF_GenPiP_p4.Vect();")
                .Define("GenhM_p3",       "if (GenPi0M_p4.E()>0) return  (1.777 * (TauMRF_GenPiM_p4.E() - TauMRF_GenPi0M_p4.E()) * (TauMRF_GenPiM_p4.Vect() - TauMRF_GenPi0M_p4.Vect()) + 0.5 * (TauMRF_GenPiM_p4 + TauMRF_GenPi0M_p4).Mag2() * TauMRF_GenNuM_p4.Vect()); \
                                        else return TauMRF_GenPiM_p4.Vect();")

                .Define("HRF_HadGenTau_p4",    "FCCAnalyses::ZHfunctions::boosted_p4(- GenHiggs_p4, HadGenTau_p4)")
                .Define("HRF_HadGenTauM_p4",     "if (HadGenTau_charge.at(0)==1) return HRF_HadGenTau_p4.at(1); else return HRF_HadGenTau_p4.at(0);")

                .Define("GenhPnorm",       "(( HRF_HadGenTauM_p4.Vect() ).Cross( GenhP_p3 )).Unit()")
                .Define("GenhMnorm",       "(( HRF_HadGenTauM_p4.Vect() ).Cross( GenhM_p3 )).Unit()")

                .Define("Genhh_norm",       "GenhPnorm.Cross(GenhMnorm)")
                .Define("GenCosDeltaPhi",        "GenhPnorm.Dot(GenhMnorm)")
                .Define("GenSinDeltaPhi",       "Genhh_norm.Dot( (HRF_HadGenTauM_p4.Vect()).Unit() )")
                .Define("GenDeltaPhi",     "atan2(GenSinDeltaPhi, GenCosDeltaPhi)")

                ########################################

                # gen reconstruction of the angle between decay planes in higgs rest frame - same as polarimeters, techinically more precise at gen level at least but polarimeters consider also spin correlation
                # so for other decay than pinu doesn't work very well, there are other tricks to consider in that case

                .Define("HRF_GenNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, GenNuP_p4.at(0))")
                .Define("HRF_GenNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, GenNuM_p4.at(0))")

                .Define("HRF_GenPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, GenPiP_p4.at(0))")
                .Define("HRF_GenPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, GenPiM_p4.at(0))")
                #defined ad pi+pi0 so when there is no pi0 it's just pi so it works for both
                .Define("HRF_GenRhoP_p4",    "if (GenPi0P1_e>0) return FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, -GenRhoP_p4); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, GenPiP_p4.at(0));")
                .Define("HRF_GenRhoM_p4",    "if (GenPi0M1_e>0) return FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, -GenRhoM_p4); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- GenHiggs_p4, GenPiM_p4.at(0));")

                .Define("HRF_Pnorm",        "((( HRF_GenTauM_p4.Vect() ).Cross( HRF_GenPiP_p4.Vect() )).Unit());")
                .Define("HRF_Mnorm",        "((( HRF_GenTauM_p4.Vect() ).Cross( HRF_GenPiM_p4.Vect() )).Unit());")

                .Define("Cross_norm",       "HRF_Pnorm.Cross(HRF_Mnorm)")
                .Define("CosPhi",        "HRF_Pnorm.Dot(HRF_Mnorm)")
                .Define("SinPhi",       "Cross_norm.Dot( (HRF_GenTauM_p4.Vect()).Unit() )")
                .Define("GenPhi_decay",     "atan2(SinPhi, CosPhi)")

                ###################################################

                # reference from D. Jeans https://arxiv.org/pdf/1507.01700 for tau reconstruction used in the ILC paper 
                # polarimeters for the cp angle

                .Define("GenKinILC_Nu_p4",        "FCCAnalyses::ZHfunctions::build_nu_kin_ILC(GenZ_p4, GenPi_p4, GenPi0_p4, GenNu_Impact_p4, GenIP)")
                .Filter("GenKinILC_Nu_p4.at(0).E() > 0 && GenKinILC_Nu_p4.at(1).E() > 0")

                .Define("GenKinILC_NuP_p4",       "GenKinILC_Nu_p4.at(0)")
                .Define("GenKinILC_NuM_p4",       "GenKinILC_Nu_p4.at(1)")

                .Define("GenKinILC_chi2",      "GenKinILC_Nu_p4.at(2).X()")

                .Define("GenKinILC_TauP_p4",      "GenKinILC_NuP_p4 + GenPiP_p4.at(0) + GenPi0P_p4")
                .Define("GenKinILC_TauM_p4",     "GenKinILC_NuM_p4 + GenPiM_p4.at(0) + GenPi0M_p4")

                .Define("GenKinILC_Higgs_p4",      "GenKinILC_TauP_p4 + GenKinILC_TauM_p4")

                .Define("GenTauPRF_ILCPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenKinILC_TauP_p4, GenPiP_p4.at(0))")
                .Define("GenTauPRF_ILCPi0P_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenKinILC_TauP_p4, GenPi0P_p4)")
                .Define("GenTauPRF_ILCNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenKinILC_TauP_p4, GenKinILC_NuP_p4)")

                .Define("GenTauMRF_ILCPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenKinILC_TauM_p4,  GenPiM_p4.at(0))")
                .Define("GenTauMRF_ILCPi0M_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenKinILC_TauM_p4,  GenPi0M_p4)")
                .Define("GenTauMRF_ILCNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenKinILC_TauM_p4, GenKinILC_NuM_p4)")
                
                .Define("GenILChP_p3",       "if (GenTauPRF_ILCPi0P_p4.E()>0) return (1.777 * (GenTauPRF_ILCPiP_p4.E() - GenTauPRF_ILCPi0P_p4.E()) * (GenTauPRF_ILCPiP_p4.Vect() - GenTauPRF_ILCPi0P_p4.Vect()) + 0.5 * (GenTauPRF_ILCPiP_p4 + GenTauPRF_ILCPi0P_p4).Mag2() * GenTauPRF_ILCNuP_p4.Vect()); \
                                        else return GenTauPRF_ILCPiP_p4.Vect();")
                .Define("GenILChM_p3",       "if (GenTauMRF_ILCPi0M_p4.E()>0) return  (1.777 * (GenTauMRF_ILCPiM_p4.E() - GenTauMRF_ILCPi0M_p4.E()) * (GenTauMRF_ILCPiM_p4.Vect() - GenTauMRF_ILCPi0M_p4.Vect()) + 0.5 * (GenTauMRF_ILCPiM_p4 + GenTauMRF_ILCPi0M_p4).Mag2() * GenTauMRF_ILCNuM_p4.Vect()); \
                                        else return GenTauMRF_ILCPiM_p4.Vect();")

                # get the direction on which to compute the angles from the tauM boosted into the higgs/recoil rest frame
                .Define("Gen_ILCTauM_p4",      "FCCAnalyses::ZHfunctions::boosted_p4_single(- GenKinILC_Higgs_p4, GenKinILC_TauM_p4)")

                .Define("GenILChPnorm",       "(( Gen_ILCTauM_p4.Vect() ).Cross( GenILChP_p3 )).Unit()")
                .Define("GenILChMnorm",       "(( Gen_ILCTauM_p4.Vect() ).Cross( GenILChM_p3 )).Unit()")

                .Define("GenILChh_norm",       "GenILChPnorm.Cross(GenILChMnorm)")
                .Define("GenCosDeltaPhiILC",        "GenILChPnorm.Dot(GenILChMnorm)")
                .Define("GenSinDeltaPhiILC",       "GenILChh_norm.Dot( (Gen_ILCTauM_p4.Vect()).Unit() )")
                .Define("GenDeltaPhiILC",     "atan2(GenSinDeltaPhiILC, GenCosDeltaPhiILC)") 
                .Define("RecoTotal",        "GenZ_p4 + GenKinILC_TauP_p4 + GenKinILC_TauM_p4")

                # comparison

                .Define("HadGenTauP_p4",      "if (HadGenTau_charge.at(0)==1) return HadGenTau_p4.at(0); else return HadGenTau_p4.at(1);")
                .Define("HadGenTauM_p4",      "if (HadGenTau_charge.at(0)==1) return HadGenTau_p4.at(1); else return HadGenTau_p4.at(0);")

                .Define("Gen_ILC_TauP_p4",      "HadGenTauP_p4 - GenKinILC_TauP_p4")
                .Define("Gen_ILC_TauM_p4",      "HadGenTauM_p4 - GenKinILC_TauM_p4")

                ###################### test

                .Define("GenPiP_track",     "(GenPiP_p4.at(0).Vect()).Unit()")

                .Define("Intersec_p3",      "FCCAnalyses::ZHfunctions::findIntersection((GenNuP_Impact_p4.at(0)).Vect(), GenPiP_track, GenIP.Vect(), (GenKinILC_TauP_p4.Vect()).Unit()) - GenIP.Vect()")
                .Define("DecaySign",        "(Intersec_p3.Unit()).Dot((GenKinILC_TauP_p4.Vect()).Unit())")
                .Define("DecayLength_diff",      "(Intersec_p3 + GenIP.Vect()).Mag()-((GenNuP_Impact_p4.at(0)).Vect()).Mag()")

                
                .Define("GenIntersec_p3",      "FCCAnalyses::ZHfunctions::findIntersection((GenNuP_Impact_p4.at(0)).Vect(), GenPiP_track, GenIP.Vect(), (GenTauP_p4.Vect()).Unit()) - GenIP.Vect()")
                .Define("GenDecaySign",        "(GenIntersec_p3.Unit()).Dot((GenTauP_p4.Vect()).Unit())")
                .Define("GenTau_cos",        "(((GenNuP_Impact_p4.at(0)).Vect()).Unit()).Dot((GenTauP_p4.Vect() - GenIP.Vect()).Unit())")
                .Define("GenDecayLength_diff",      "(GenIntersec_p3 + GenIP.Vect()).Mag()-((GenNuP_Impact_p4.at(0)).Vect()).Mag()")
                .Define("GenParallel",       "((GenNuP_Impact_p4.at(0)).Vect()).Unit()-((GenTauP_p4.Vect() - GenIP.Vect()).Unit())")
                .Define("GenIntersect",     "GenIntersec_p3 + GenIP.Vect() - (GenNuP_Impact_p4.at(0)).Vect()")
                .Define("GenIntersect_cos",     "((GenIntersec_p3 + GenIP.Vect()).Unit()).Dot(((GenNuP_Impact_p4.at(0)).Vect()).Unit())")

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

            "n_GenTau",
            "GenTau_e",
            "GenTau_p",
            "GenTau_pt",
            "GenTau_px",
            "GenTau_py",
            "GenTau_pz",
            "GenTau_y",
            "GenTau_eta",
            "GenTau_theta",
            "GenTau_phi",
            "GenTau_charge",
            "GenTau_mass",
            "GenTau_parentPDG",
            "GenTau_vertex_x",
            "GenTau_vertex_y",
            "GenTau_vertex_z",

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
            "GenNuP_Impact_p4",

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
            "GenNuM_Impact_p4",

            "GenPi0P1_e",
            "GenPi0P1_p",
            "GenPi0P1_pt",
            "GenPi0P1_px",
            "GenPi0P1_py",
            "GenPi0P1_pz",
            "GenPi0P1_y",
            "GenPi0P1_eta",
            "GenPi0P1_theta",
            "GenPi0P1_phi",
            "GenPi0P1_mass",
            "GenPi0P1_p4",

            "GenPi0P2_e",
            "GenPi0P2_p",
            "GenPi0P2_pt",
            "GenPi0P2_px",
            "GenPi0P2_py",
            "GenPi0P2_pz",
            "GenPi0P2_y",
            "GenPi0P2_eta",
            "GenPi0P2_theta",
            "GenPi0P2_phi",
            "GenPi0P2_mass",
            "GenPi0P2_p4",

            "GenRhoP_e",
            "GenRhoP_p",
            "GenRhoP_pt",
            "GenRhoP_px",
            "GenRhoP_py",
            "GenRhoP_pz",
            "GenRhoP_y",
            "GenRhoP_eta",
            "GenRhoP_theta",
            "GenRhoP_phi",
            "GenRhoP_mass",
            "GenRhoP_p4",

            "GenPi0M1_e",
            "GenPi0M1_p",
            "GenPi0M1_pt",
            "GenPi0M1_px",
            "GenPi0M1_py",
            "GenPi0M1_pz",
            "GenPi0M1_y",
            "GenPi0M1_eta",
            "GenPi0M1_theta",
            "GenPi0M1_phi",
            "GenPi0M1_mass",
            "GenPi0M1_p4",

            "GenPi0M2_e",
            "GenPi0M2_p",
            "GenPi0M2_pt",
            "GenPi0M2_px",
            "GenPi0M2_py",
            "GenPi0M2_pz",
            "GenPi0M2_y",
            "GenPi0M2_eta",
            "GenPi0M2_theta",
            "GenPi0M2_phi",
            "GenPi0M2_mass",
            "GenPi0M2_p4",

            "GenRhoM_e",
            "GenRhoM_p",
            "GenRhoM_pt",
            "GenRhoM_px",
            "GenRhoM_py",
            "GenRhoM_pz",
            "GenRhoM_y",
            "GenRhoM_eta",
            "GenRhoM_theta",
            "GenRhoM_phi",
            "GenRhoM_mass",
            "GenRhoM_p4",

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

            "n_GenTau_had",
            "HadGenTau_e",
            "HadGenTau_p",
            "HadGenTau_pt",
            "HadGenTau_px",
            "HadGenTau_py",
            "HadGenTau_pz",
            "HadGenTau_y",
            "HadGenTau_eta",
            "HadGenTau_theta",
            "HadGenTau_phi",
            "HadGenTau_charge",
            "HadGenTau_mass",

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

            ########## cp

            "GenEmiss_px", 
            "GenEmiss_py", 
            "GenEmiss_pz", 
            "GenEmiss_e", 
            "GenEmiss_y",
            "GenEmiss_p", 
            "GenEmiss_pt", 
            "GenEmiss_eta", 
            "GenEmiss_phi",
            "GenEmiss_theta",

            "GenPhi_decay",

            "GenCosDeltaPhi",
            "GenSinDeltaPhi",
            "GenDeltaPhi",

            "GenKinILC_TauP_p4",
            "GenKinILC_TauM_p4",
            "GenKinILC_NuP_p4",
            "GenKinILC_NuM_p4",
            "GenKinILC_Higgs_p4",
            "GenCosDeltaPhiILC", 
            "GenSinDeltaPhiILC", 
            "GenDeltaPhiILC",
            "GenKinILC_chi2",
            "Gen_ILC_TauP_p4", 
            "Gen_ILC_TauM_p4", 

            "GenIntersec_p3", 
            "GenDecaySign",      
            "GenDecayLength_diff",
            "Intersec_p3", 
            "DecaySign",      
            "DecayLength_diff",
            "GenParallel",
            "GenIntersect",
            "GenIntersect_cos",
            "GenTau_cos", 
            "GenIP",
            "RecoTotal",

            
        ]

        return branchList