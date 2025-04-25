import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    #'noISR_e+e-_noCuts_EWonly':{},
    #'noISR_e+e-_noCuts_cehim_m1':{},
    #'noISR_e+e-_noCuts_cehim_p1':{},
    #'noISR_e+e-_noCuts_cehre_m1':{},
    #'noISR_e+e-_noCuts_cehre_p1':{},
    
    'EWonly_taudecay_2Pi2Nu':{},
    'cehim_m1_taudecay_2Pi2Nu':{},
    'cehim_p1_taudecay_2Pi2Nu':{},
    'cehre_m1_taudecay_2Pi2Nu':{},
    'cehre_p1_taudecay_2Pi2Nu':{},
    
    'EWonly_taudecay_PiPi0Nu':{},
    'cehim_m1_taudecay_PiPi0Nu':{},
    'cehim_p1_taudecay_PiPi0Nu':{},
    'cehre_m1_taudecay_PiPi0Nu':{},
    'cehre_p1_taudecay_PiPi0Nu':{},

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

inputDir = "/ceph/sgiappic/HiggsCP/CPReco/stage1/"

outputDir = "/ceph/sgiappic/HiggsCP/CPReco/stage2_tag/"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
    def analysers(df):
        df2 = (df

                ### to find already made functions, this is where they are or where they can be added instead of writing them here
                ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

                ######################
                ##### FILTERING ######
                ######################
                .Define("OnePair",     "((n_RecoElectrons_sel==2 and n_RecoMuons_sel==0 and (RecoLepton_sel_charge.at(0) + RecoLepton_sel_charge.at(1))==0)*1.0)")

                .Define("TauTag_px",      "TagJet_R5_px[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_py",      "TagJet_R5_py[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_pz",      "TagJet_R5_pz[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_pt",      "TagJet_R5_pt[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_p",      "TagJet_R5_p[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_e",      "TagJet_R5_e[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_phi",      "TagJet_R5_phi[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_eta",      "TagJet_R5_eta[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_theta",      "TagJet_R5_theta[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_charge",      "TagJet_R5_charge[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_mass",      "TagJet_R5_mass[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_isG",      "TagJet_R5_isG[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_isU",      "TagJet_R5_isU[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_isD",      "TagJet_R5_isD[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_isS",      "TagJet_R5_isS[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_isC",      "TagJet_R5_isC[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_isB",      "TagJet_R5_isB[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_isTAU",      "TagJet_R5_isTAU[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("TauTag_flavor",      "TagJet_R5_flavor[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("n_TauTag_constituents",        "n_TagJet_R5_constituents[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("n_TauTag_charged_constituents",        "n_TagJet_R5_charged_constituents[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("n_TauTag_neutral_constituents",        "n_TagJet_R5_neutral_constituents[TagJet_R5_isTAU>0.5 && TagJet_R5_cleanup==1]")
                .Define("n_TauTag",          "TauTag_px.size()")

                .Define("QuarkTag_px",      "TagJet_R5_px[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_py",      "TagJet_R5_py[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_pz",      "TagJet_R5_pz[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_pt",      "TagJet_R5_pt[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_p",      "TagJet_R5_p[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_e",      "TagJet_R5_e[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_phi",      "TagJet_R5_phi[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_eta",      "TagJet_R5_eta[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_theta",      "TagJet_R5_theta[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_charge",      "TagJet_R5_charge[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_mass",      "TagJet_R5_mass[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_isG",      "TagJet_R5_isG[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_isU",      "TagJet_R5_isU[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_isD",      "TagJet_R5_isD[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_isS",      "TagJet_R5_isS[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_isC",      "TagJet_R5_isC[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_isB",      "TagJet_R5_isB[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_isTAU",      "TagJet_R5_isTAU[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("QuarkTag_flavor",      "TagJet_R5_flavor[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("n_QuarkTag_constituents",        "n_TagJet_R5_constituents[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("n_QuarkTag_charged_constituents",        "n_TagJet_R5_charged_constituents[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("n_QuarkTag_neutral_constituents",        "n_TagJet_R5_neutral_constituents[TagJet_R5_isTAU<=0.5 && TagJet_R5_cleanup==1]")
                .Define("n_QuarkTag",     "QuarkTag_charge.size()")

                ###################################

                .Filter("OnePair==1 && n_TauTag==2 && n_QuarkTag==0 && (abs(ChargedJet_charge.at(0)) + abs(ChargedJet_charge.at(1)))==2")

                ##################
                # Reco particles #
                ##################

                .Define("RecoEmiss_p4",  "TLorentzVector(RecoEmiss_px, RecoEmiss_py, RecoEmiss_pz, RecoEmiss_e)")

                .Define("ChargedJetImpactP_p4",       "if (RecoChargedJetTrack_charge.at(0)==1) return ChargedJetImpact_p4.at(0); else return ChargedJetImpact_p4.at(1);")
                .Define("ChargedJetImpactM_p4",       "if (RecoChargedJetTrack_charge.at(0)==1) return ChargedJetImpact_p4.at(1); else return ChargedJetImpact_p4.at(0);")
                .Define("Impact_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(ChargedJetImpactP_p4, ChargedJetImpactM_p4)")

                .Define("RecoPiP_p4",       "if (ChargedJet_charge.at(0)==1) return ChargedJet_p4.at(0); else return ChargedJet_p4.at(1);")
                .Define("RecoPiM_p4",       "if (ChargedJet_charge.at(0)==1) return ChargedJet_p4.at(1); else return ChargedJet_p4.at(0);")
                .Define("RecoPi_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(RecoPiP_p4, RecoPiM_p4)")

                .Define("RecoPi0P_p4",       "if (ChargedJet_charge.at(0)==1) return NeutralJet_p4.at(0); else return NeutralJet_p4.at(1);")
                .Define("RecoPi0M_p4",       "if (ChargedJet_charge.at(0)==1) return NeutralJet_p4.at(1); else return NeutralJet_p4.at(0);")
                .Define("RecoPi0_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(RecoPi0P_p4, RecoPi0M_p4)")

                ####################################

                .Define("RecoLepton_p4",  "FCCAnalyses::ZHfunctions::build_p4(RecoLepton_sel_px, RecoLepton_sel_py, RecoLepton_sel_pz, RecoLepton_sel_e)")

                #.Define("RecoZH_idx",        "FCCAnalyses::ZHfunctions::FindBest_3(RecoLepton_p4, RecoLepton_sel_charge, RecoLepton_sel_mass, 91.188)")

                .Define("RecoZ1_p4",      "TLorentzVector(RecoLepton_sel_px.at(0), RecoLepton_sel_py.at(0), RecoLepton_sel_pz.at(0), RecoLepton_sel_e.at(0))")
                .Define("RecoZ2_p4",      "TLorentzVector(RecoLepton_sel_px.at(1), RecoLepton_sel_py.at(1), RecoLepton_sel_pz.at(1), RecoLepton_sel_e.at(1))")

                .Define("RecoZLead_p4",      "if (RecoZ1_p4.Pt()>RecoZ2_p4.Pt()) return RecoZ1_p4; else return RecoZ2_p4;")
                .Define("RecoZLead_px",    "RecoZLead_p4.Px()")
                .Define("RecoZLead_py",    "RecoZLead_p4.Py()")
                .Define("RecoZLead_pz",    "RecoZLead_p4.Pz()")
                .Define("RecoZLead_p",    "RecoZLead_p4.P()")
                .Define("RecoZLead_pt",    "RecoZLead_p4.Pt()")
                .Define("RecoZLead_e",     "RecoZLead_p4.E()")
                .Define("RecoZLead_eta",    "RecoZLead_p4.Eta()")
                .Define("RecoZLead_phi",    "RecoZLead_p4.Phi()")
                .Define("RecoZLead_theta",    "RecoZLead_p4.Theta()")
                .Define("RecoZLead_y",     "RecoZLead_p4.Rapidity()")
                .Define("RecoZLead_mass",    "RecoZLead_p4.M()")

                .Define("RecoZSub_p4",      "if (RecoZ1_p4.Pt()>RecoZ2_p4.Pt()) return RecoZ2_p4; else return RecoZ1_p4;")
                .Define("RecoZSub_px",    "RecoZSub_p4.Px()")
                .Define("RecoZSub_py",    "RecoZSub_p4.Py()")
                .Define("RecoZSub_pz",    "RecoZSub_p4.Pz()")
                .Define("RecoZSub_p",    "RecoZSub_p4.P()")
                .Define("RecoZSub_pt",    "RecoZSub_p4.Pt()")
                .Define("RecoZSub_e",     "RecoZSub_p4.E()")
                .Define("RecoZSub_eta",    "RecoZSub_p4.Eta()")
                .Define("RecoZSub_phi",    "RecoZSub_p4.Phi()")
                .Define("RecoZSub_theta",    "RecoZSub_p4.Theta()")
                .Define("RecoZSub_y",     "RecoZSub_p4.Rapidity()")
                .Define("RecoZSub_mass",    "RecoZSub_p4.M()")

                .Define("RecoZP_p4",      "if (RecoLepton_sel_charge.at(0)==1) return RecoZ1_p4; else return RecoZ2_p4;")
                .Define("RecoZP_px",    "RecoZP_p4.Px()")
                .Define("RecoZP_py",    "RecoZP_p4.Py()")
                .Define("RecoZP_pz",    "RecoZP_p4.Pz()")
                .Define("RecoZP_p",    "RecoZP_p4.P()")
                .Define("RecoZP_pt",    "RecoZP_p4.Pt()")
                .Define("RecoZP_e",     "RecoZP_p4.E()")
                .Define("RecoZP_eta",    "RecoZP_p4.Eta()")
                .Define("RecoZP_phi",    "RecoZP_p4.Phi()")
                .Define("RecoZP_theta",    "RecoZP_p4.Theta()")
                .Define("RecoZP_y",     "RecoZP_p4.Rapidity()")
                .Define("RecoZP_mass",    "RecoZP_p4.M()")

                .Define("RecoZM_p4",      "if (RecoLepton_sel_charge.at(0)==1) return RecoZ2_p4; else return RecoZ1_p4;")
                .Define("RecoZM_px",    "RecoZM_p4.Px()")
                .Define("RecoZM_py",    "RecoZM_p4.Py()")
                .Define("RecoZM_pz",    "RecoZM_p4.Pz()")
                .Define("RecoZM_p",    "RecoZM_p4.P()")
                .Define("RecoZM_pt",    "RecoZM_p4.Pt()")
                .Define("RecoZM_e",     "RecoZM_p4.E()")
                .Define("RecoZM_eta",    "RecoZM_p4.Eta()")
                .Define("RecoZM_phi",    "RecoZM_p4.Phi()")
                .Define("RecoZM_theta",    "RecoZM_p4.Theta()")
                .Define("RecoZM_y",     "RecoZM_p4.Rapidity()")
                .Define("RecoZM_mass",    "RecoZM_p4.M()")

                .Define("RecoZ_p4",          "RecoZ1_p4+RecoZ2_p4")
                .Define("RecoZ_px",    "RecoZ_p4.Px()")
                .Define("RecoZ_py",    "RecoZ_p4.Py()")
                .Define("RecoZ_pz",    "RecoZ_p4.Pz()")
                .Define("RecoZ_p",    "RecoZ_p4.P()")
                .Define("RecoZ_pt",    "RecoZ_p4.Pt()")
                .Define("RecoZ_e",     "RecoZ_p4.E()")
                .Define("RecoZ_eta",    "RecoZ_p4.Eta()")
                .Define("RecoZ_phi",    "RecoZ_p4.Phi()")
                .Define("RecoZ_theta",    "RecoZ_p4.Theta()")
                .Define("RecoZ_y",     "RecoZ_p4.Rapidity()")
                .Define("RecoZ_mass",    "RecoZ_p4.M()")
                
                #.Define("RecoTau1_p4",      "TLorentzVector(TauFromJet_R5_px.at(0), TauFromJet_R5_py.at(0), TauFromJet_R5_pz.at(0), TauFromJet_R5_e.at(0))")
                #.Define("RecoTau2_p4",      "TLorentzVector(TauFromJet_R5_px.at(1), TauFromJet_R5_py.at(1), TauFromJet_R5_pz.at(1), TauFromJet_R5_e.at(1))")
                .Define("RecoTau1_p4",      "TLorentzVector(TauTag_px.at(0), TauTag_py.at(0), TauTag_pz.at(0), TauTag_e.at(0))")
                .Define("RecoTau2_p4",      "TLorentzVector(TauTag_px.at(1), TauTag_py.at(1), TauTag_pz.at(1), TauTag_e.at(1))")
                .Define("RecoTau1_type",        "TauTag_isTAU.at(0)") #"TauFromJet_R5Tag_type.at(0)")
                .Define("RecoTau2_type",        "TauTag_isTAU.at(1)") #"TauFromJet_R5Tag_type.at(1)")
                .Define("n_RecoTau1_constituents",        "n_TauTag_constituents.at(0)")
                .Define("n_RecoTau2_constituents",        "n_TauTag_constituents.at(1)")
                .Define("n_RecoTau1_charged_constituents",        "n_TauTag_charged_constituents.at(0)")
                .Define("n_RecoTau2_charged_constituents",        "n_TauTag_charged_constituents.at(1)")
                .Define("n_RecoTau1_neutral_constituents",        "n_TauTag_charged_constituents.at(0)")
                .Define("n_RecoTau2_neutral_constituents",        "n_TauTag_neutral_constituents.at(1)")

                .Define("Higgs_p4",         "RecoTau1_p4+RecoTau2_p4")
                .Define("Higgs_px",    "Higgs_p4.Px()")
                .Define("Higgs_py",    "Higgs_p4.Py()")
                .Define("Higgs_pz",    "Higgs_p4.Pz()")
                .Define("Higgs_p",    "Higgs_p4.P()")
                .Define("Higgs_pt",    "Higgs_p4.Pt()")
                .Define("Higgs_e",     "Higgs_p4.E()")
                .Define("Higgs_eta",    "Higgs_p4.Eta()")
                .Define("Higgs_phi",    "Higgs_p4.Phi()")
                .Define("Higgs_theta",    "Higgs_p4.Theta()")
                .Define("Higgs_y",     "Higgs_p4.Rapidity()")
                .Define("Higgs_mass",    "Higgs_p4.M()")
                
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
                .Define("TauLead_type",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau1_type; else return RecoTau2_type;")
                .Define("n_TauLead_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau1_constituents; else return n_RecoTau2_constituents;")
                .Define("n_TauLead_charged_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau1_charged_constituents; else return n_RecoTau2_charged_constituents;")
                .Define("n_TauLead_neutral_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau1_neutral_constituents; else return n_RecoTau2_neutral_constituents;")

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
                .Define("TauSub_type",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return RecoTau2_type; else return RecoTau1_type;")
                .Define("n_TauSub_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau2_constituents; else return n_RecoTau1_constituents;")
                .Define("n_TauSub_charged_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau2_charged_constituents; else return n_RecoTau1_charged_constituents;")
                .Define("n_TauSub_neutral_constituents",     "if (RecoTau1_p4.Pt()>RecoTau2_p4.Pt()) return n_RecoTau2_neutral_constituents; else return n_RecoTau1_neutral_constituents;")

                .Define("TauP_p4","if (ChargedJet_charge.at(0)==1) return RecoTau1_p4; else return RecoTau2_p4;")
                .Define("TauP_px",    "TauP_p4.Px()")
                .Define("TauP_py",    "TauP_p4.Py()")
                .Define("TauP_pz",    "TauP_p4.Pz()")
                .Define("TauP_p",    "TauP_p4.P()")
                .Define("TauP_pt",    "TauP_p4.Pt()")
                .Define("TauP_e",     "TauP_p4.E()")
                .Define("TauP_eta",    "TauP_p4.Eta()")
                .Define("TauP_phi",    "TauP_p4.Phi()")
                .Define("TauP_theta",    "TauP_p4.Theta()")
                .Define("TauP_y",     "TauP_p4.Rapidity()")
                .Define("TauP_mass",    "TauP_p4.M()")
                .Define("n_TauP_constituents",     "if (ChargedJet_charge.at(0)==1) return n_RecoTau1_constituents; else return n_RecoTau2_constituents;")
                .Define("n_TauP_charged_constituents",     "if (ChargedJet_charge.at(0)==1) return n_RecoTau1_charged_constituents; else return n_RecoTau2_charged_constituents;")
                .Define("n_TauP_neutral_constituents",     "if (ChargedJet_charge.at(0)==1) return n_RecoTau1_neutral_constituents; else return n_RecoTau2_neutral_constituents;")

                .Define("TauM_p4",       "if (ChargedJet_charge.at(0)==1) return RecoTau2_p4; else return RecoTau1_p4;")
                .Define("TauM_px",    "TauM_p4.Px()")
                .Define("TauM_py",    "TauM_p4.Py()")
                .Define("TauM_pz",    "TauM_p4.Pz()")
                .Define("TauM_p",    "TauM_p4.P()")
                .Define("TauM_pt",    "TauM_p4.Pt()")
                .Define("TauM_e",     "TauM_p4.E()")
                .Define("TauM_eta",    "TauM_p4.Eta()")
                .Define("TauM_phi",    "TauM_p4.Phi()")
                .Define("TauM_theta",    "TauM_p4.Theta()")
                .Define("TauM_y",     "TauM_p4.Rapidity()")
                .Define("TauM_mass",    "TauM_p4.M()")
                .Define("n_TauM_constituents",     "if (ChargedJet_charge.at(0)==1) return n_RecoTau2_constituents; else return n_RecoTau1_constituents;")
                .Define("n_TauM_charged_constituents",     "if (ChargedJet_charge.at(0)==1) return n_RecoTau2_charged_constituents; else return n_RecoTau1_charged_constituents;")
                .Define("n_TauM_neutral_constituents",     "if (ChargedJet_charge.at(0)==1) return n_RecoTau2_neutral_constituents; else return n_RecoTau1_neutral_constituents;")

                .Define("Tau_DR",       "FCCAnalyses::ZHfunctions::deltaR(TauLead_phi, TauSub_phi, TauLead_eta, TauSub_eta)")
                .Define("Tau_scalar",      "(TauLead_px*TauSub_px + TauLead_py*TauSub_py + TauLead_pz*TauSub_pz)")
                .Define("Tau_cos",      "Tau_scalar/(TauLead_p*TauSub_p)")
                .Define("Tau_DEta",    "(TauLead_eta - TauSub_eta)")
                .Define("Tau_DPhi",     "FCCAnalyses::ZHfunctions::deltaPhi(TauLead_phi, TauSub_phi)")

                .Define("RecoZDaughter_DR",       "FCCAnalyses::ZHfunctions::deltaR(RecoZLead_phi, RecoZSub_phi, RecoZLead_eta, RecoZSub_eta)")
                .Define("RecoZDaughter_scalar",      "(RecoZLead_px*RecoZSub_px + RecoZLead_py*RecoZSub_py + RecoZLead_pz*RecoZSub_pz)")
                .Define("RecoZDaughter_cos",      "RecoZDaughter_scalar/(RecoZLead_p*RecoZSub_p)")
                .Define("RecoZDaughter_DEta",    "(RecoZLead_eta - RecoZSub_eta)")
                .Define("RecoZDaughter_DPhi",    "FCCAnalyses::ZHfunctions::deltaPhi(RecoZLead_phi, RecoZSub_phi)")

                .Define("Total_p4",     "TLorentzVector(0.,0.,0.,240.)")
                .Define("Recoil",       "(Total_p4-RecoZ_p4).M()")
                .Define("Recoil_p4",       "Total_p4-RecoZ_p4")

                .Define("p12",      "(TauLead_py*TauSub_px-TauLead_px*TauSub_py)")
                .Define("r0",       "abs((RecoEmiss_py*TauLead_px-RecoEmiss_px*TauLead_py)/p12)")
                .Define("f0",       "1./(1.+r0)")
                .Define("r1",       "abs((RecoEmiss_py*TauSub_px-RecoEmiss_px*TauSub_py)/p12)")
                .Define("f1",       "1./(1.+r1)")
                .Define("Collinear_mass",       "Higgs_mass/sqrt(f0*f1)")

                #.Filter("Collinear_mass>100 && Collinear_mass<150")

                #####################
                ######## CP #########
                #####################

                # impact parameter method from CMS for decay into one pion
                # we do know the higgs rest frame / recoil frame so we can use that instead of going around it with the visible taus

                .Define("ZMF_p4",       "RecoPiP_p4+RecoPiM_p4")

                .Define("OP_ImpactP_p4",        "FCCAnalyses::ZHfunctions::ImpactFromIP(ChargedJEtImpactP_p4, RecoPiP_p4, RecoIP_p4)")
                .Define("ZMF_RecoPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, RecoPiP_p4)")
                .Define("ZMF_RecoPi0P_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, RecoPi0P_p4)")
                .Define("ZMF_ImpactP_p4",    "(FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, OP_ImpactP_p4))")
                .Define("ZMF_ImpactP_par",       "((ZMF_ImpactP_p4.Vect()).Dot((ZMF_RecoPiP_p4.Vect())))/((ZMF_RecoPiP_p4.Vect()).Mag2())*ZMF_RecoPiP_p4.Vect()")
                .Define("ZMF_ImpactP_perp",      "(ZMF_ImpactP_p4.Vect() - ZMF_ImpactP_par).Unit()")
                .Define("ZMF_RecoPi0P_par",       "((ZMF_RecoPi0P_p4.Vect()).Dot((ZMF_RecoPiP_p4.Vect())))/((ZMF_RecoPiP_p4.Vect()).Mag2())*ZMF_RecoPiP_p4.Vect()")
                .Define("ZMF_RecoPi0P_perp",      "(ZMF_RecoPi0P_p4.Vect() - ZMF_RecoPi0P_par).Unit()")

                .Define("OP_ImpactM_p4",        "FCCAnalyses::ZHfunctions::ImpactFromIP(ChargedJEtImpactM_p4, RecoPiM_p4, RecoIP_p4)")
                .Define("ZMF_RecoPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, RecoPiM_p4)")
                .Define("ZMF_RecoPi0M_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, RecoPi0M_p4)")
                .Define("ZMF_ImpactM_p4",    "(FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, OP_ImpactM_p4))")
                .Define("ZMF_ImpactM_par",       "((ZMF_ImpactM_p4.Vect()).Dot((ZMF_RecoPiM_p4.Vect())))/((ZMF_RecoPiM_p4.Vect()).Mag2())*ZMF_RecoPiM_p4.Vect()")
                .Define("ZMF_ImpactM_perp",      "(ZMF_ImpactM_p4.Vect() - ZMF_ImpactM_par).Unit()")
                .Define("ZMF_RecoPi0M_par",       "((ZMF_RecoPi0M_p4.Vect()).Dot((ZMF_RecoPiM_p4.Vect())))/((ZMF_RecoPiM_p4.Vect()).Mag2())*ZMF_RecoPiM_p4.Vect()")
                .Define("ZMF_RecoPi0M_perp",      "(ZMF_RecoPi0M_p4.Vect() - ZMF_RecoPi0M_par).Unit()")

                .Define("Phi_Recoil",       "if (ZMF_RecoPi0P_p4.E()>0 && ZMF_RecoPi0M_p4.E()>0) return acos(ZMF_RecoPi0P_perp.Dot(ZMF_RecoPi0M_perp)); else return acos(ZMF_ImpactP_perp.Dot(ZMF_ImpactM_perp));")
                .Define("y_plus",       "(RecoPiP_p4.E()-RecoPi0P_p4.E())/(RecoPiP_p4.E()+RecoPi0P_p4.E())")
                .Define("y_min",       "(RecoPiM_p4.E()-RecoPi0M_p4.E())/(RecoPiM_p4.E()+RecoPi0M_p4.E())")
                .Define("O_Recoil",         "if (ZMF_RecoPi0P_p4.E()>0 && ZMF_RecoPi0M_p4.E()>0) return (y_plus * y_min); else return ((ZMF_RecoPiM_p4.Vect()).Unit()).Dot(ZMF_ImpactP_perp.Cross(ZMF_ImpactM_perp));")

                .Define("PhiCP_CMS",        "if (O_Recoil>=0) return Phi_Recoil; else return (- Phi_Recoil);")

                ###########################################

                #following ILC paper https://arxiv.org/pdf/1804.01241 and reference from d. Jeans https://arxiv.org/pdf/1507.01700

                .Define("KinILC_Nu_p4",        "FCCAnalyses::ZHfunctions::build_nu_kin_ILC(RecoZ_p4, RecoPi_p4, RecoPi0_p4, Impact_p4, RecoIP_p4)")
                .Define("ILC_Filter",       "if (KinILC_Nu_p4.at(0).Pt() > 0 && KinILC_Nu_p4.at(0).E() > 0 && KinILC_Nu_p4.at(1).Pt() > 0 && KinILC_Nu_p4.at(1).E() > 0) return int(1); else return int(0);")

                .Define("KinILC_NuP_p4",       "KinILC_Nu_p4.at(0)")
                .Define("KinILC_NuM_p4",       "KinILC_Nu_p4.at(1)")

                .Define("KinILC_chi2",      "KinILC_Nu_p4.at(2).X()")

                .Define("KinILC_TauP_p4",      "KinILC_NuP_p4 + RecoPiP_p4 + RecoPi0P_p4")
                .Define("KinILC_TauM_p4",     "KinILC_NuM_p4 + RecoPiM_p4 + RecoPi0M_p4")

                .Define("KinILC_Higgs_p4",      "KinILC_TauP_p4 + KinILC_TauM_p4")

                .Define("TauPRF_ILCPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- KinILC_TauP_p4, RecoPiP_p4)")
                .Define("TauPRF_ILCPi0P_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- KinILC_TauP_p4, RecoPi0P_p4)")
                .Define("TauPRF_ILCNuP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- KinILC_TauP_p4, KinILC_NuP_p4)")

                .Define("TauMRF_ILCPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- KinILC_TauM_p4,  RecoPiM_p4)")
                .Define("TauMRF_ILCPi0M_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- KinILC_TauM_p4,  RecoPi0M_p4)")
                .Define("TauMRF_ILCNuM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- KinILC_TauM_p4, KinILC_NuM_p4)")
                
                .Define("ILChP_p3",       "if (TauPRF_ILCPi0P_p4.E()>0) return (1.777 * (TauPRF_ILCPiP_p4.E() - TauPRF_ILCPi0P_p4.E()) * (TauPRF_ILCPiP_p4.Vect() - TauPRF_ILCPi0P_p4.Vect()) + 0.5 * (TauPRF_ILCPiP_p4 + TauPRF_ILCPi0P_p4).Mag2() * TauPRF_ILCNuP_p4.Vect()); \
                                        else return TauPRF_ILCPiP_p4.Vect();")
                .Define("ILChM_p3",       "if (TauMRF_ILCPi0M_p4.E()>0) return  (1.777 * (TauMRF_ILCPiM_p4.E() - TauMRF_ILCPi0M_p4.E()) * (TauMRF_ILCPiM_p4.Vect() - TauMRF_ILCPi0M_p4.Vect()) + 0.5 * (TauMRF_ILCPiM_p4 + TauMRF_ILCPi0M_p4).Mag2() * TauMRF_ILCNuM_p4.Vect()); \
                                        else return TauMRF_ILCPiM_p4.Vect();")

                # get the direction on which to compute the angles from the tauM boosted into the higgs/recoil rest frame
                .Define("ILCTauM_p4",      "FCCAnalyses::ZHfunctions::boosted_p4_single(- KinILC_Higgs_p4, KinILC_TauM_p4)")

                .Define("ILChPnorm",       "(( ILCTauM_p4.Vect() ).Cross( ILChP_p3 )).Unit()")
                .Define("ILChMnorm",       "(( ILCTauM_p4.Vect() ).Cross( ILChM_p3 )).Unit()")

                .Define("ILChh_norm",       "ILChPnorm.Cross(ILChMnorm)")
                .Define("CosDeltaPhiILC",        "ILChPnorm.Dot(ILChMnorm)")
                .Define("SinDeltaPhiILC",       "ILChh_norm.Dot( (ILCTauM_p4.Vect()).Unit() )")
                .Define("DeltaPhiILC",     "atan2(SinDeltaPhiILC, CosDeltaPhiILC)") 

                .Define("ILCRecoTotal",        "RecoZ_p4 + KinILC_TauP_p4 + KinILC_TauM_p4")

                ############################
                ########### Tau ############
                ############################

                .Define("RecoH_p4",         "KinILC_Higgs_p4")
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
                
                .Define("RecoTauLead_p4",       "if (KinILC_TauP_p4.Pt()>KinILC_TauM_p4.Pt()) return KinILC_TauP_p4; else return KinILC_TauM_p4;")
                .Define("RecoTauLead_px",    "RecoTauLead_p4.Px()")
                .Define("RecoTauLead_py",    "RecoTauLead_p4.Py()")
                .Define("RecoTauLead_pz",    "RecoTauLead_p4.Pz()")
                .Define("RecoTauLead_p",    "RecoTauLead_p4.P()")
                .Define("RecoTauLead_pt",    "RecoTauLead_p4.Pt()")
                .Define("RecoTauLead_e",     "RecoTauLead_p4.E()")
                .Define("RecoTauLead_eta",    "RecoTauLead_p4.Eta()")
                .Define("RecoTauLead_phi",    "RecoTauLead_p4.Phi()")
                .Define("RecoTauLead_theta",    "RecoTauLead_p4.Theta()")
                .Define("RecoTauLead_y",     "RecoTauLead_p4.Rapidity()")
                .Define("RecoTauLead_mass",    "RecoTauLead_p4.M()")

                .Define("RecoTauSub_p4",       "if (KinILC_TauP_p4.Pt()>KinILC_TauP_p4.Pt()) return KinILC_TauM_p4; else return KinILC_TauP_p4;")
                .Define("RecoTauSub_px",    "RecoTauSub_p4.Px()")
                .Define("RecoTauSub_py",    "RecoTauSub_p4.Py()")
                .Define("RecoTauSub_pz",    "RecoTauSub_p4.Pz()")
                .Define("RecoTauSub_p",    "RecoTauSub_p4.P()")
                .Define("RecoTauSub_pt",    "RecoTauSub_p4.Pt()")
                .Define("RecoTauSub_e",     "RecoTauSub_p4.E()")
                .Define("RecoTauSub_eta",    "RecoTauSub_p4.Eta()")
                .Define("RecoTauSub_phi",    "RecoTauSub_p4.Phi()")
                .Define("RecoTauSub_theta",    "RecoTauSub_p4.Theta()")
                .Define("RecoTauSub_y",     "RecoTauSub_p4.Rapidity()")
                .Define("RecoTauSub_mass",    "RecoTauSub_p4.M()")

                .Define("RecoTauP_p4","KinILC_TauP_p4")
                .Define("RecoTauP_px",    "RecoTauP_p4.Px()")
                .Define("RecoTauP_py",    "RecoTauP_p4.Py()")
                .Define("RecoTauP_pz",    "RecoTauP_p4.Pz()")
                .Define("RecoTauP_p",    "RecoTauP_p4.P()")
                .Define("RecoTauP_pt",    "RecoTauP_p4.Pt()")
                .Define("RecoTauP_e",     "RecoTauP_p4.E()")
                .Define("RecoTauP_eta",    "RecoTauP_p4.Eta()")
                .Define("RecoTauP_phi",    "RecoTauP_p4.Phi()")
                .Define("RecoTauP_theta",    "RecoTauP_p4.Theta()")
                .Define("RecoTauP_y",     "RecoTauP_p4.Rapidity()")
                .Define("RecoTauP_mass",    "RecoTauP_p4.M()")

                .Define("RecoTauM_p4",       "KinILC_TauM_p4")
                .Define("RecoTauM_px",    "RecoTauM_p4.Px()")
                .Define("RecoTauM_py",    "RecoTauM_p4.Py()")
                .Define("RecoTauM_pz",    "RecoTauM_p4.Pz()")
                .Define("RecoTauM_p",    "RecoTauM_p4.P()")
                .Define("RecoTauM_pt",    "RecoTauM_p4.Pt()")
                .Define("RecoTauM_e",     "RecoTauM_p4.E()")
                .Define("RecoTauM_eta",    "RecoTauM_p4.Eta()")
                .Define("RecoTauM_phi",    "RecoTauM_p4.Phi()")
                .Define("RecoTauM_theta",    "RecoTauM_p4.Theta()")
                .Define("RecoTauM_y",     "RecoTauM_p4.Rapidity()")
                .Define("RecoTauM_mass",    "RecoTauM_p4.M()")

                .Define("RecoTau_DR",       "FCCAnalyses::ZHfunctions::deltaR(RecoTauLead_phi, RecoTauSub_phi, RecoTauLead_eta, RecoTauSub_eta)")
                .Define("RecoTau_scalar",      "(RecoTauLead_px*RecoTauSub_px + RecoTauLead_py*RecoTauSub_py + RecoTauLead_pz*RecoTauSub_pz)")
                .Define("RecoTau_cos",      "RecoTau_scalar/(RecoTauLead_p*RecoTauSub_p)")
                .Define("RecoTau_DEta",    "(RecoTauLead_eta - RecoTauSub_eta)")
                .Define("RecoTau_DPhi",     "FCCAnalyses::ZHfunctions::deltaPhi(RecoTauLead_phi, RecoTauSub_phi)")

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
            #"GenPiP_Impact_p4",

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
            #"GenPiM_Impact_p4",

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
        branchList +=[

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

            #"n_RecoTracks",
            #"RecoVertexObject",
            #"RecoVertex",
            #"n_PrimaryTracks",
            #"PrimaryVertexObject",
            #"PrimaryVertex", 
            #"PrimaryVertex_xyz",
            #"PrimaryVertes_xy",
            #"n_SecondaryTracks",
            #"SecondaryVertexObject",
            #"SecondaryVertex",
            #"SecondaryVertex_xyz",
            #"SecondaryVertes_xy",
            #"VertexObject", 
            #"RecoPartPID" ,
            #"RecoPartPIDAtVertex",

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

            "n_ChargedHadron",
            "ChargedHadron_e",
            "ChargedHadron_p",
            "ChargedHadron_pt",
            "ChargedHadron_px",
            "ChargedHadron_py",
            "ChargedHadron_pz",
            "ChargedHadron_eta",
            "ChargedHadron_theta",
            "ChargedHadron_phi",
            "ChargedHadron_charge",
            "ChargedHadron_mass",
            "ChargedHadron_p4",

            "n_NeutralHadron",
            "NeutralHadron_e",
            "NeutralHadron_p",
            "NeutralHadron_pt",
            "NeutralHadron_px",
            "NeutralHadron_py",
            "NeutralHadron_pz",
            "NeutralHadron_eta",
            "NeutralHadron_theta",
            "NeutralHadron_phi",
            "NeutralHadron_charge",
            "NeutralHadron_mass",
            "NeutralHadron_p4",

            "n_ChargedTau",
            "ChargedTau_e",
            "ChargedTau_p",
            "ChargedTau_pt",
            "ChargedTau_px",
            "ChargedTau_py",
            "ChargedTau_pz",
            "ChargedTau_eta",
            "ChargedTau_theta",
            "ChargedTau_phi",
            "ChargedTau_charge",
            "ChargedTau_mass",
            "ChargedTau_p4",

            "n_NeutralTau",
            "NeutralTau_e",
            "NeutralTau_p",
            "NeutralTau_pt",
            "NeutralTau_px",
            "NeutralTau_py",
            "NeutralTau_pz",
            "NeutralTau_eta",
            "NeutralTau_theta",
            "NeutralTau_phi",
            "NeutralTau_charge",
            "NeutralTau_mass",
            "NeutralTau_p4",

            "n_ChargedJet",
            "ChargedJet_e",
            "ChargedJet_p",
            "ChargedJet_pt",
            "ChargedJet_px",
            "ChargedJet_py",
            "ChargedJet_pz",
            "ChargedJet_eta",
            "ChargedJet_theta",
            "ChargedJet_phi",
            "ChargedJet_charge",
            "ChargedJet_mass",
            "ChargedJet_p4",

            "n_NeutralJet",
            "NeutralJet_e",
            "NeutralJet_p",
            "NeutralJet_pt",
            "NeutralJet_px",
            "NeutralJet_py",
            "NeutralJet_pz",
            "NeutralJet_eta",
            "NeutralJet_theta",
            "NeutralJet_phi",
            "NeutralJet_charge",
            "NeutralJet_mass",
            "NeutralJet_p4",

            "ChargedHadronImpact_p4", 
            "ChargedTauImpact_p4", 
            "ChargedJetImpact_p4", 
            "RecoIP_p4",

            "RecoChargedHadronTrack_D0",
            "RecoChargedHadronTrack_Z0",
            "RecoChargedHadronTrack_charge",
            "RecoChargedHadronTrack_omega",

            "RecoChargedTauTrack_D0",
            "RecoChargedTauTrack_Z0",
            "RecoChargedTauTrack_charge",
            "RecoChargedTauTrack_omega",

            "RecoChargedJetTrack_D0",
            "RecoChargedJetTrack_Z0",
            "RecoChargedJetTrack_charge",
            "RecoChargedJetTrack_omega",

        ]
        branchList += [
            ######## stage2

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

            "RecoZP_px", 
            "RecoZP_py",   
            "RecoZP_pz",   
            "RecoZP_p",    
            "RecoZP_pt",   
            "RecoZP_e",    
            "RecoZP_eta",    
            "RecoZP_phi",    
            "RecoZP_theta",   
            "RecoZP_y",     
            "RecoZP_mass",   

            "RecoZM_px",    
            "RecoZM_py",   
            "RecoZM_pz",   
            "RecoZM_p",   
            "RecoZM_pt",  
            "RecoZM_e",     
            "RecoZM_eta",   
            "RecoZM_phi",   
            "RecoZM_theta",    
            "RecoZM_y",    
            "RecoZM_mass", 

            "Higgs_px",
            "Higgs_py",
            "Higgs_pz",
            "Higgs_p",
            "Higgs_pt",
            "Higgs_e",
            "Higgs_eta",
            "Higgs_phi",
            "Higgs_theta",
            "Higgs_y",
            "Higgs_mass",

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

            ########## cp
            "Recoil_p4",

            "ZMF_ImpactP_par",
            "ZMF_ImpactM_par",
            "Phi_Recoil",
            "O_Recoil",      
            "PhiCP_CMS",

            "KinILC_TauP_p4",
            "KinILC_TauM_p4",
            "KinILC_NuP_p4",
            "KinILC_NuM_p4",
            "KinILC_Higgs_p4",
            "TauPRF_ILCPiP_p4",   
            "TauPRF_ILCPi0P_p4", 
            "TauPRF_ILCNuP_p4",  
            "TauMRF_ILCPiM_p4",   
            "TauMRF_ILCPi0M_p4", 
            "TauMRF_ILCNuM_p4", 
            "CosDeltaPhiILC", 
            "SinDeltaPhiILC", 
            "DeltaPhiILC",
            "KinILC_chi2",
            "ILC_Filter", 
            "ILCRecoTotal",

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

            "RecoTauLead_px",    
            "RecoTauLead_py",   
            "RecoTauLead_pz",   
            "RecoTauLead_p",   
            "RecoTauLead_pt",   
            "RecoTauLead_e",    
            "RecoTauLead_eta",    
            "RecoTauLead_phi",    
            "RecoTauLead_theta",    
            "RecoTauLead_y",    
            "RecoTauLead_mass",

            "RecoTauSub_px",    
            "RecoTauSub_py",   
            "RecoTauSub_pz",   
            "RecoTauSub_p",   
            "RecoTauSub_pt",   
            "RecoTauSub_e",    
            "RecoTauSub_eta",    
            "RecoTauSub_phi",    
            "RecoTauSub_theta",    
            "RecoTauSub_y",    
            "RecoTauSub_mass",

            "RecoTauP_px", 
            "RecoTauP_py",   
            "RecoTauP_pz",   
            "RecoTauP_p",    
            "RecoTauP_pt",   
            "RecoTauP_e",    
            "RecoTauP_eta",    
            "RecoTauP_phi",    
            "RecoTauP_theta",   
            "RecoTauP_y",     
            "RecoTauP_mass",   

            "RecoTauM_px",    
            "RecoTauM_py",   
            "RecoTauM_pz",   
            "RecoTauM_p",   
            "RecoTauM_pt",  
            "RecoTauM_e",     
            "RecoTauM_eta",   
            "RecoTauM_phi",   
            "RecoTauM_theta",    
            "RecoTauM_y",    
            "RecoTauM_mass", 

            "RecoTau_DR",
            "RecoTau_cos",
            "RecoTau_DEta", 
            "RecoTau_DPhi",
        ]

        return branchList