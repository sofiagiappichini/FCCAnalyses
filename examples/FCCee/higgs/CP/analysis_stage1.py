import os, copy # tagging
import ROOT

#Mandatory: List of processes
processList = {
    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Huu_ecm240': {'chunks':10},
    #'wzp6_ee_nunuH_Hdd_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_Hmumu_ecm240': {'chunks':10},
    'wzp6_ee_nunuH_HWW_ecm240': {'chunks':10},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "/eos/user/s/sgiappic/HiggsCP/stage1_24_06_25/"

### necessary to run on HTCondor ###c
eosType = "eosuser"

#Optional: ncpus, default is 4
nCPUS = 10

#Optional running on HTCondor, default is False
runBatch = True

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "tomorrow"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_FCC.local_gen"

### tagging
## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc_v1"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = (
    "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
)
local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)


weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
    InclusiveJetClusteringHelper,
)

jetFlavourHelper = None
jetClusteringHelper = None

jetClusteringHelper_kt2   = None
jetClusteringHelper_R5   = None
jetFlavourHelper_kt2   = None
jetFlavourHelper_R5   = None

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
                .Define("FSGenMuon_eta", "FCCAnalyses::MCParticle::get_eta(FSGenMuon)")
                .Define("FSGenMuon_theta", "FCCAnalyses::MCParticle::get_theta(FSGenMuon)")
                .Define("FSGenMuon_phi", "FCCAnalyses::MCParticle::get_phi(FSGenMuon)")
                .Define("FSGenMuon_charge", "FCCAnalyses::MCParticle::get_charge(FSGenMuon)")
                .Define("FSGenMuon_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenMuon)")
                .Define("FSGenMuon_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(FSGenMuon,Particle,Particle0)")
                .Define("FSGenMuon_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( FSGenMuon )")
                .Define("FSGenMuon_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( FSGenMuon )")
                .Define("FSGenMuon_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( FSGenMuon )")

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
                .Define("FSGenPhoton_eta", "FCCAnalyses::MCParticle::get_eta(FSGenPhoton)")
                .Define("FSGenPhoton_theta", "FCCAnalyses::MCParticle::get_theta(FSGenPhoton)")
                .Define("FSGenPhoton_phi", "FCCAnalyses::MCParticle::get_phi(FSGenPhoton)")
                .Define("FSGenPhoton_charge", "FCCAnalyses::MCParticle::get_charge(FSGenPhoton)")
                #.Define("FSGenPhoton_parentPDG", "FCCAnalyses::MCParticle::get_parentid(FSGenPhoton,Particle,Particle0)")

                .Define("GenZ",   "FCCAnalyses::MCParticle::sel_pdgID(23, true)(Particle)")
                .Define("n_GenZ",   "FCCAnalyses::MCParticle::get_n(GenZ)")

                .Define("GenH",   "FCCAnalyses::MCParticle::sel_pdgID(25, true)(Particle)")
                .Define("n_GenH",   "FCCAnalyses::MCParticle::get_n(GenH)")
                
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
                .Define("RecoElectron_eta",     "ReconstructedParticle::get_eta(RecoElectrons)") #pseudorapidity eta
                .Define("RecoElectron_theta",   "ReconstructedParticle::get_theta(RecoElectrons)")
                .Define("RecoElectron_phi",     "ReconstructedParticle::get_phi(RecoElectrons)") #polar angle in the transverse plane phi
                .Define("RecoElectron_charge",  "ReconstructedParticle::get_charge(RecoElectrons)")
                .Define("RecoElectronTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") #significance
                .Define("RecoElectronTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
                .Define("RecoElectronTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoElectronTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")

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
                .Define("RecoMuon_eta",     "ReconstructedParticle::get_eta(RecoMuons)") #pseudorapidity eta
                .Define("RecoMuon_theta",   "ReconstructedParticle::get_theta(RecoMuons)")
                .Define("RecoMuon_phi",     "ReconstructedParticle::get_phi(RecoMuons)") #polar angle in the transverse plane phi
                .Define("RecoMuon_charge",  "ReconstructedParticle::get_charge(RecoMuons)")
                .Define("RecoMuonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack_1))") #significance
                .Define("RecoMuonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack_1))")
                .Define("RecoMuonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoMuonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack_1)")

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
		        .Define("RecoPhoton_eta",     "ReconstructedParticle::get_eta(RecoPhotons)") #pseudorapidity eta
                .Define("RecoPhoton_theta",   "ReconstructedParticle::get_theta(RecoPhotons)")
		        .Define("RecoPhoton_phi",     "ReconstructedParticle::get_phi(RecoPhotons)") #polar angle in the transverse plane phi
                .Define("RecoPhoton_charge",  "ReconstructedParticle::get_charge(RecoPhotons)")

                #EVENTWIDE VARIABLES: Access quantities that exist only once per event, such as the missing energy (despite the name, the MissingET collection contains the total missing energy)
                .Define("RecoMissingEnergy_e", "ReconstructedParticle::get_e(MissingET)")
                .Define("RecoMissingEnergy_p", "ReconstructedParticle::get_p(MissingET)")
                .Define("RecoMissingEnergy_pt", "ReconstructedParticle::get_pt(MissingET)")
                .Define("RecoMissingEnergy_px", "ReconstructedParticle::get_px(MissingET)") #x-component of RecoMissingEnergy
                .Define("RecoMissingEnergy_py", "ReconstructedParticle::get_py(MissingET)") #y-component of RecoMissingEnergy
                .Define("RecoMissingEnergy_pz", "ReconstructedParticle::get_pz(MissingET)") #z-component of RecoMissingEnergy
                .Define("RecoMissingEnergy_eta", "ReconstructedParticle::get_eta(MissingET)")
                .Define("RecoMissingEnergy_theta", "ReconstructedParticle::get_theta(MissingET)")
                .Define("RecoMissingEnergy_phi", "ReconstructedParticle::get_phi(MissingET)") #angle of RecoMissingEnergy

                # reconstructed tracks
                .Define("n_RecoTracks","ReconstructedParticle2Track::getTK_n(EFlowTrack_1)")
                .Define("RecoVertexObject",   "VertexFitterSimple::VertexFitter_Tk( 0, EFlowTrack_1)" ) ### reconstructing a vertex withour any request n=0 ###
                .Define("RecoVertex",  "VertexingUtils::get_VertexData( RecoVertexObject )")
                #.Define("n_RecoVertex",  "VertexingUtils::get_Nvertex(RecoVertex)")

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
                .Define("RP_px",          "ReconstructedParticle::get_px(ReconstructedParticles)")
                .Define("RP_py",          "ReconstructedParticle::get_py(ReconstructedParticles)")
                .Define("RP_pz",          "ReconstructedParticle::get_pz(ReconstructedParticles)")
                .Define("RP_e",           "ReconstructedParticle::get_e(ReconstructedParticles)")
                .Define("RP_m",           "ReconstructedParticle::get_mass(ReconstructedParticles)")
                .Define("RP_q",           "ReconstructedParticle::get_charge(ReconstructedParticles)")
                #.Define("pseudo_jets",    "JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
                # build pseudo jets with the RP, using the interface that takes px,py,pz,E
                .Define("pseudo_jets",  "JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)" )

                # Durham algo, exclusive clustering (first number 2) N_jets=0 (second number), E-scheme=0 (third and forth numbers)
                .Define( "FCCAnalysesJets_ee_kt",  "JetClustering::clustering_ee_kt(2, 0, 1, 0)(pseudo_jets)" )
                .Define("Jets_kt2",  "JetClusteringUtils::get_pseudoJets( FCCAnalysesJets_ee_kt )") 
		        .Define("Jets_kt2_e",      "JetClusteringUtils::get_e(Jets_kt2)")
                .Define("Jets_kt2_p",      "JetClusteringUtils::get_p(Jets_kt2)") #momentum p
                .Define("Jets_kt2_pt",      "JetClusteringUtils::get_pt(Jets_kt2)") #transverse momentum pt
                .Define("Jets_kt2_px",      "JetClusteringUtils::get_px(Jets_kt2)")
                .Define("Jets_kt2_py",      "JetClusteringUtils::get_py(Jets_kt2)")
                .Define("Jets_kt2_pz",      "JetClusteringUtils::get_pz(Jets_kt2)")
		        .Define("Jets_kt2_eta",     "JetClusteringUtils::get_eta(Jets_kt2)") #pseudorapidity eta
                .Define("Jets_kt2_theta",   "JetClusteringUtils::get_theta(Jets_kt2)")
		        .Define("Jets_kt2_phi",     "JetClusteringUtils::get_phi(Jets_kt2)") #polar angle in the transverse plane phi
                .Define("Jets_kt2_mass",      "JetClusteringUtils::get_m(Jets_kt2)")
                .Define("Jets_kt2_flavor",      "JetTaggingUtils::get_flavour(Jets_kt2, Particle)")
                .Define("n_Jets_kt2", "Jets_kt2_e.size()")

                # Inclusive anitkt algorithm, numbers are jet radius paramter, exclusive clustering, pt cut, pt ordering, recombination scheme
                .Define("FCCAnalysesJets_antikt5", "JetClustering::clustering_antikt(0.5, 0, 5., 0, 0)(pseudo_jets)")
                .Define("Jets_antikt5", "JetClusteringUtils::get_pseudoJets(FCCAnalysesJets_antikt5)")
                .Define("Jets_antikt5_e",      "JetClusteringUtils::get_e(Jets_antikt5)")
                .Define("Jets_antikt5_p",      "JetClusteringUtils::get_p(Jets_antikt5)") #momentum p
                .Define("Jets_antikt5_pt",      "JetClusteringUtils::get_pt(Jets_antikt5)") #transverse momentum pt
                .Define("Jets_antikt5_px",      "JetClusteringUtils::get_px(Jets_antikt5)")
                .Define("Jets_antikt5_py",      "JetClusteringUtils::get_py(Jets_antikt5)")
                .Define("Jets_antikt5_pz",      "JetClusteringUtils::get_pz(Jets_antikt5)")
		        .Define("Jets_antikt5_eta",     "JetClusteringUtils::get_eta(Jets_antikt5)") #pseudorapidity eta
                .Define("Jets_antikt5_theta",   "JetClusteringUtils::get_theta(Jets_antikt5)")
		        .Define("Jets_antikt5_phi",     "JetClusteringUtils::get_phi(Jets_antikt5)") #polar angle in the transverse plane phi
                .Define("Jets_antikt5_mass",      "JetClusteringUtils::get_m(Jets_antikt5)")
                .Define("Jets_antikt5_flavor",      "JetTaggingUtils::get_flavour(Jets_antikt5, Particle)")
                .Define("n_Jets_antikt5", "Jets_antikt5_e.size()")
               
        )

        ### tagging, inherited from lars to build the tau tagging alogirthm later on
        # cleaning out low momentum leptons
        df3 = (df2
               .Define("muons_15",     "FCCAnalyses::ReconstructedParticle::sel_p(15)(RecoMuons)")
               .Define("electrons_15", "FCCAnalyses::ReconstructedParticle::sel_p(15)(RecoElectrons)")
               .Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,muons_15)")
               .Define("ReconstructedParticlesNoLeps",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons,electrons_15)")
        )

        global jetClusteringHelper_kt2
        global jetClusteringHelper_R5
        global jetFlavourHelper_kt2
        global jetFlavourHelper_R5
        ## define jet and run clustering parameters
        ## name of collections in EDM root files
        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticles",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "EFlowTrack_1",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "EFlowTrack_2",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }
        collections_noleps = copy.deepcopy(collections)
        collections_noleps["PFParticles"] = "ReconstructedParticlesNoLeps"

        ## def __init__(self, coll, njets, tag="")
        jetClusteringHelper_kt2 = ExclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 2, "kt2",
        )
        jetClusteringHelper_R5  = InclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 0.5, 1, "R5",
        )
        df3 = jetClusteringHelper_kt2.define(df3)
        df3 = jetClusteringHelper_R5. define(df3)

        ## define jet flavour tagging parameters

        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt2.jets,
            jetClusteringHelper_kt2.constituents,
            "kt2",
        )
        jetFlavourHelper_R5 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_R5.jets,
            jetClusteringHelper_R5.constituents,
            "R5",
        )
        ## define observables for tagger
        df3 = jetFlavourHelper_kt2.define(df3)
        df3 = jetFlavourHelper_R5. define(df3)

        ## tagger inference
        df3 = jetFlavourHelper_kt2.inference(weaver_preproc, weaver_model, df3)
        df3 = jetFlavourHelper_R5. inference(weaver_preproc, weaver_model, df3)

        # is this needed?
        # no, this is just variables for output
        df3 = df3.Define(
            "jets_kt2_p4",
            "JetConstituentsUtils::compute_tlv_jets({})".format(
                jetClusteringHelper_kt2.jets
            ),
        )

        df3 = (df3
            .Define("jet_kt2_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt2.jets))
            .Define("jet_kt2_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt2.jets))
            .Define("jet_kt2_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt2.jets))
            .Define("jet_kt2_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt2.jets))
            .Define("jet_kt2_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt2.jets))
            .Define("jet_kt2_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt2.jets))
            .Define("jet_kt2_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt2.jets))
            .Define("jet_kt2_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt2.jets))
            .Define("n_jets_kt2",           "return jet_kt2_flavor.size()")
            #.Define("pfcand_PID_kt2", "JetConstituentsUtils::get_PIDs(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle,_jet_kt2)")
            
            .Define("jet_R5_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_R5.jets))
            .Define("jet_R5_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_R5.jets))
            .Define("jet_R5_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_R5.jets))
            .Define("jet_R5_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_R5.jets))
            .Define("jet_R5_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_R5.jets))
            .Define("jet_R5_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_R5.jets))
            .Define("jet_R5_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_R5.jets))
            .Define("jet_R5_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_R5.jets) )
            .Define("n_jets_R5",           "return jet_R5_flavor.size()")
            #.Define("pfcand_PID_R5", "JetConstituentsUtils::get_PIDs(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle,_jet_R5)")
        )
        return df3

        ## tagging

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
            "FSGenMuon_eta",
            "FSGenMuon_theta",
            "FSGenMuon_phi",
            "FSGenMuon_charge",
            "FSGenMuon_mass",
            "FSGenMuon_parentPDG",
            "FSGenMuon_vertex_x",
            "FSGenMuon_vertex_y",
            "FSGenMuon_vertex_z",

            "n_AllGenTau",
            "AllGenTau_e",
            "AllGenTau_p",
            "AllGenTau_pt",
            "AllGenTau_px",
            "AllGenTau_py",
            "AllGenTau_pz",
            "AllGenTau_eta",
            "AllGenTau_theta",
            "AllGenTau_phi",
            "AllGenTau_charge",
            "AllGenTau_mass",
            "AllGenTau_parentPDG",
            "AllGenTau_vertex_x",
            "AllGenTau_vertex_y",
            "AllGenTau_vertex_z",

            "noFSRGenTau_parentPDG",

            "n_FSRGenTau",
            "FSRGenTau_e",
            "FSRGenTau_p",
            "FSRGenTau_pt",
            "FSRGenTau_px",
            "FSRGenTau_py",
            "FSRGenTau_pz",
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
            "FSGenPhoton_eta",
            "FSGenPhoton_theta",
            "FSGenPhoton_phi",
            "FSGenPhoton_charge",
            #"FSGenPhoton_parentPDG",

            "n_GenZ",
            "n_GenH",

            ######## Reconstructed particles #######
            "RecoMC_PID",

            "n_RecoElectrons",
            "RecoElectron_e",
            "RecoElectron_p",
            "RecoElectron_pt",
            "RecoElectron_px",
            "RecoElectron_py",
            "RecoElectron_pz",
            "RecoElectron_eta",
            "RecoElectron_theta",
            "RecoElectron_phi",
            "RecoElectron_charge",
            "RecoElectronTrack_absD0",
            "RecoElectronTrack_absZ0",
            "RecoElectronTrack_absD0sig",
            "RecoElectronTrack_absZ0sig",
            "RecoElectronTrack_D0cov",
            "RecoElectronTrack_Z0cov",

            "n_RecoMuons",
            "RecoMuon_e",
            "RecoMuon_p",
            "RecoMuon_pt",
            "RecoMuon_px",
            "RecoMuon_py",
            "RecoMuon_pz",
            "RecoMuon_eta",
            "RecoMuon_theta",
            "RecoMuon_phi",
            "RecoMuon_charge",
            "RecoMuonTrack_absD0",
            "RecoMuonTrack_absZ0",
            "RecoMuonTrack_absD0sig",
            "RecoMuonTrack_absZ0sig",
            "RecoMuonTrack_D0cov",
            "RecoMuonTrack_Z0cov",

            "n_RecoPhotons",
            "RecoPhoton_e",
            "RecoPhoton_p",
            "RecoPhoton_pt",
            "RecoPhoton_px",
            "RecoPhoton_py",
            "RecoPhoton_pz",
            "RecoPhoton_eta",
            "RecoPhoton_theta",
            "RecoPhoton_phi",
            "RecoPhoton_charge",

            "RecoMissingEnergy_e",
            "RecoMissingEnergy_p",
            "RecoMissingEnergy_pt",
            "RecoMissingEnergy_px",
            "RecoMissingEnergy_py",
            "RecoMissingEnergy_pz",
            "RecoMissingEnergy_eta",
            "RecoMissingEnergy_theta",
            "RecoMissingEnergy_phi",

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
            "VertexObject", 
            "RecoPartPID" ,
            "RecoPartPIDAtVertex",

        ]

        branchList += jetFlavourHelper_kt2.outputBranches() 
        branchList += jetFlavourHelper_R5.outputBranches()
        branchList += [obs for obs in jetFlavourHelper_kt2.definition.keys() if "pfcand_" in obs]
        branchList += [obs for obs in jetFlavourHelper_R5. definition.keys() if "pfcand_" in obs]
        branchList += ["jet_kt2_px", "jet_kt2_py", "jet_kt2_pz", "jet_kt2_phi", "jet_kt2_eta", "jet_kt2_energy", "jet_kt2_mass", "jet_kt2_flavor", "n_jets_kt2",]
        branchList += ["jet_R5_px", "jet_R5_py", "jet_R5_pz", "jet_R5_phi", "jet_R5_eta", "jet_R5_energy", "jet_R5_mass", "jet_R5_flavor", "n_jets_R5", ]

        return branchList