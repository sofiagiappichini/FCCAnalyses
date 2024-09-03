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

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/winter2023/IDEA/"

inputDir_xsec = "/ceph/sgiappic/HiggsCP/winter23"

#Optional: output directory, default is local running directory
outputDir_xsec   = "/ceph/awiedl/FCCee/HiggsCP/stage1/"

inputDir_EFT = "/ceph/mpresill/FCCee/ZH_SMEFT_LO_noISR_noCuts_prod/ele"

outputDir_EFT = "/ceph/sgiappic/HiggsCP/CP/stage1"

#Optional: ncpus, default is 4
nCPUS = 10

if EFT :
    processList = processList_EFT
    inputDir = inputDir_EFT
    outputDir = outputDir_EFT
else:
    processList = processList_xsec
    inputDir = inputDir_xsec
    outputDir = outputDir_xsec

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df

                #################
                # Gen particles #
                #################

                .Alias("Particle0", "Particle#0.index")
                .Alias("Particle1", "Particle#1.index")
                .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
                .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

                #all final state gen electrons and positrons
                .Define("GenElectron_PID", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
                .Define("FSGenElectron", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenElectron_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenElectron", "FCCAnalyses::MCParticle::get_n(FSGenElectron)")
                .Define("FSGenElectron_e", "FCCAnalyses::MCParticle::get_e(FSGenElectron)")
                .Define("FSGenElectron_p", "FCCAnalyses::MCParticle::get_p(FSGenElectron)")
                .Define("FSGenElectron_pt", "FCCAnalyses::MCParticle::get_pt(FSGenElectron)")
                .Define("FSGenElectron_px", "FCCAnalyses::MCParticle::get_px(FSGenElectron)")
                .Define("FSGenElectron_py", "FCCAnalyses::MCParticle::get_py(FSGenElectron)")
                .Define("FSGenElectron_pz", "FCCAnalyses::MCParticle::get_pz(FSGenElectron)")
                .Define("FSGenElectron_y", "FCCAnalyses::MCParticle::get_y(FSGenElectron)") #rapidity
                .Define("FSGenElectron_eta", "FCCAnalyses::MCParticle::get_eta(FSGenElectron)")
                .Define("FSGenElectron_theta", "FCCAnalyses::MCParticle::get_theta(FSGenElectron)")
                .Define("FSGenElectron_phi", "FCCAnalyses::MCParticle::get_phi(FSGenElectron)")
                .Define("FSGenElectron_charge", "FCCAnalyses::MCParticle::get_charge(FSGenElectron)")
                .Define("FSGenElectron_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenElectron)")
                .Define("FSGenElectron_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenElectron,Particle,Particle0)")
                .Define("FSGenElectron_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( FSGenElectron )")
                .Define("FSGenElectron_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( FSGenElectron )")
                .Define("FSGenElectron_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( FSGenElectron )")
                
                #all final state gen muons 
                .Define("GenMuon_PID", "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
                .Define("FSGenMuon", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenMuon_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenMuon", "FCCAnalyses::MCParticle::get_n(FSGenMuon)")
                .Define("FSGenMuon_e", "FCCAnalyses::MCParticle::get_e(FSGenMuon)")
                .Define("FSGenMuon_p", "FCCAnalyses::MCParticle::get_p(FSGenMuon)")
                .Define("FSGenMuon_pt", "FCCAnalyses::MCParticle::get_pt(FSGenMuon)")
                .Define("FSGenMuon_px", "FCCAnalyses::MCParticle::get_px(FSGenMuon)")
                .Define("FSGenMuon_py", "FCCAnalyses::MCParticle::get_py(FSGenMuon)")
                .Define("FSGenMuon_pz", "FCCAnalyses::MCParticle::get_pz(FSGenMuon)")
                .Define("FSGenMuon_y", "FCCAnalyses::MCParticle::get_y(FSGenMuon)")
                .Define("FSGenMuon_eta", "FCCAnalyses::MCParticle::get_eta(FSGenMuon)")
                .Define("FSGenMuon_theta", "FCCAnalyses::MCParticle::get_theta(FSGenMuon)")
                .Define("FSGenMuon_phi", "FCCAnalyses::MCParticle::get_phi(FSGenMuon)")
                .Define("FSGenMuon_charge", "FCCAnalyses::MCParticle::get_charge(FSGenMuon)")
                .Define("FSGenMuon_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenMuon)")
                .Define("FSGenMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenMuon,Particle,Particle0)")
                .Define("FSGenMuon_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( FSGenMuon )")
                .Define("FSGenMuon_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( FSGenMuon )")
                .Define("FSGenMuon_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( FSGenMuon )")
                
                #need to define a class only for muons coming from the Z
                #info on gen Z are not kept at all, muons seem to come directly from initial state electron
                .Define("ZFSGenMuon",   "FCCAnalyses::MCParticle::sel_parentID(15, false, true)(FSGenMuon,Particle,Particle0)")
                .Define("n_ZFSGenMuon", "FCCAnalyses::MCParticle::get_n(ZFSGenMuon)")
                .Define("ZFSGenMuon_e", "FCCAnalyses::MCParticle::get_e(ZFSGenMuon)")
                .Define("ZFSGenMuon_p", "FCCAnalyses::MCParticle::get_p(ZFSGenMuon)")
                .Define("ZFSGenMuon_pt", "FCCAnalyses::MCParticle::get_pt(ZFSGenMuon)")
                .Define("ZFSGenMuon_px", "FCCAnalyses::MCParticle::get_px(ZFSGenMuon)")
                .Define("ZFSGenMuon_py", "FCCAnalyses::MCParticle::get_py(ZFSGenMuon)")
                .Define("ZFSGenMuon_pz", "FCCAnalyses::MCParticle::get_pz(ZFSGenMuon)")
                .Define("ZFSGenMuon_y", "FCCAnalyses::MCParticle::get_y(ZFSGenMuon)")
                .Define("ZFSGenMuon_eta", "FCCAnalyses::MCParticle::get_eta(ZFSGenMuon)")
                .Define("ZFSGenMuon_theta", "FCCAnalyses::MCParticle::get_theta(ZFSGenMuon)")
                .Define("ZFSGenMuon_phi", "FCCAnalyses::MCParticle::get_phi(ZFSGenMuon)")
                .Define("ZFSGenMuon_charge", "FCCAnalyses::MCParticle::get_charge(ZFSGenMuon)")
                .Define("ZFSGenMuon_mass",   "FCCAnalyses::MCParticle::get_mass(ZFSGenMuon)")
                .Define("ZFSGenMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(ZFSGenMuon,Particle,Particle0)")
                .Define("ZFSGenMuon_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( ZFSGenMuon )")
                .Define("ZFSGenMuon_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( ZFSGenMuon )")
                .Define("ZFSGenMuon_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( ZFSGenMuon )")

                #distinguish between pre fsr and after iterative fsr taus and keep them in separate classes to be analysed
                .Define("AllGenTauPlus",    "FCCAnalyses::MCParticle::sel_pdgID(-15, false)(Particle)")
                .Define("n_GenTauPlus",      "FCCAnalyses::MCParticle::get_n(AllGenTauPlus)")
                .Define("noFSRGenTauPlus",       "FCCAnalyses::MCParticle::sel_parentID(-15, false, false)(AllGenTauPlus,Particle,Particle0)")
                #.Define("FSRGenTauPlus_parent",       "FCCAnalyses::MCParticle::sel_parentID(-15, true, false)(AllGenTauPlus,Particle,Particle0)")
                #.Define("noFSRGenTauPlus_daughter",       "if (noFSRGenTauPlus_parent.size()>0) return FCCAnalyses::MCParticle::sel_daughterID(-15, true, false)(noFSRGenTauPlus_parent,Particle,Particle1); else return ROOT::VecOps::RVec<edm4hep::MCParticleData>{};")
                .Define("FSRGenTauPlus",       "FCCAnalyses::MCParticle::sel_daughterID(-15, false, false)(AllGenTauPlus,Particle,Particle1)")
                
                .Define("AllGenTauMin",    "FCCAnalyses::MCParticle::sel_pdgID(15, false)(Particle)")
                .Define("n_GenTauMin",      "FCCAnalyses::MCParticle::get_n(AllGenTauMin)")
                .Define("noFSRGenTauMin",       "FCCAnalyses::MCParticle::sel_parentID(15, false, false)(AllGenTauMin,Particle,Particle0)")
                #.Define("FSRGenTauMin_parent",       "FCCAnalyses::MCParticle::sel_parentID(15, true, false)(AllGenTauMin,Particle,Particle0)")
                #.Define("noFSRGenTauMin_daughter",       "if (noFSRGenTauMin_parent.size()>0) return FCCAnalyses::MCParticle::sel_daughterID(15, true, false)(noFSRGenTauMin_parent,Particle,Particle1); else return ROOT::VecOps::RVec<edm4hep::MCParticleData>{};")
                .Define("FSRGenTauMin",       "FCCAnalyses::MCParticle::sel_daughterID(15, false, false)(AllGenTauMin,Particle,Particle1)")
                
                .Define("AllGenTau",           "FCCAnalyses::MCParticle::mergeParticles(AllGenTauPlus, AllGenTauMin)")
                .Define("n_AllGenTau",      "FCCAnalyses::MCParticle::get_n(AllGenTau)")
                .Define("AllGenTau_e",     "FCCAnalyses::MCParticle::get_e(AllGenTau)")
                .Define("AllGenTau_p",     "FCCAnalyses::MCParticle::get_p(AllGenTau)")
                .Define("AllGenTau_pt",     "FCCAnalyses::MCParticle::get_pt(AllGenTau)")
                .Define("AllGenTau_px",     "FCCAnalyses::MCParticle::get_px(AllGenTau)")
                .Define("AllGenTau_py",     "FCCAnalyses::MCParticle::get_py(AllGenTau)")
                .Define("AllGenTau_pz",     "FCCAnalyses::MCParticle::get_pz(AllGenTau)")
                .Define("AllGenTau_y",    "FCCAnalyses::MCParticle::get_y(AllGenTau)")
                .Define("AllGenTau_eta",    "FCCAnalyses::MCParticle::get_eta(AllGenTau)")
                .Define("AllGenTau_theta",     "FCCAnalyses::MCParticle::get_theta(AllGenTau)")
                .Define("AllGenTau_phi",    "FCCAnalyses::MCParticle::get_phi(AllGenTau)")
                .Define("AllGenTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(AllGenTau,Particle,Particle0)")
                .Define("AllGenTau_charge", "FCCAnalyses::MCParticle::get_charge(AllGenTau)")
                .Define("AllGenTau_mass",   "FCCAnalyses::MCParticle::get_mass(AllGenTau)")
                .Define("AllGenTau_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( AllGenTau )")
                .Define("AllGenTau_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( AllGenTau )")
                .Define("AllGenTau_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( AllGenTau )")
                
                .Define("noFSRGenTau",           "FCCAnalyses::MCParticle::mergeParticles(noFSRGenTauPlus, noFSRGenTauMin)")
                .Define("noFSRGenTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(noFSRGenTau,Particle,Particle0)")

                .Define("FSRGenTau",           "FCCAnalyses::MCParticle::mergeParticles(FSRGenTauPlus, FSRGenTauMin)")
                .Define("n_FSRGenTau",      "FCCAnalyses::MCParticle::get_n(FSRGenTau)")
                .Define("FSRGenTau_e",     "FCCAnalyses::MCParticle::get_e(FSRGenTau)")
                .Define("FSRGenTau_p",     "FCCAnalyses::MCParticle::get_p(FSRGenTau)")
                .Define("FSRGenTau_pt",     "FCCAnalyses::MCParticle::get_pt(FSRGenTau)")
                .Define("FSRGenTau_px",     "FCCAnalyses::MCParticle::get_px(FSRGenTau)")
                .Define("FSRGenTau_py",     "FCCAnalyses::MCParticle::get_py(FSRGenTau)")
                .Define("FSRGenTau_pz",     "FCCAnalyses::MCParticle::get_pz(FSRGenTau)")
                .Define("FSRGenTau_y",    "FCCAnalyses::MCParticle::get_y(FSRGenTau)")
                .Define("FSRGenTau_eta",    "FCCAnalyses::MCParticle::get_eta(FSRGenTau)")
                .Define("FSRGenTau_theta",     "FCCAnalyses::MCParticle::get_theta(FSRGenTau)")
                .Define("FSRGenTau_phi",    "FCCAnalyses::MCParticle::get_phi(FSRGenTau)")
                .Define("FSRGenTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSRGenTau,Particle,Particle0)")
                .Define("FSRGenTau_charge", "FCCAnalyses::MCParticle::get_charge(FSRGenTau)")
                .Define("FSRGenTau_mass",   "FCCAnalyses::MCParticle::get_mass(FSRGenTau)")
                .Define("FSRGenTau_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( FSRGenTau )")
                .Define("FSRGenTau_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( FSRGenTau )")
                .Define("FSRGenTau_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( FSRGenTau )")

                .Define("ind_tauneg_MuNuNu",       "FCCAnalyses::MCParticle::get_indices(  15, {13,-14,16},            true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_tauneg_MuNuNu_Phot",  "FCCAnalyses::MCParticle::get_indices(  15, {13,-14,16,22},         true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_tauneg_ENuNu",        "FCCAnalyses::MCParticle::get_indices(  15, {11,-12,16},            true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_tauneg_ENuNu_Phot",   "FCCAnalyses::MCParticle::get_indices(  15, {11,-12,16,22},         true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_tauneg_PiNu",         "FCCAnalyses::MCParticle::get_indices(  15, {-211,16},              true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_tauneg_PiNu_Phot",    "FCCAnalyses::MCParticle::get_indices(  15, {-211,16,22},           true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_tauneg_KNu",          "FCCAnalyses::MCParticle::get_indices(  15, {-321,16},              true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_tauneg_KNu_Phot",     "FCCAnalyses::MCParticle::get_indices(  15, {-321,16,22},           true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_tauneg_PiK0Nu",       "FCCAnalyses::MCParticle::get_indices(  15, {-211,-311,16},         true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_tauneg_PiK0Nu_Phot",  "FCCAnalyses::MCParticle::get_indices(  15, {-211,-311,16,22},      true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_tauneg_KK0Nu",        "FCCAnalyses::MCParticle::get_indices(  15, {-321,311,16},          true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_tauneg_KK0Nu_Phot",   "FCCAnalyses::MCParticle::get_indices(  15, {-321,311,16,22},       true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_tauneg_3PiNu",        "FCCAnalyses::MCParticle::get_indices(  15, {-211,-211,211,16},     true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_tauneg_3PiNu_Phot",   "FCCAnalyses::MCParticle::get_indices(  15, {-211,-211,211,16,22},  true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_tauneg_PiKKNu",       "FCCAnalyses::MCParticle::get_indices(  15, {-211,-321,321,16},     true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_tauneg_PiKKNu_Phot",  "FCCAnalyses::MCParticle::get_indices(  15, {-211,-321,321,16,22},  true, false, false, true)  ( Particle, Particle1)" )

                .Define("ind_taupos_MuNuNu",       "FCCAnalyses::MCParticle::get_indices( -15, {-13,14,-16},           true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_taupos_MuNuNu_Phot",  "FCCAnalyses::MCParticle::get_indices( -15, {-13,14,-16,22},        true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_taupos_ENuNu",        "FCCAnalyses::MCParticle::get_indices( -15, {-11,12,-16},           true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_taupos_ENuNu_Phot",   "FCCAnalyses::MCParticle::get_indices( -15, {-11,12,-16,22},        true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_taupos_PiNu",         "FCCAnalyses::MCParticle::get_indices( -15, {211,-16},              true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_taupos_PiNu_Phot",    "FCCAnalyses::MCParticle::get_indices( -15, {211,-16,22},           true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_taupos_KNu",          "FCCAnalyses::MCParticle::get_indices( -15, {321,-16},              true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_taupos_KNu_Phot",     "FCCAnalyses::MCParticle::get_indices( -15, {321,-16,22},           true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_taupos_PiK0Nu",       "FCCAnalyses::MCParticle::get_indices( -15, {211,311,-16},          true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_taupos_PiK0Nu_Phot",  "FCCAnalyses::MCParticle::get_indices( -15, {211,311,-16,22},       true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_taupos_KK0Nu",        "FCCAnalyses::MCParticle::get_indices( -15, {321,-311,-16},         true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_taupos_KK0Nu_Phot",   "FCCAnalyses::MCParticle::get_indices( -15, {321,-311,-16,22},      true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_taupos_3PiNu",        "FCCAnalyses::MCParticle::get_indices( -15, {211,211,-211,-16},     true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_taupos_3PiNu_Phot",   "FCCAnalyses::MCParticle::get_indices( -15, {211,211,-211,-16,22},  true, false, false, true)  ( Particle, Particle1)" )
                .Define("ind_taupos_PiKKNu",       "FCCAnalyses::MCParticle::get_indices( -15, {211,321,-321,-16},     true, false, false, false) ( Particle, Particle1)" )
                .Define("ind_taupos_PiKKNu_Phot",  "FCCAnalyses::MCParticle::get_indices( -15, {211,321,-321,-16,22},  true, false, false, true)  ( Particle, Particle1)" )

                .Define("n_TauNeg_MuNuNu",       "return int(ind_tauneg_MuNuNu.size() )"     )
                .Define("n_TauNeg_MuNuNu_Phot",  "return int(ind_tauneg_MuNuNu_Phot.size() )")
                .Define("n_TauNeg_ENuNu",        "return int(ind_tauneg_ENuNu.size() )"      )
                .Define("n_TauNeg_ENuNu_Phot",   "return int(ind_tauneg_ENuNu_Phot.size() )" )
                .Define("n_TauNeg_PiNu",         "return int(ind_tauneg_PiNu.size() )"       )
                .Define("n_TauNeg_PiNu_Phot",    "return int(ind_tauneg_PiNu_Phot.size() )"  )
                .Define("n_TauNeg_KNu",          "return int(ind_tauneg_KNu.size() )"        )
                .Define("n_TauNeg_KNu_Phot",     "return int(ind_tauneg_KNu_Phot.size() )"   )
                .Define("n_TauNeg_PiK0Nu",       "return int(ind_tauneg_PiK0Nu.size() )"     )
                .Define("n_TauNeg_PiK0Nu_Phot",  "return int(ind_tauneg_PiK0Nu_Phot.size() )")
                .Define("n_TauNeg_KK0Nu",        "return int(ind_tauneg_KK0Nu.size() )"      )
                .Define("n_TauNeg_KK0Nu_Phot",   "return int(ind_tauneg_KK0Nu_Phot.size() )" )
                .Define("n_TauNeg_3PiNu",        "return int(ind_tauneg_3PiNu.size() )"      )
                .Define("n_TauNeg_3PiNu_Phot",   "return int(ind_tauneg_3PiNu_Phot.size() )" )
                .Define("n_TauNeg_PiKKNu",       "return int(ind_tauneg_PiKKNu.size() )"     )
                .Define("n_TauNeg_PiKKNu_Phot",  "return int(ind_tauneg_PiKKNu_Phot.size() )")
                                                    
                .Define("n_TauPos_MuNuNu",       "return int(ind_taupos_MuNuNu.size() )"     )
                .Define("n_TauPos_MuNuNu_Phot",  "return int(ind_taupos_MuNuNu_Phot.size() )")
                .Define("n_TauPos_ENuNu",        "return int(ind_taupos_ENuNu.size() )"      )
                .Define("n_TauPos_ENuNu_Phot",   "return int(ind_taupos_ENuNu_Phot.size() )" )
                .Define("n_TauPos_PiNu",         "return int(ind_taupos_PiNu.size() )"       )
                .Define("n_TauPos_PiNu_Phot",    "return int(ind_taupos_PiNu_Phot.size() )"  )
                .Define("n_TauPos_KNu",          "return int(ind_taupos_KNu.size() )"        )
                .Define("n_TauPos_KNu_Phot",     "return int(ind_taupos_KNu_Phot.size() )"   )
                .Define("n_TauPos_PiK0Nu",       "return int(ind_taupos_PiK0Nu.size() )"     )
                .Define("n_TauPos_PiK0Nu_Phot",  "return int(ind_taupos_PiK0Nu_Phot.size() )")
                .Define("n_TauPos_KK0Nu",        "return int(ind_taupos_KK0Nu.size() )"      )
                .Define("n_TauPos_KK0Nu_Phot",   "return int(ind_taupos_KK0Nu_Phot.size() )" )
                .Define("n_TauPos_3PiNu",        "return int(ind_taupos_3PiNu.size() )"      )
                .Define("n_TauPos_3PiNu_Phot",   "return int(ind_taupos_3PiNu_Phot.size() )" )
                .Define("n_TauPos_PiKKNu",       "return int(ind_taupos_PiKKNu.size() )"     )
                .Define("n_TauPos_PiKKNu_Phot",  "return int(ind_taupos_PiKKNu_Phot.size() )")

                #all final state gen neutrinos and anti-neutrinos
                .Define("GenElectronNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(12, true)(Particle)")
                .Define("GenMuonNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(14, true)(Particle)")
                .Define("GenTauNeutrino_PID", "FCCAnalyses::MCParticle::sel_pdgID(16, true)(Particle)")
                .Define("GenNeutrino1_PID", "FCCAnalyses::MCParticle::mergeParticles(GenElectronNeutrino_PID, GenMuonNeutrino_PID)") #merge all the neutrino flavors into one class, takes two arguments
                .Define("GenNeutrino_PID", "FCCAnalyses::MCParticle::mergeParticles(GenNeutrino1_PID, GenTauNeutrino_PID)") 
                .Define("FSGenNeutrino", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenNeutrino_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenNeutrino", "FCCAnalyses::MCParticle::get_n(FSGenNeutrino)")
                .Define("FSGenNeutrino_e", "FCCAnalyses::MCParticle::get_e(FSGenNeutrino)")
                .Define("FSGenNeutrino_p", "FCCAnalyses::MCParticle::get_p(FSGenNeutrino)")
                .Define("FSGenNeutrino_pt", "FCCAnalyses::MCParticle::get_pt(FSGenNeutrino)")
                .Define("FSGenNeutrino_px", "FCCAnalyses::MCParticle::get_px(FSGenNeutrino)")
                .Define("FSGenNeutrino_py", "FCCAnalyses::MCParticle::get_py(FSGenNeutrino)")
                .Define("FSGenNeutrino_pz", "FCCAnalyses::MCParticle::get_pz(FSGenNeutrino)")
                .Define("FSGenNeutrino_y", "FCCAnalyses::MCParticle::get_y(FSGenNeutrino)")
                .Define("FSGenNeutrino_eta", "FCCAnalyses::MCParticle::get_eta(FSGenNeutrino)")
                .Define("FSGenNeutrino_theta", "FCCAnalyses::MCParticle::get_theta(FSGenNeutrino)")
                .Define("FSGenNeutrino_phi", "FCCAnalyses::MCParticle::get_phi(FSGenNeutrino)")
                .Define("FSGenNeutrino_charge", "FCCAnalyses::MCParticle::get_charge(FSGenNeutrino)")
                #.Define("FSGenNeutrino_parentPDG", "FCCAnalyses::MCParticle::get_parentid(FSGenNeutrino,Particle,Particle0)")
                
                #all final state gen photons
                .Define("GenPhoton_PID", "FCCAnalyses::MCParticle::sel_pdgID(22, false)(Particle)")
                .Define("FSGenPhoton", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenPhoton_PID)") #gen status==1 means final state particle (FS)
                .Define("n_FSGenPhoton", "FCCAnalyses::MCParticle::get_n(FSGenPhoton)")
                .Define("FSGenPhoton_e", "FCCAnalyses::MCParticle::get_e(FSGenPhoton)")
                .Define("FSGenPhoton_p", "FCCAnalyses::MCParticle::get_p(FSGenPhoton)")
                .Define("FSGenPhoton_pt", "FCCAnalyses::MCParticle::get_pt(FSGenPhoton)")
                .Define("FSGenPhoton_px", "FCCAnalyses::MCParticle::get_px(FSGenPhoton)")
                .Define("FSGenPhoton_py", "FCCAnalyses::MCParticle::get_py(FSGenPhoton)")
                .Define("FSGenPhoton_pz", "FCCAnalyses::MCParticle::get_pz(FSGenPhoton)")
                .Define("FSGenPhoton_y", "FCCAnalyses::MCParticle::get_y(FSGenPhoton)")
                .Define("FSGenPhoton_eta", "FCCAnalyses::MCParticle::get_eta(FSGenPhoton)")
                .Define("FSGenPhoton_theta", "FCCAnalyses::MCParticle::get_theta(FSGenPhoton)")
                .Define("FSGenPhoton_phi", "FCCAnalyses::MCParticle::get_phi(FSGenPhoton)")
                .Define("FSGenPhoton_charge", "FCCAnalyses::MCParticle::get_charge(FSGenPhoton)")
                #.Define("FSGenPhoton_parentPDG", "FCCAnalyses::MCParticle::get_parentid(FSGenPhoton,Particle,Particle0)")

                .Define("GenZ",   "FCCAnalyses::MCParticle::sel_pdgID(23, true)(Particle)")
                .Define("n_GenZ",   "FCCAnalyses::MCParticle::get_n(GenZ)")
                .Define("GenZ_e", "FCCAnalyses::MCParticle::get_e(GenZ)")
                .Define("GenZ_p", "FCCAnalyses::MCParticle::get_p(GenZ)")
                .Define("GenZ_pt", "FCCAnalyses::MCParticle::get_pt(GenZ)")
                .Define("GenZ_px", "FCCAnalyses::MCParticle::get_px(GenZ)")
                .Define("GenZ_py", "FCCAnalyses::MCParticle::get_py(GenZ)")
                .Define("GenZ_pz", "FCCAnalyses::MCParticle::get_pz(GenZ)")
                .Define("GenZ_y", "FCCAnalyses::MCParticle::get_y(GenZ)")
                .Define("GenZ_mass",  "FCCAnalyses::MCParticle::get_mass(GenZ)")
                .Define("GenZ_eta", "FCCAnalyses::MCParticle::get_eta(GenZ)")
                .Define("GenZ_theta", "FCCAnalyses::MCParticle::get_theta(GenZ)")
                .Define("GenZ_phi", "FCCAnalyses::MCParticle::get_phi(GenZ)")
                .Define("GenZ_charge", "FCCAnalyses::MCParticle::get_charge(GenZ)")

                .Define("GenW",   "FCCAnalyses::MCParticle::sel_pdgID(24, true)(Particle)")
                .Define("n_GenW",   "FCCAnalyses::MCParticle::get_n(GenW)")

                .Define("GenHiggs",   "FCCAnalyses::MCParticle::sel_pdgID(25, true)(Particle)")
                .Define("n_GenHiggs",   "FCCAnalyses::MCParticle::get_n(GenHiggs)")
                .Define("GenHiggs_e", "FCCAnalyses::MCParticle::get_e(GenHiggs)")
                .Define("GenHiggs_p", "FCCAnalyses::MCParticle::get_p(GenHiggs)")
                .Define("GenHiggs_pt", "FCCAnalyses::MCParticle::get_pt(GenHiggs)")
                .Define("GenHiggs_px", "FCCAnalyses::MCParticle::get_px(GenHiggs)")
                .Define("GenHiggs_py", "FCCAnalyses::MCParticle::get_py(GenHiggs)")
                .Define("GenHiggs_pz", "FCCAnalyses::MCParticle::get_pz(GenHiggs)")
                .Define("GenHiggs_y", "FCCAnalyses::MCParticle::get_y(GenHiggs)")
                .Define("GenHiggs_mass",  "FCCAnalyses::MCParticle::get_mass(GenHiggs)")
                .Define("GenHiggs_eta", "FCCAnalyses::MCParticle::get_eta(GenHiggs)")
                .Define("GenHiggs_theta", "FCCAnalyses::MCParticle::get_theta(GenHiggs)")
                .Define("GenHiggs_phi", "FCCAnalyses::MCParticle::get_phi(GenHiggs)")
                .Define("GenHiggs_charge", "FCCAnalyses::MCParticle::get_charge(GenHiggs)")
                
                ##################
                # Reco particles #
                ##################

                #simple mc to reco association to get pid, only work on the whole classes, not subsets
                .Define("RecoMC_PID", "ReconstructedParticle2MC::getRP2MC_pdg(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle)")
                
                #ELECTRONS 
                .Alias("Electron0", "Electron#0.index")
                .Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
                .Define("n_RecoElectrons",  "ReconstructedParticle::get_n(RecoElectrons)") #count how many electrons are in the event in total
                .Define("RecoElectron_e",      "ReconstructedParticle::get_e(RecoElectrons)")
                .Define("RecoElectron_p",      "ReconstructedParticle::get_p(RecoElectrons)")
                .Define("RecoElectron_pt",      "ReconstructedParticle::get_pt(RecoElectrons)")
                .Define("RecoElectron_px",      "ReconstructedParticle::get_px(RecoElectrons)")
                .Define("RecoElectron_py",      "ReconstructedParticle::get_py(RecoElectrons)")
                .Define("RecoElectron_pz",      "ReconstructedParticle::get_pz(RecoElectrons)")
                .Define("RecoElectron_y",     "ReconstructedParticle::get_y(RecoElectrons)")
                .Define("RecoElectron_eta",     "ReconstructedParticle::get_eta(RecoElectrons)") #pseudorapidity eta
                .Define("RecoElectron_theta",   "ReconstructedParticle::get_theta(RecoElectrons)")
                .Define("RecoElectron_phi",     "ReconstructedParticle::get_phi(RecoElectrons)") #polar angle in the transverse plane phi
                .Define("RecoElectron_charge",  "ReconstructedParticle::get_charge(RecoElectrons)")
                .Define("RecoElectron_mass",     "ReconstructedParticle::get_mass(RecoElectrons)")
                .Define("RecoElectronTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") #significance
                .Define("RecoElectronTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoElectronTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")

                .Define("RecoElectrons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoElectrons)")
                .Define("RecoElectrons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoElectrons_hard, ReconstructedParticles)")
                .Define("RecoElectrons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoElectrons_hard, RecoElectrons_iso)")

                .Define("n_RecoElectrons_sel",  "ReconstructedParticle::get_n(RecoElectrons_sel)") 
                .Define("RecoElectron_sel_e",      "ReconstructedParticle::get_e(RecoElectrons_sel)")
                .Define("RecoElectron_sel_p",      "ReconstructedParticle::get_p(RecoElectrons_sel)")
                .Define("RecoElectron_sel_pt",      "ReconstructedParticle::get_pt(RecoElectrons_sel)")
                .Define("RecoElectron_sel_px",      "ReconstructedParticle::get_px(RecoElectrons_sel)")
                .Define("RecoElectron_sel_py",      "ReconstructedParticle::get_py(RecoElectrons_sel)")
                .Define("RecoElectron_sel_pz",      "ReconstructedParticle::get_pz(RecoElectrons_sel)")
                .Define("RecoElectron_sel_y",      "ReconstructedParticle::get_y(RecoElectrons_sel)")
                .Define("RecoElectron_sel_eta",     "ReconstructedParticle::get_eta(RecoElectrons_sel)") #pseudorapidity eta
                .Define("RecoElectron_sel_theta",   "ReconstructedParticle::get_theta(RecoElectrons_sel)")
                .Define("RecoElectron_sel_phi",     "ReconstructedParticle::get_phi(RecoElectrons_sel)") #polar angle in the transverse plane phi
                .Define("RecoElectron_sel_charge",  "ReconstructedParticle::get_charge(RecoElectrons_sel)")
                .Define("RecoElectron_sel_mass",     "ReconstructedParticle::get_mass(RecoElectrons_sel)")
                .Define("RecoElectronTrack_sel_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons_sel,EFlowTrack_1))")
                .Define("RecoElectronTrack_sel_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons_sel,EFlowTrack_1))")
                .Define("RecoElectronTrack_sel_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons_sel,EFlowTrack_1))") #significance
                .Define("RecoElectronTrack_sel_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons_sel,EFlowTrack_1))")
                .Define("RecoElectronTrack_sel_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons_sel,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoElectronTrack_sel_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons_sel,EFlowTrack_1)")

                # MUONS
                .Alias("Muon0", "Muon#0.index")
                .Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
                .Define("n_RecoMuons",  "ReconstructedParticle::get_n(RecoMuons)") #count how many muons are in the event in total
                .Define("RecoMuon_e",      "ReconstructedParticle::get_e(RecoMuons)")
                .Define("RecoMuon_p",      "ReconstructedParticle::get_p(RecoMuons)")
                .Define("RecoMuon_pt",      "ReconstructedParticle::get_pt(RecoMuons)")
                .Define("RecoMuon_px",      "ReconstructedParticle::get_px(RecoMuons)")
                .Define("RecoMuon_py",      "ReconstructedParticle::get_py(RecoMuons)")
                .Define("RecoMuon_pz",      "ReconstructedParticle::get_pz(RecoMuons)")
                .Define("RecoMuon_y",     "ReconstructedParticle::get_y(RecoMuons)")
                .Define("RecoMuon_eta",     "ReconstructedParticle::get_eta(RecoMuons)") #pseudorapidity eta
                .Define("RecoMuon_theta",   "ReconstructedParticle::get_theta(RecoMuons)")
                .Define("RecoMuon_phi",     "ReconstructedParticle::get_phi(RecoMuons)") #polar angle in the transverse plane phi
                .Define("RecoMuon_charge",  "ReconstructedParticle::get_charge(RecoMuons)")
                .Define("RecoMuon_mass",     "ReconstructedParticle::get_mass(RecoMuons)")
                .Define("RecoMuonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack_1))") #significance
                .Define("RecoMuonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoMuonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack_1)")

                .Define("RecoMuons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoMuons)")
                .Define("RecoMuons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoMuons_hard, ReconstructedParticles)")
                .Define("RecoMuons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoMuons_hard, RecoMuons_iso)")
                
                .Define("n_RecoMuons_sel",  "ReconstructedParticle::get_n(RecoMuons_sel)") 
                .Define("RecoMuon_sel_e",      "ReconstructedParticle::get_e(RecoMuons_sel)")
                .Define("RecoMuon_sel_p",      "ReconstructedParticle::get_p(RecoMuons_sel)")
                .Define("RecoMuon_sel_pt",      "ReconstructedParticle::get_pt(RecoMuons_sel)")
                .Define("RecoMuon_sel_px",      "ReconstructedParticle::get_px(RecoMuons_sel)")
                .Define("RecoMuon_sel_py",      "ReconstructedParticle::get_py(RecoMuons_sel)")
                .Define("RecoMuon_sel_pz",      "ReconstructedParticle::get_pz(RecoMuons_sel)")
                .Define("RecoMuon_sel_y",      "ReconstructedParticle::get_y(RecoMuons_sel)")
                .Define("RecoMuon_sel_eta",     "ReconstructedParticle::get_eta(RecoMuons_sel)") #pseudorapidity eta
                .Define("RecoMuon_sel_theta",   "ReconstructedParticle::get_theta(RecoMuons_sel)")
                .Define("RecoMuon_sel_phi",     "ReconstructedParticle::get_phi(RecoMuons_sel)") #polar angle in the transverse plane phi
                .Define("RecoMuon_sel_charge",  "ReconstructedParticle::get_charge(RecoMuons_sel)")
                .Define("RecoMuon_sel_mass",     "ReconstructedParticle::get_mass(RecoMuons_sel)")
                .Define("RecoMuonTrack_sel_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons_sel,EFlowTrack_1))")
                .Define("RecoMuonTrack_sel_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons_sel,EFlowTrack_1))")
                .Define("RecoMuonTrack_sel_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons_sel,EFlowTrack_1))") #significance
                .Define("RecoMuonTrack_sel_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons_sel,EFlowTrack_1))")
                .Define("RecoMuonTrack_sel_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons_sel,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoMuonTrack_sel_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons_sel,EFlowTrack_1)")

                # LEPTONS
                .Define("RecoLeptons", "ReconstructedParticle::merge(RecoElectrons, RecoMuons)")
                .Define("n_RecoLeptons",  "ReconstructedParticle::get_n(RecoLeptons)") 
                .Define("RecoLepton_e",      "ReconstructedParticle::get_e(RecoLeptons)")
                .Define("RecoLepton_p",      "ReconstructedParticle::get_p(RecoLeptons)")
                .Define("RecoLepton_pt",      "ReconstructedParticle::get_pt(RecoLeptons)")
                .Define("RecoLepton_px",      "ReconstructedParticle::get_px(RecoLeptons)")
                .Define("RecoLepton_py",      "ReconstructedParticle::get_py(RecoLeptons)")
                .Define("RecoLepton_pz",      "ReconstructedParticle::get_pz(RecoLeptons)")
                .Define("RecoLepton_y",      "ReconstructedParticle::get_y(RecoLeptons)")
                .Define("RecoLepton_eta",     "ReconstructedParticle::get_eta(RecoLeptons)") #pseudorapidity eta
                .Define("RecoLepton_theta",   "ReconstructedParticle::get_theta(RecoLeptons)")
                .Define("RecoLepton_phi",     "ReconstructedParticle::get_phi(RecoLeptons)") #polar angle in the transverse plane phi
                .Define("RecoLepton_charge",  "ReconstructedParticle::get_charge(RecoLeptons)")
                .Define("RecoLepton_mass",     "ReconstructedParticle::get_mass(RecoLeptons)")
                .Define("RecoLeptonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons,EFlowTrack_1))")
                .Define("RecoLeptonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons,EFlowTrack_1))")
                .Define("RecoLeptonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons,EFlowTrack_1))") #significance
                .Define("RecoLeptonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons,EFlowTrack_1))")
                .Define("RecoLeptonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoLeptons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoLeptonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoLeptons,EFlowTrack_1)")

                .Define("RecoLeptons_sel", "ReconstructedParticle::merge(RecoElectrons_sel, RecoMuons_sel)")
                .Define("n_RecoLeptons_sel",  "ReconstructedParticle::get_n(RecoLeptons_sel)") 
                .Define("RecoLepton_sel_e",      "ReconstructedParticle::get_e(RecoLeptons_sel)")
                .Define("RecoLepton_sel_p",      "ReconstructedParticle::get_p(RecoLeptons_sel)")
                .Define("RecoLepton_sel_pt",      "ReconstructedParticle::get_pt(RecoLeptons_sel)")
                .Define("RecoLepton_sel_px",      "ReconstructedParticle::get_px(RecoLeptons_sel)")
                .Define("RecoLepton_sel_py",      "ReconstructedParticle::get_py(RecoLeptons_sel)")
                .Define("RecoLepton_sel_pz",      "ReconstructedParticle::get_pz(RecoLeptons_sel)")
                .Define("RecoLepton_sel_y",      "ReconstructedParticle::get_y(RecoLeptons_sel)")
                .Define("RecoLepton_sel_eta",     "ReconstructedParticle::get_eta(RecoLeptons_sel)") #pseudorapidity eta
                .Define("RecoLepton_sel_theta",   "ReconstructedParticle::get_theta(RecoLeptons_sel)")
                .Define("RecoLepton_sel_phi",     "ReconstructedParticle::get_phi(RecoLeptons_sel)") #polar angle in the transverse plane phi
                .Define("RecoLepton_sel_charge",  "ReconstructedParticle::get_charge(RecoLeptons_sel)")
                .Define("RecoLepton_sel_mass",     "ReconstructedParticle::get_mass(RecoLeptons_sel)")
                .Define("RecoLeptonTrack_sel_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons_sel,EFlowTrack_1))")
                .Define("RecoLeptonTrack_sel_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons_sel,EFlowTrack_1))")
                .Define("RecoLeptonTrack_sel_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons_sel,EFlowTrack_1))") #significance
                .Define("RecoLeptonTrack_sel_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons_sel,EFlowTrack_1))")
                .Define("RecoLeptonTrack_sel_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoLeptons_sel,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoLeptonTrack_sel_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoLeptons_sel,EFlowTrack_1)")

                #PHOTONS
                .Alias("Photon0", "Photon#0.index") 
                .Define("RecoPhotons",  "ReconstructedParticle::get(Photon0, ReconstructedParticles)")
                .Define("n_RecoPhotons",  "ReconstructedParticle::get_n(RecoPhotons)") #count how many photons are in the event in total
                .Define("RecoPhoton_e",      "ReconstructedParticle::get_e(RecoPhotons)")
                .Define("RecoPhoton_p",      "ReconstructedParticle::get_p(RecoPhotons)")
                .Define("RecoPhoton_pt",      "ReconstructedParticle::get_pt(RecoPhotons)")
                .Define("RecoPhoton_px",      "ReconstructedParticle::get_px(RecoPhotons)")
                .Define("RecoPhoton_py",      "ReconstructedParticle::get_py(RecoPhotons)")
                .Define("RecoPhoton_pz",      "ReconstructedParticle::get_pz(RecoPhotons)")
		        .Define("RecoPhoton_y",     "ReconstructedParticle::get_y(RecoPhotons)") 
		        .Define("RecoPhoton_eta",     "ReconstructedParticle::get_eta(RecoPhotons)") #pseudorapidity eta
                .Define("RecoPhoton_theta",   "ReconstructedParticle::get_theta(RecoPhotons)")
		        .Define("RecoPhoton_phi",     "ReconstructedParticle::get_phi(RecoPhotons)") #polar angle in the transverse plane phi
                .Define("RecoPhoton_charge",  "ReconstructedParticle::get_charge(RecoPhotons)")

                # different definition of missing energy from fccanalysis classes instead of edm4hep
                .Define("RecoEmiss", "FCCAnalyses::ZHfunctions::missingEnergy(240, ReconstructedParticles)") #ecm 
                .Define("RecoEmiss_px",  "RecoEmiss[0].momentum.x")
                .Define("RecoEmiss_py",  "RecoEmiss[0].momentum.y")
                .Define("RecoEmiss_pz",  "RecoEmiss[0].momentum.z")
                .Define("RecoEmiss_pt",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py)")
                .Define("RecoEmiss_p",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py + RecoEmiss_pz*RecoEmiss_pz)")
                .Define("RecoEmiss_e",   "RecoEmiss[0].energy")

                # reconstructed tracks
                .Define("n_RecoTracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")
                .Define("RecoVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 0, EFlowTrack_1)" ) ### reconstructing a vertex withour any request n=0 ###
                .Define("RecoVertex",  "VertexingUtils::get_VertexData( RecoVertexObject )")

                .Define("PrimaryTracks",  "VertexFitterSimple::get_PrimaryTracks( EFlowTrack_1, true, 4.5, 20e-3, 300, 0., 0., 0.)") 
                .Define("n_PrimaryTracks",  "ReconstructedParticle2Track::getTK_n( PrimaryTracks )")
                .Define("PrimaryVertexObject", "VertexFitterSimple::VertexFitter_Tk(1, PrimaryTracks, true, 4.5, 20e-3, 300)")
                .Define("PrimaryVertex",  "VertexingUtils::get_VertexData( PrimaryVertexObject )")
                .Define("PrimaryVertex_xyz","return sqrt(PrimaryVertex.position.x*PrimaryVertex.position.x + PrimaryVertex.position.y*PrimaryVertex.position.y + PrimaryVertex.position.z*PrimaryVertex.position.z);")
                .Define("PrimaryVertes_xy","return sqrt(PrimaryVertex.position.x*PrimaryVertex.position.x + PrimaryVertex.position.y*PrimaryVertex.position.y);")
                
                .Define("SecondaryTracks",   "VertexFitterSimple::get_NonPrimaryTracks( EFlowTrack_1, PrimaryTracks )")
                .Define("n_SecondaryTracks",  "ReconstructedParticle2Track::getTK_n( SecondaryTracks )" )
                .Define("SecondaryVertexObject", "VertexFitterSimple::VertexFitter_Tk(2, SecondaryTracks)")
                .Define("SecondaryVertex",  "VertexingUtils::get_VertexData( SecondaryVertexObject )")
                .Define("SecondaryVertex_xyz","return sqrt(SecondaryVertex.position.x*SecondaryVertex.position.x + SecondaryVertex.position.y*SecondaryVertex.position.y + SecondaryVertex.position.z*SecondaryVertex.position.z);")
                .Define("SecondaryVertes_xy","return sqrt(SecondaryVertex.position.x*SecondaryVertex.position.x + SecondaryVertex.position.y*SecondaryVertex.position.y);")

                # MC vertex association
                #.Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(3)( Particle )" )
                .Define("MCVertexObject", "myUtils::get_MCVertexObject(Particle, Particle0)")
                .Define("VertexObject", "myUtils::get_VertexObject(MCVertexObject, ReconstructedParticles, EFlowTrack_1, MCRecoAssociations0, MCRecoAssociations1)")
                .Define("RecoPartPID" ,"myUtils::PID(ReconstructedParticles, MCRecoAssociations0, MCRecoAssociations1, Particle)")
                .Define("RecoPartPIDAtVertex" ,"myUtils::get_RP_atVertex(RecoPartPID, VertexObject)")

                # JETS, reclustered from the reconstructed particles, never use the class in the samples
                ### https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/JetClustering.h ###

                .Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,RecoMuons_sel)")
                .Define("ReconstructedParticlesNoLeps",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons,RecoElectrons_sel)")
            
                .Define("RP_px_sel",          "ReconstructedParticle::get_px(ReconstructedParticlesNoLeps)")
                .Define("RP_py_sel",          "ReconstructedParticle::get_py(ReconstructedParticlesNoLeps)")
                .Define("RP_pz_sel",          "ReconstructedParticle::get_pz(ReconstructedParticlesNoLeps)")
                .Define("RP_e_sel",           "ReconstructedParticle::get_e(ReconstructedParticlesNoLeps)")
                .Define("RP_m_sel",           "ReconstructedParticle::get_mass(ReconstructedParticlesNoLeps)")
                .Define("RP_q_sel",           "ReconstructedParticle::get_charge(ReconstructedParticlesNoLeps)")
                #.Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
                # build pseudo jets with the RP, using the interface that takes px,py,pz,E
                .Define("pseudo_jets_sel",  "JetClusteringUtils::set_pseudoJets(RP_px_sel, RP_py_sel, RP_pz_sel, RP_e_sel)" )

                #R5 inclusive
                .Define("FCCAnalysesJets_R5", "JetClustering::clustering_ee_genkt(0.5, 0, 2., 0, 1, -1)(pseudo_jets_sel)")
                .Define("Jets_R5",  "JetClusteringUtils::get_pseudoJets( FCCAnalysesJets_R5 )") 
                .Define("Jet_GetConstituents_R5","JetClusteringUtils::get_constituents(FCCAnalysesJets_R5)")
                .Define("Jets_Constituents_R5", "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticlesNoLeps, Jet_GetConstituents_R5)") #build jet constituents lists for tau reconstruction

		        .Define("Jets_R5_e",      "JetClusteringUtils::get_e(Jets_R5)")
                .Define("Jets_R5_p",      "JetClusteringUtils::get_p(Jets_R5)") #momentum p
                .Define("Jets_R5_pt",      "JetClusteringUtils::get_pt(Jets_R5)") #transverse momentum pt
                .Define("Jets_R5_px",      "JetClusteringUtils::get_px(Jets_R5)")
                .Define("Jets_R5_py",      "JetClusteringUtils::get_py(Jets_R5)")
                .Define("Jets_R5_pz",      "JetClusteringUtils::get_pz(Jets_R5)")
		        .Define("Jets_R5_eta",     "JetClusteringUtils::get_eta(Jets_R5)") #pseudorapidity eta
                .Define("Jets_R5_theta",   "JetClusteringUtils::get_theta(Jets_R5)")
		        .Define("Jets_R5_phi",     "JetClusteringUtils::get_phi(Jets_R5)") #polar angle in the transverse plane phi
                .Define("Jets_R5_mass",      "JetClusteringUtils::get_m(Jets_R5)")
                .Define("n_Jets_R5", "Jets_R5_e.size()")

                .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
                .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
                .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
                .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
                .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
                .Define("RP_q",           "ReconstructedParticle::get_charge(ReconstructedParticles)")
                #.Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
                # build pseudo jets with the RP, using the interface that takes px,py,pz,E
                .Define("pseudo_jets",  "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)" )

                .Define("FCCAnalysesJets_excl4", "JetClustering::clustering_ee_kt(2, 4, 1, 0)(pseudo_jets)")
                .Define("Jets_excl4",           "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_excl4)")
                .Define("Jet_Constituents_recluster","JetClusteringUtils::get_constituents(FCCAnalysesJets_excl4)")
                .Define("Jets_Constituents", "JetConstituentsUtils::build_constituents_cluster(ReconstructedParticles, Jet_Constituents_recluster)") #build jet constituents lists

                .Define("Jets_excl4_e",      "JetClusteringUtils::get_e(Jets_excl4)")
                .Define("Jets_excl4_p",      "JetClusteringUtils::get_p(Jets_excl4)") #momentum p
                .Define("Jets_excl4_pt",      "JetClusteringUtils::get_pt(Jets_excl4)") #transverse momentum pt
                .Define("Jets_excl4_px",      "JetClusteringUtils::get_px(Jets_excl4)")
                .Define("Jets_excl4_py",      "JetClusteringUtils::get_py(Jets_excl4)")
                .Define("Jets_excl4_pz",      "JetClusteringUtils::get_pz(Jets_excl4)")
		        .Define("Jets_excl4_eta",     "JetClusteringUtils::get_eta(Jets_excl4)") #pseudorapidity eta
                .Define("Jets_excl4_theta",   "JetClusteringUtils::get_theta(Jets_excl4)")
		        .Define("Jets_excl4_phi",     "JetClusteringUtils::get_phi(Jets_excl4)") #polar angle in the transverse plane phi
                .Define("Jets_excl4_mass",      "JetClusteringUtils::get_m(Jets_excl4)")
                .Define("n_Jets_excl4", "Jets_excl4_e.size()")

                ### reconstruction of hadronic taus from jets
                .Define("TauFromJet_R5", "FCCAnalyses::ZHfunctions::findTauInJet(Jets_Constituents_R5)") 
                .Define("TauFromJet_R5_type_sel","ReconstructedParticle::get_type(TauFromJet_R5)")
                .Define("TauFromJet_R5_tau", "TauFromJet_R5[TauFromJet_R5_type_sel>=0]") 
                .Define("TauFromJet_R5_p","ReconstructedParticle::get_p(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_pt","ReconstructedParticle::get_pt(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_px","ReconstructedParticle::get_px(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_py","ReconstructedParticle::get_py(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_pz","ReconstructedParticle::get_pz(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_theta","ReconstructedParticle::get_theta(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_phi","ReconstructedParticle::get_phi(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_e","ReconstructedParticle::get_e(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_charge","ReconstructedParticle::get_charge(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_type","ReconstructedParticle::get_type(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_mass","ReconstructedParticle::get_mass(TauFromJet_R5_tau)")
                .Define("n_TauFromJet_R5","(UInt_t)TauFromJet_R5_pt.size()")

                .Define("TauFromJet", "FCCAnalyses::ZHfunctions::findTauInJet(Jets_Constituents)") 
                .Define("TauFromJet_type_sel","ReconstructedParticle::get_type(TauFromJet)")
                .Define("TauFromJet_tau", "TauFromJet[TauFromJet_type_sel>=0]") 
                .Define("TauFromJet_p","ReconstructedParticle::get_p(TauFromJet_tau)")
                .Define("TauFromJet_pt","ReconstructedParticle::get_pt(TauFromJet_tau)")
                .Define("TauFromJet_px","ReconstructedParticle::get_px(TauFromJet_tau)")
                .Define("TauFromJet_py","ReconstructedParticle::get_py(TauFromJet_tau)")
                .Define("TauFromJet_pz","ReconstructedParticle::get_pz(TauFromJet_tau)")
                .Define("TauFromJet_theta","ReconstructedParticle::get_theta(TauFromJet_tau)")
                .Define("TauFromJet_phi","ReconstructedParticle::get_phi(TauFromJet_tau)")
                .Define("TauFromJet_e","ReconstructedParticle::get_e(TauFromJet_tau)")
                .Define("TauFromJet_charge","ReconstructedParticle::get_charge(TauFromJet_tau)")
                .Define("TauFromJet_type","ReconstructedParticle::get_type(TauFromJet_tau)")
                .Define("TauFromJet_mass","ReconstructedParticle::get_mass(TauFromJet_tau)")
                .Define("n_TauFromJet","(UInt_t)TauFromJet_pt.size()")

                .Define("Jets_R5_sel_e",      "Jets_R5_e[TauFromJet_R5_type_sel<0]")
                .Define("Jets_R5_sel_p",      "Jets_R5_p[TauFromJet_R5_type_sel<0]")
                .Define("Jets_R5_sel_pt",      "Jets_R5_pt[TauFromJet_R5_type_sel<0]")
                .Define("Jets_R5_sel_px",      "Jets_R5_px[TauFromJet_R5_type_sel<0]")
                .Define("Jets_R5_sel_py",      "Jets_R5_py[TauFromJet_R5_type_sel<0]")
                .Define("Jets_R5_sel_pz",      "Jets_R5_pz[TauFromJet_R5_type_sel<0]")
		        .Define("Jets_R5_sel_eta",     "Jets_R5_eta[TauFromJet_R5_type_sel<0]")
                .Define("Jets_R5_sel_theta",   "Jets_R5_theta[TauFromJet_R5_type_sel<0]")
		        .Define("Jets_R5_sel_phi",     "Jets_R5_phi[TauFromJet_R5_type_sel<0]")
                .Define("Jets_R5_sel_mass",      "Jets_R5_mass[TauFromJet_R5_type_sel<0]")
                .Define("n_Jets_R5_sel", "Jets_R5_sel_e.size()")
               
        )
        return df2
    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
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

            "n_GenZ",
            "GenZ_e",
            "GenZ_p", 
            "GenZ_pt", 
            "GenZ_px", 
            "GenZ_py", 
            "GenZ_pz", 
            "GenZ_y", 
            "GenZ_mass",
            "GenZ_eta", 
            "GenZ_theta", 
            "GenZ_phi", 
            "GenZ_charge", 

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

            "RecoEmiss_px",
            "RecoEmiss_py",
            "RecoEmiss_pz",
            "RecoEmiss_pt",
            "RecoEmiss_p",
            "RecoEmiss_e",

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
            "n_Jets_excl4", 
 
            "TauFromJet_R5_p",
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

            "TauFromJet_p",
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
            "n_Jets_R5_sel", 

        #for testing
            #"TauFromJet_R5_type_sel",
        ]

        return branchList