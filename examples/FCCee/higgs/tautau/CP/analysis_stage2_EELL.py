import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
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

inputDir = "/ceph/sgiappic/HiggsCP/CP/stage1_tag"

outputDir = "/ceph/sgiappic/HiggsCP/CP/stage2_tag_EELL"

#Optional: ncpus, default is 4
nCPUS = 10

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

                .Define("TauTag_px",      "TagJet_R5_px[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_py",      "TagJet_R5_py[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_pz",      "TagJet_R5_pz[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_pt",      "TagJet_R5_pt[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_p",      "TagJet_R5_p[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_e",      "TagJet_R5_e[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_phi",      "TagJet_R5_phi[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_eta",      "TagJet_R5_eta[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_theta",      "TagJet_R5_theta[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_charge",      "TagJet_R5_charge[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_mass",      "TagJet_R5_mass[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_isG",      "TagJet_R5_isG[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_isU",      "TagJet_R5_isU[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_isD",      "TagJet_R5_isD[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_isS",      "TagJet_R5_isS[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_isC",      "TagJet_R5_isC[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_isB",      "TagJet_R5_isB[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_isTAU",      "TagJet_R5_isTAU[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("TauTag_flavor",      "TagJet_R5_flavor[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("n_TauTag_constituents",        "n_TagJet_R5_constituents[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("n_TauTag_charged_constituents",        "n_TagJet_R5_charged_constituents[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("n_TauTag_neutral_constituents",        "n_TagJet_R5_neutral_constituents[TagJet_R5_isTAU>0.5 && abs(TagJet_R5_charge)==1 && TagJet_R5_mass<3]")
                .Define("n_TauTag",          "TauTag_px.size()")

                .Define("QuarkTag_px",      "TagJet_R5_px[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_py",      "TagJet_R5_py[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_pz",      "TagJet_R5_pz[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_pt",      "TagJet_R5_pt[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_p",      "TagJet_R5_p[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_e",      "TagJet_R5_e[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_phi",      "TagJet_R5_phi[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_eta",      "TagJet_R5_eta[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_theta",      "TagJet_R5_theta[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_charge",      "TagJet_R5_charge[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_mass",      "TagJet_R5_mass[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_isG",      "TagJet_R5_isG[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_isU",      "TagJet_R5_isU[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_isD",      "TagJet_R5_isD[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_isS",      "TagJet_R5_isS[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_isC",      "TagJet_R5_isC[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_isB",      "TagJet_R5_isB[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_isTAU",      "TagJet_R5_isTAU[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("QuarkTag_flavor",      "TagJet_R5_flavor[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("n_QuarkTag_constituents",        "n_TagJet_R5_constituents[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("n_QuarkTag_charged_constituents",        "n_TagJet_R5_charged_constituents[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("n_QuarkTag_neutral_constituents",        "n_TagJet_R5_neutral_constituents[TagJet_R5_isTAU<=0.5 || abs(TagJet_R5_charge)!=1 || TagJet_R5_mass>=3]")
                .Define("n_QuarkTag",     "QuarkTag_charge.size()")

                ######################
                ##### FILTERING ######
                ######################

                .Define("AllLeptons",    "((n_RecoElectrons==4 and n_RecoMuons==0) and (RecoLepton_charge.at(0) + RecoLepton_charge.at(1) + RecoLepton_charge.at(2) + RecoLepton_charge.at(3))==0)*1.0")
                .Define("TwoPairs",     "((n_RecoElectrons==2 and n_RecoMuons==2) and (RecoElectron_charge.at(0) + RecoElectron_charge.at(1))==0 and (RecoMuon_charge.at(0) + RecoMuon_charge.at(1))==0)*1.0")
                .Define("OnePair",     "((n_RecoElectrons==3 and n_RecoMuons==1)  and (RecoLepton_charge.at(0) + RecoLepton_charge.at(1) + RecoLepton_charge.at(2) + RecoLepton_charge.at(3))==0)*1.0")

                #.Filter("(AllLeptons==1 || TwoPairs==1 || OnePair==1) && n_TagJet_R5_sel==0 && n_TauFromJet_R5Tag==0") 

                ###########################
                
                .Filter("(AllLeptons==1 || TwoPairs==1 || OnePair==1) && n_TauTag==0 && n_QuarkTag==0") 

                #.Filter("(RecoElectron_charge.at(0) + RecoElectron_charge.at(1))==0")

                #.Filter("(TauTag_charge.at(0) + TauTag_charge.at(1))==0")

                #select one prong decay >> leading pi is the constituent individuated here

                #.Filter("n_TauTag_charged_constituents.at(0)==1 && n_TauTag_charged_constituents.at(1)==1")

                ##############################

                #one prong decay of both taus

                #.Filter("OnePair==1 && n_TauFromJet_R5==2 && n_Jets_R5_sel==0")

                #.Filter("(TauFromJet_R5_charge.at(0) + TauFromJet_R5_charge.at(1))==0")

                #.Filter("TauFromJet_R5_type.at(0)==2 and TauFromJet_R5_type.at(1)==2")

                ##################
                # Reco particles #
                ##################

                .Define("RecoLepton_p4",  "FCCAnalyses::ZHfunctions::build_p4(RecoLepton_px, RecoLepton_py, RecoLepton_pz, RecoLepton_e)")

                .Define("RecoZH_idx",        "FCCAnalyses::ZHfunctions::FindBest_4(RecoLepton_p4, RecoLepton_charge, RecoLepton_mass, 91.188, 125.25)")

                .Define("RecoZ1_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(RecoLepton_px.at(RecoZH_idx[0]), RecoLepton_py.at(RecoZH_idx[0]), RecoLepton_pz.at(RecoZH_idx[0]), RecoLepton_e.at(RecoZH_idx[0]))")
                .Define("RecoZ2_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(RecoLepton_px.at(RecoZH_idx[1]), RecoLepton_py.at(RecoZH_idx[1]), RecoLepton_pz.at(RecoZH_idx[1]), RecoLepton_e.at(RecoZH_idx[1]))")

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

                .Define("RecoZP_p4",      "if (RecoLepton_charge.at(RecoZH_idx[0])==1) return RecoZ1_p4; else return RecoZ2_p4;")
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

                .Define("RecoZM_p4",      "if (RecoLepton_charge.at(RecoZH_idx[0])==1) return RecoZ2_p4; else return RecoZ1_p4;")
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

                .Define("RecoZ_p4",          "RecoZLead_p4+RecoZSub_p4")
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
                
                .Define("RecoTau1_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(RecoLepton_px.at(RecoZH_idx[2]), RecoLepton_py.at(RecoZH_idx[2]), RecoLepton_pz.at(RecoZH_idx[2]), RecoLepton_e.at(RecoZH_idx[2]))")
                .Define("RecoTau2_p4",      "FCCAnalyses::ZHfunctions::build_p4_single(RecoLepton_px.at(RecoZH_idx[3]), RecoLepton_py.at(RecoZH_idx[3]), RecoLepton_pz.at(RecoZH_idx[3]), RecoLepton_e.at(RecoZH_idx[3]))")
                .Define("RecoTau1_type",        "if (RecoLepton_mass.at(RecoZH_idx[2])<0.05) return float(-0.11); else return float(-0.13);")
                .Define("RecoTau2_type",        "if (RecoLepton_mass.at(RecoZH_idx[2])<0.05) return float(-0.13); else return float(-0.11);")
                .Define("n_RecoTau1_constituents",        "return float(1);")
                .Define("n_RecoTau2_constituents",        "return float(1);")
                .Define("n_RecoTau1_charged_constituents",        "return float(1);")
                .Define("n_RecoTau2_charged_constituents",        "return float(1);")
                .Define("n_RecoTau1_neutral_constituents",        "return float(0);")
                .Define("n_RecoTau2_neutral_constituents",        "return float(0);")

                #.Define("TauDaughter1_p4",        "FCCAnalyses::ZHfunctions::build_p4_single(TauDaughter_px.at(0), TauDaughter_py.at(0), TauDaughter_pz.at(0), TauDaughter_e.at(0))")
                #.Define("TauDaughter2_p4",        "FCCAnalyses::ZHfunctions::build_p4_single(TauDaughter_px.at(1), TauDaughter_py.at(1), TauDaughter_pz.at(1), TauDaughter_e.at(1))")

                .Define("RecoH_p4",         "RecoTau1_p4+RecoTau2_p4")
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

                .Define("TauP_p4","if (RecoLepton_charge.at(RecoZH_idx[2])==1) return RecoTau1_p4; else return RecoTau2_p4;")
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
                .Define("TauP_type",     "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return RecoTau1_type; else return RecoTau2_type;")
                .Define("n_TauP_constituents",     "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return n_RecoTau1_constituents; else return n_RecoTau2_constituents;")
                .Define("n_TauP_charged_constituents",     "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return n_RecoTau1_charged_constituents; else return n_RecoTau2_charged_constituents;")
                .Define("n_TauP_neutral_constituents",     "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return n_RecoTau1_neutral_constituents; else return n_RecoTau2_neutral_constituents;")

                .Define("TauM_p4",       "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return RecoTau2_p4; else return RecoTau1_p4;")
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
                .Define("TauM_type",     "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return RecoTau2_type; else return RecoTau1_type;")
                .Define("n_TauM_constituents",     "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return n_RecoTau2_constituents; else return n_RecoTau1_constituents;")
                .Define("n_TauM_charged_constituents",     "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return n_RecoTau2_charged_constituents; else return n_RecoTau1_charged_constituents;")
                .Define("n_TauM_neutral_constituents",     "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return n_RecoTau2_neutral_constituents; else return n_RecoTau1_neutral_constituents;")

                .Define("Tau_DR",       "FCCAnalyses::ZHfunctions::deltaR(TauLead_phi, TauSub_phi, TauLead_eta, TauSub_eta)")
                .Define("Tau_scalar",      "(TauLead_px*TauSub_px + TauLead_py*TauSub_py + TauLead_pz*TauSub_pz)")
                .Define("Tau_cos",      "Tau_scalar/(TauLead_p*TauSub_p)")
                .Define("Tau_DEta",    "(TauLead_eta - TauSub_eta)")
                .Define("Tau_DPhi",    "(TauLead_phi - TauSub_phi)")

                .Define("RecoZDaughter_DR",       "FCCAnalyses::ZHfunctions::deltaR(RecoZLead_phi, RecoZSub_phi, RecoZLead_eta, RecoZSub_eta)")
                .Define("RecoZDaughter_scalar",      "(RecoZLead_px*RecoZSub_px + RecoZLead_py*RecoZSub_py + RecoZLead_pz*RecoZSub_pz)")
                .Define("RecoZDaughter_cos",      "RecoZDaughter_scalar/(RecoZLead_p*RecoZSub_p)")
                .Define("RecoZDaughter_DEta",    "(RecoZLead_eta - RecoZSub_eta)")
                .Define("RecoZDaughter_DPhi",    "(RecoZLead_phi - RecoZSub_phi)")

                .Define("Total_p4",     "FCCAnalyses::ZHfunctions::build_p4_single(0.,0.,0.,240.)")
                .Define("Recoil",       "(Total_p4-RecoZ_p4).M()")

                .Define("p12",      "(TauLead_py*TauSub_px-TauLead_px*TauSub_py)")
                .Define("r0",       "abs((RecoEmiss_py*TauLead_px-RecoEmiss_px*TauLead_py)/p12)")
                .Define("f0",       "1./(1.+r0)")
                .Define("r1",       "abs((RecoEmiss_py*TauSub_px-RecoEmiss_px*TauSub_py)/p12)")
                .Define("f1",       "1./(1.+r1)")
                .Define("Collinear_mass",       "RecoH_mass/sqrt(f0*f1)")

                #### reco CP angular variables

                .Define("Tau_DEta_y",    "if (TauLead_y>TauSub_y) return (TauLead_eta - TauSub_eta); \
                                        else if (TauLead_y<TauSub_y) return (TauSub_eta - TauLead_eta); else return double(-10.);")
                .Define("Tau_DPhi_y",    "if (TauLead_y>TauSub_y) return (TauLead_phi - TauSub_phi); \
                                        else if (TauLead_y<TauSub_y) return (TauSub_phi - TauLead_phi); else return double(-10.);")

                .Define("RecoZDaughter_DEta_y",    "if (RecoZLead_y>RecoZSub_y) return (RecoZLead_eta - RecoZSub_eta); \
                                        else if (RecoZLead_y<RecoZSub_y) return (RecoZSub_eta - RecoZLead_eta); else return double(-10.);")
                .Define("RecoZDaughter_DPhi_y",    "if (RecoZLead_y>RecoZSub_y) return (RecoZLead_phi - RecoZSub_phi); \
                                        else if (RecoZLead_y<RecoZSub_y) return (RecoZSub_phi - RecoZLead_phi); else return double(-10.);")

                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("Tau_p4",       "ROOT::VecOps::RVec<TLorentzVector>{RecoTau1_p4, RecoTau2_p4}")
                .Define("HRF_Tau_p4",    "myUtils::boosted_p4(- RecoH_p4, Tau_p4)")
                
                .Define("HRF_TauLead_p4",       "if (HRF_Tau_p4.at(0).Pt()>HRF_Tau_p4.at(1).Pt()) return HRF_Tau_p4.at(0); else return HRF_Tau_p4.at(1);")
                .Define("HRF_TauLead_px",    "HRF_TauLead_p4.Px()")
                .Define("HRF_TauLead_py",    "HRF_TauLead_p4.Py()")
                .Define("HRF_TauLead_pz",    "HRF_TauLead_p4.Pz()")
                .Define("HRF_TauLead_p",    "HRF_TauLead_p4.P()")
                .Define("HRF_TauLead_pt",    "HRF_TauLead_p4.Pt()")
                .Define("HRF_TauLead_e",     "HRF_TauLead_p4.E()")
                .Define("HRF_TauLead_eta",    "HRF_TauLead_p4.Eta()")
                .Define("HRF_TauLead_phi",    "HRF_TauLead_p4.Phi()")
                .Define("HRF_TauLead_theta",    "HRF_TauLead_p4.Theta()")
                .Define("HRF_TauLead_y",     "HRF_TauLead_p4.Rapidity()")
                .Define("HRF_TauLead_mass",    "HRF_TauLead_p4.M()")

                .Define("HRF_TauSub_p4",       "if (HRF_Tau_p4.at(0).Pt()>HRF_Tau_p4.at(1).Pt()) return HRF_Tau_p4.at(1); else return HRF_Tau_p4.at(0);")
                .Define("HRF_TauSub_px",    "HRF_TauSub_p4.Px()")
                .Define("HRF_TauSub_py",    "HRF_TauSub_p4.Py()")
                .Define("HRF_TauSub_pz",    "HRF_TauSub_p4.Pz()")
                .Define("HRF_TauSub_p",    "HRF_TauSub_p4.P()")
                .Define("HRF_TauSub_pt",    "HRF_TauSub_p4.Pt()")
                .Define("HRF_TauSub_e",     "HRF_TauSub_p4.E()")
                .Define("HRF_TauSub_eta",    "HRF_TauSub_p4.Eta()")
                .Define("HRF_TauSub_phi",    "HRF_TauSub_p4.Phi()")
                .Define("HRF_TauSub_theta",    "HRF_TauSub_p4.Theta()")
                .Define("HRF_TauSub_y",     "HRF_TauSub_p4.Rapidity()")
                .Define("HRF_TauSub_mass",    "HRF_TauSub_p4.M()")

                .Define("HRF_TauP_p4",       "if(RecoLepton_charge.at(RecoZH_idx[2])==1) return HRF_Tau_p4.at(0); else return HRF_Tau_p4.at(1);")
                .Define("HRF_TauP_px",    "HRF_TauP_p4.Px()")
                .Define("HRF_TauP_py",    "HRF_TauP_p4.Py()")
                .Define("HRF_TauP_pz",    "HRF_TauP_p4.Pz()")
                .Define("HRF_TauP_p",    "HRF_TauP_p4.P()")
                .Define("HRF_TauP_pt",    "HRF_TauP_p4.Pt()")
                .Define("HRF_TauP_e",     "HRF_TauP_p4.E()")
                .Define("HRF_TauP_eta",    "HRF_TauP_p4.Eta()")
                .Define("HRF_TauP_phi",    "HRF_TauP_p4.Phi()")
                .Define("HRF_TauP_theta",    "HRF_TauP_p4.Theta()")
                .Define("HRF_TauP_y",     "HRF_TauP_p4.Rapidity()")
                .Define("HRF_TauP_mass",    "HRF_TauP_p4.M()")

                .Define("HRF_TauM_p4",       "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return HRF_Tau_p4.at(1); else return HRF_Tau_p4.at(0);")
                .Define("HRF_TauM_px",    "HRF_TauM_p4.Px()")
                .Define("HRF_TauM_py",    "HRF_TauM_p4.Py()")
                .Define("HRF_TauM_pz",    "HRF_TauM_p4.Pz()")
                .Define("HRF_TauM_p",    "HRF_TauM_p4.P()")
                .Define("HRF_TauM_pt",    "HRF_TauM_p4.Pt()")
                .Define("HRF_TauM_e",     "HRF_TauM_p4.E()")
                .Define("HRF_TauM_eta",    "HRF_TauM_p4.Eta()")
                .Define("HRF_TauM_phi",    "HRF_TauM_p4.Phi()")
                .Define("HRF_TauM_theta",    "HRF_TauM_p4.Theta()")
                .Define("HRF_TauM_y",     "HRF_TauM_p4.Rapidity()")
                .Define("HRF_TauM_mass",    "HRF_TauM_p4.M()")

                .Define("HRF_Tau_DEta_y",    "if (HRF_TauLead_y>HRF_TauSub_y) return (HRF_TauLead_eta - HRF_TauSub_eta); \
                                        else if (HRF_TauLead_y<HRF_TauSub_y) return (HRF_TauSub_eta - HRF_TauLead_eta); else return double(-10.);")
                .Define("HRF_Tau_DPhi_y",    "if (HRF_TauLead_y>HRF_TauSub_y) return (HRF_TauLead_phi - HRF_TauSub_phi); \
                                        else if (HRF_TauLead_y<HRF_TauSub_y) return (HRF_TauSub_phi - HRF_TauLead_phi); else return double(-10.);")

                .Define("HRF_Tau_DEta",    "(HRF_TauLead_eta - HRF_TauSub_eta)")
                .Define("HRF_Tau_DPhi",    "(HRF_TauLead_phi - HRF_TauSub_phi)")

                #boosted_p4 function will boost a vector of 4-vectors(_tlv, last component is the time/energy), to go to the rest frame you need to use the inverse vector 
                .Define("RecoZDaughter_p4",     "ROOT::VecOps::RVec<TLorentzVector>{RecoZ1_p4, RecoZ2_p4}")
                .Define("ZRF_RecoZDaughter_p4",    "return myUtils::boosted_p4(- RecoZ_p4, RecoZDaughter_p4);")

                .Define("ZRF_RecoZLead_p4",       "if (ZRF_RecoZDaughter_p4.at(0).Pt()>ZRF_RecoZDaughter_p4.at(1).Pt()) return ZRF_RecoZDaughter_p4.at(0); else return ZRF_RecoZDaughter_p4.at(1);")
                .Define("ZRF_RecoZLead_px",    "ZRF_RecoZLead_p4.Px()")
                .Define("ZRF_RecoZLead_py",    "ZRF_RecoZLead_p4.Py()")
                .Define("ZRF_RecoZLead_pz",    "ZRF_RecoZLead_p4.Pz()")
                .Define("ZRF_RecoZLead_p",    "ZRF_RecoZLead_p4.P()")
                .Define("ZRF_RecoZLead_pt",    "ZRF_RecoZLead_p4.Pt()")
                .Define("ZRF_RecoZLead_e",     "ZRF_RecoZLead_p4.E()")
                .Define("ZRF_RecoZLead_eta",    "ZRF_RecoZLead_p4.Eta()")
                .Define("ZRF_RecoZLead_phi",    "ZRF_RecoZLead_p4.Phi()")
                .Define("ZRF_RecoZLead_theta",    "ZRF_RecoZLead_p4.Theta()")
                .Define("ZRF_RecoZLead_y",     "ZRF_RecoZLead_p4.Rapidity()")
                .Define("ZRF_RecoZLead_mass",    "ZRF_RecoZLead_p4.M()")

                .Define("ZRF_RecoZSub_p4",       "if (ZRF_RecoZDaughter_p4.at(0).Pt()>ZRF_RecoZDaughter_p4.at(1).Pt()) return ZRF_RecoZDaughter_p4.at(1); else return ZRF_RecoZDaughter_p4.at(0);")
                .Define("ZRF_RecoZSub_px",    "ZRF_RecoZSub_p4.Px()")
                .Define("ZRF_RecoZSub_py",    "ZRF_RecoZSub_p4.Py()")
                .Define("ZRF_RecoZSub_pz",    "ZRF_RecoZSub_p4.Pz()")
                .Define("ZRF_RecoZSub_p",    "ZRF_RecoZSub_p4.P()")
                .Define("ZRF_RecoZSub_pt",    "ZRF_RecoZSub_p4.Pt()")
                .Define("ZRF_RecoZSub_e",     "ZRF_RecoZSub_p4.E()")
                .Define("ZRF_RecoZSub_eta",    "ZRF_RecoZSub_p4.Eta()")
                .Define("ZRF_RecoZSub_phi",    "ZRF_RecoZSub_p4.Phi()")
                .Define("ZRF_RecoZSub_theta",    "ZRF_RecoZSub_p4.Theta()")
                .Define("ZRF_RecoZSub_y",     "ZRF_RecoZSub_p4.Rapidity()")
                .Define("ZRF_RecoZSub_mass",    "ZRF_RecoZSub_p4.M()")

                .Define("ZRF_RecoZP_p4",       "if (RecoLepton_charge.at(RecoZH_idx[0])==1) return ZRF_RecoZDaughter_p4.at(0); else return ZRF_RecoZDaughter_p4.at(1);")
                .Define("ZRF_RecoZP_px",    "ZRF_RecoZP_p4.Px()")
                .Define("ZRF_RecoZP_py",    "ZRF_RecoZP_p4.Py()")
                .Define("ZRF_RecoZP_pz",    "ZRF_RecoZP_p4.Pz()")
                .Define("ZRF_RecoZP_p",    "ZRF_RecoZP_p4.P()")
                .Define("ZRF_RecoZP_pt",    "ZRF_RecoZP_p4.Pt()")
                .Define("ZRF_RecoZP_e",     "ZRF_RecoZP_p4.E()")
                .Define("ZRF_RecoZP_eta",    "ZRF_RecoZP_p4.Eta()")
                .Define("ZRF_RecoZP_phi",    "ZRF_RecoZP_p4.Phi()")
                .Define("ZRF_RecoZP_theta",    "ZRF_RecoZP_p4.Theta()")
                .Define("ZRF_RecoZP_y",     "ZRF_RecoZP_p4.Rapidity()")
                .Define("ZRF_RecoZP_mass",    "ZRF_RecoZP_p4.M()")

                .Define("ZRF_RecoZM_p4",       "if (RecoLepton_charge.at(RecoZH_idx[0])==1) return ZRF_RecoZDaughter_p4.at(1); else return ZRF_RecoZDaughter_p4.at(0);")
                .Define("ZRF_RecoZM_px",    "ZRF_RecoZM_p4.Px()")
                .Define("ZRF_RecoZM_py",    "ZRF_RecoZM_p4.Py()")
                .Define("ZRF_RecoZM_pz",    "ZRF_RecoZM_p4.Pz()")
                .Define("ZRF_RecoZM_p",    "ZRF_RecoZM_p4.P()")
                .Define("ZRF_RecoZM_pt",    "ZRF_RecoZM_p4.Pt()")
                .Define("ZRF_RecoZM_e",     "ZRF_RecoZM_p4.E()")
                .Define("ZRF_RecoZM_eta",    "ZRF_RecoZM_p4.Eta()")
                .Define("ZRF_RecoZM_phi",    "ZRF_RecoZM_p4.Phi()")
                .Define("ZRF_RecoZM_theta",    "ZRF_RecoZM_p4.Theta()")
                .Define("ZRF_RecoZM_y",     "ZRF_RecoZM_p4.Rapidity()")
                .Define("ZRF_RecoZM_mass",    "ZRF_RecoZM_p4.M()")

                .Define("ZRF_RecoZDaughter_DEta_y",    "if (ZRF_RecoZLead_y>ZRF_RecoZSub_y) return (ZRF_RecoZLead_eta - ZRF_RecoZSub_eta); \
                                        else if (ZRF_RecoZLead_y<ZRF_RecoZSub_y) return (ZRF_RecoZSub_eta - ZRF_RecoZLead_eta); else return double(-10.);")
                .Define("ZRF_RecoZDaughter_DPhi_y",    "if (ZRF_RecoZLead_y>ZRF_RecoZSub_y) return (ZRF_RecoZLead_phi - ZRF_RecoZSub_phi); \
                                        else if (ZRF_RecoZLead_y<ZRF_RecoZSub_y) return (ZRF_RecoZSub_phi - ZRF_RecoZLead_phi); else return double(-10.);")

                .Define("ZRF_RecoZDaughter_DEta",    "(ZRF_RecoZLead_eta - ZRF_RecoZSub_eta)")
                .Define("ZRF_RecoZDaughter_DPhi",    "(ZRF_RecoZLead_phi - ZRF_RecoZSub_phi)")

                ### angles visualisation in figure 1 (2) at pag 8 of https://arxiv.org/pdf/2205.07715
                #may be interesting to simnply keep the cosine of thetas (John Hopkins)
                #angle between beam line and Z decay plane
                .Define("Beam_vec",     "FCCAnalyses::ZHfunctions::build_p4_single(0, 0, 1, 0)") #unitary vector of beam axis along z
                .Define("Beam_p",       "float(1.)") #magnitude
                #angle between H vector in lab frame and tau in H rest frame
                .Define("RecoTheta2_cos",      "(RecoH_px*HRF_TauM_px + RecoH_py*HRF_TauM_py + RecoH_pz*HRF_TauM_pz)/(RecoH_p*HRF_TauM_p)")
                #angle between Z vector in lab frame and Muon in Z rest frame
                .Define("RecoTheta1_cos",      "(RecoZ_px*ZRF_RecoZM_px + RecoZ_py*ZRF_RecoZM_py + RecoZ_pz*ZRF_RecoZM_pz)/(RecoZ_p*ZRF_RecoZM_p)")
                #angle between decay planes of H and Z
                .Define("RecoPhi_cos",      "(HRF_TauM_px*ZRF_RecoZM_px + HRF_TauM_py*ZRF_RecoZM_py + HRF_TauM_pz*ZRF_RecoZM_pz)/(HRF_TauM_p*ZRF_RecoZM_p)")
                #angle between beam line and Z decay plane
                .Define("RecoPhi1_cos",      "(RecoZM_pz)/(Beam_p*ZRF_RecoZM_p)")
                .Define("RecoThetastar_cos",      "(RecoZ_pz)/(Beam_p*RecoZ_p)")

                .Define("RecoThetastar",        "(acos(RecoThetastar_cos))")
                .Define("RecoTheta1",        "(acos(RecoTheta1_cos))")
                .Define("RecoTheta2",        "(acos(RecoTheta2_cos))")
                .Define("RecoPhi",        "(acos(RecoPhi_cos))")
                .Define("RecoPhi1",        "(acos(RecoPhi1_cos))")


        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        #branches from stage1 to be kept for histogram booking in final and plotting
        branchList = [
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

            "n_NeutralHadrons",
            "NeutralHadrons_e",
            "NeutralHadrons_p",
            "NeutralHadrons_pt",
            "NeutralHadrons_px",
            "NeutralHadrons_py",
            "NeutralHadrons_pz",
            "NeutralHadrons_eta",
            "NeutralHadrons_theta",
            "NeutralHadrons_phi",
            "NeutralHadrons_charge",
            "NeutralHadrons_mass",

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
            "n_Jets_R5", 
 
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
            "n_Jets_R5_sel", 

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

            "TagJet_R5_isG",  
            "TagJet_R5_isU",
            "TagJet_R5_isD",   
            "TagJet_R5_isS",  
            "TagJet_R5_isC",
            "TagJet_R5_isB",  
            "TagJet_R5_isTAU",

            "n_GenTau_had", 
            "n_TauTag_R5_match",  
            "n_TauTag_R5_mass_match",
            "n_events_tag",  
            "n_events_tag_mass",
            "n_TauTag_R5_match5",  
            "n_TauTag_R5_mass_match5",
            "n_events_tag5",  
            "n_events_tag5_mass",
            "n_events_func",  

            "n_LeadingPi",
            "LeadingPi_e",
            "LeadingPi_p",
            "LeadingPi_pt",
            "LeadingPi_px",
            "LeadingPi_py",
            "LeadingPi_pz",
            "LeadingPi_eta",
            "LeadingPi_theta",
            "LeadingPi_phi",
            "LeadingPi_charge",
            "LeadingPi_mass",
        ]
        #complex variables added here at stage2
        branchList += [
            ### Reconstructed particles ###
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
            "n_TauTag_constituents", 
            "n_TauTag_charged_constituents",  
            "n_TauTag_neutral_constituents",                   
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
            "n_QuarkTag_constituents", 
            "n_QuarkTag_charged_constituents",  
            "n_QuarkTag_neutral_constituents",      
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
            "n_TauP_constituents",
            "n_TauP_charged_constituents",
            "n_TauP_neutral_constituents",

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
            "n_TauM_constituents",
            "n_TauM_charged_constituents",
            "n_TauM_neutral_constituents",

            "Recoil",
            "Collinear_mass", 
        
            "Tau_DR",
            "Tau_cos",
            "Tau_DEta", 
            "Tau_DPhi",
            "Tau_DEta_y", 
            "Tau_DPhi_y", 
            
            "RecoZDaughter_DR", 
            "RecoZDaughter_cos", 
            "RecoZDaughter_DEta", 
            "RecoZDaughter_DPhi", 
            "RecoZDaughter_DEta_y", 
            "RecoZDaughter_DPhi_y", 

            "HRF_TauLead_px",  
            "HRF_TauLead_py",  
            "HRF_TauLead_pz", 
            "HRF_TauLead_p", 
            "HRF_TauLead_pt",  
            "HRF_TauLead_e",   
            "HRF_TauLead_eta", 
            "HRF_TauLead_phi",  
            "HRF_TauLead_theta",    
            "HRF_TauLead_y", 

            "HRF_TauSub_px",  
            "HRF_TauSub_py",  
            "HRF_TauSub_pz", 
            "HRF_TauSub_p", 
            "HRF_TauSub_pt",  
            "HRF_TauSub_e",   
            "HRF_TauSub_eta", 
            "HRF_TauSub_phi",  
            "HRF_TauSub_theta",    
            "HRF_TauSub_y", 

            "HRF_TauP_px",  
            "HRF_TauP_py",  
            "HRF_TauP_pz", 
            "HRF_TauP_p", 
            "HRF_TauP_pt",  
            "HRF_TauP_e",   
            "HRF_TauP_eta", 
            "HRF_TauP_phi",  
            "HRF_TauP_theta",    
            "HRF_TauP_y", 

            "HRF_TauM_px",  
            "HRF_TauM_py",  
            "HRF_TauM_pz", 
            "HRF_TauM_p", 
            "HRF_TauM_pt",  
            "HRF_TauM_e",   
            "HRF_TauM_eta", 
            "HRF_TauM_phi",  
            "HRF_TauM_theta",    
            "HRF_TauM_y", 

            "HRF_Tau_DEta", 
            "HRF_Tau_DPhi",
            "HRF_Tau_DEta_y", 
            "HRF_Tau_DPhi_y", 

            "ZRF_RecoZLead_px",  
            "ZRF_RecoZLead_py",  
            "ZRF_RecoZLead_pz", 
            "ZRF_RecoZLead_p", 
            "ZRF_RecoZLead_pt",  
            "ZRF_RecoZLead_e",   
            "ZRF_RecoZLead_eta", 
            "ZRF_RecoZLead_phi",  
            "ZRF_RecoZLead_theta",    
            "ZRF_RecoZLead_y", 

            "ZRF_RecoZSub_px",  
            "ZRF_RecoZSub_py",  
            "ZRF_RecoZSub_pz", 
            "ZRF_RecoZSub_p", 
            "ZRF_RecoZSub_pt",  
            "ZRF_RecoZSub_e",   
            "ZRF_RecoZSub_eta", 
            "ZRF_RecoZSub_phi",  
            "ZRF_RecoZSub_theta",    
            "ZRF_RecoZSub_y", 

            "ZRF_RecoZP_px",  
            "ZRF_RecoZP_py",  
            "ZRF_RecoZP_pz", 
            "ZRF_RecoZP_p", 
            "ZRF_RecoZP_pt",  
            "ZRF_RecoZP_e",   
            "ZRF_RecoZP_eta", 
            "ZRF_RecoZP_phi",  
            "ZRF_RecoZP_theta",    
            "ZRF_RecoZP_y", 

            "ZRF_RecoZM_px",  
            "ZRF_RecoZM_py",  
            "ZRF_RecoZM_pz", 
            "ZRF_RecoZM_p", 
            "ZRF_RecoZM_pt",  
            "ZRF_RecoZM_e",   
            "ZRF_RecoZM_eta", 
            "ZRF_RecoZM_phi",  
            "ZRF_RecoZM_theta",    
            "ZRF_RecoZM_y", 

            "ZRF_RecoZDaughter_DEta", 
            "ZRF_RecoZDaughter_DPhi",
            "ZRF_RecoZDaughter_DEta_y", 
            "ZRF_RecoZDaughter_DPhi_y", 

            "RecoThetastar",
            "RecoTheta2",
            "RecoPhi1", 
            "RecoPhi", 
            "RecoTheta1", 

            "RecoThetastar_cos",
            "RecoTheta2_cos",
            "RecoPhi1_cos", 
            "RecoPhi_cos", 
            "RecoTheta1_cos", 

        ]

        return branchList