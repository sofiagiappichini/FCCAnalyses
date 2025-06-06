import os, copy # tagging
import ROOT
import urllib.request

#Mandatory: List of processes
processList = {
    #using only about 5M events per sample for testing
    "p8_ee_Ztautau_ecm91":{'chunks':1000, 'fraction':0.05},
    #'wzp6_ee_tautau_ecm240':{'chunks':1000, 'fraction':0.1},
    #'wzp6_ee_tautau_ecm365':{'chunks':1000, 'fraction':0.5},
    #'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':10},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#inputDir = "/ceph/sgiappic/HiggsCP/winter23"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"

#Optional: output directory, default is local running directory
#outputDir   = "/ceph/sgiappic/HiggsCP/stage1_241105/" 
outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/taureco_test/"

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

## tagging -------------------------------
## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
#model_dir = "/ceph/sgiappic/FCCAnalyses/addons/jet_flavor_tagging/winter2023/wc_pt_7classes_12_04_2023/"
model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_7classes_12_04_2023/"

local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    #else:
    #    urllib.request.urlretrieve(url, os.path.basename(url))
    #    return os.path.basename(url)
    ## this is the old version of the tagger and we don't care about it


weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
    InclusiveJetClusteringHelper,
)

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():
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

                #distinguish between pre fsr and after iterative fsr taus and keep them in separate classes to be analysed
                .Define("AllGenTauPlus",    "FCCAnalyses::MCParticle::sel_pdgID(-15, false)(Particle)")
                .Define("AllGenTauMin",    "FCCAnalyses::MCParticle::sel_pdgID(15, false)(Particle)")
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

                .Define("FSRGenTauPlus",       "FCCAnalyses::MCParticle::sel_daughterID(-15, false, false)(AllGenTauPlus,Particle,Particle1)")
                .Define("FSRGenTauMin",       "FCCAnalyses::MCParticle::sel_daughterID(15, false, false)(AllGenTauMin,Particle,Particle1)")
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

                # study the reconstruction by decay mode, only br>1%
                #rho nu decay (pi pi0 nu)
                .Define("TauPtoRhoNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 22, 22, -16},  true, false, false, false)  ( Particle, Particle1)" ) #size is the size of the vector (mother+daughters) because it only saves the first matching decay in the event, not all the decays
                .Define("TauMtoRhoNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 22, 22, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #pi nu decay
                .Define("TauPtoPiNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, -16},  true, false, false, false)  ( Particle, Particle1)" ) #size is the size of the vector (mother+daughters) because it only saves the first matching decay in the event, not all the decays
                .Define("TauMtoPiNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #a1 nu decay (pi pi0 pi0 nu)
                .Define("TauPto2Pi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 22, 22, 22, 22, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMto2Pi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 22, 22, 22, 22, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #a1 nu decay (pi pi0 pi0 pi0 nu)
                .Define("TauPto3Pi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 22, 22, 22, 22, 22, 22, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMto3Pi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 22, 22, 22, 22, 22, 22, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #a1 nu decay - three prongs (pi pi pi nu)
                .Define("TauPto3PiNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 211, -211, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMto3PiNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, -211, 211, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #a1 nu decay - three prongs (pi pi pi pi0 nu)
                .Define("TauPto3PiPi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 211, -211, 22, 22, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMto3PiPi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, -211, 211, 22, 22, 16},  true, false, false, false)  ( Particle, Particle1)" )

                .Define("n_TauPtoRhoNu",  "TauPtoRhoNu_idx.size()" ) #size is the size of the vector (mother+daughters) because it only saves the first matching decay in the event, not all the decays
                .Define("n_TauMtoRhoNu",  "TauMtoRhoNu_idx.size()" )
                #pi nu decay
                .Define("n_TauPtoPiNu",  "TauPtoPiNu_idx.size()" ) #size is the size of the vector (mother+daughters) because it only saves the first matching decay in the event, not all the decays
                .Define("n_TauMtoPiNu",  "TauMtoPiNu_idx.size()" )
                #a1 nu decay (pi pi0 pi0 nu)
                .Define("n_TauPto2Pi0Nu",  "TauPto2Pi0Nu_idx.size()" )
                .Define("n_TauMto2Pi0Nu",  "TauMto2Pi0Nu_idx.size()" )
                #a1 nu decay (pi pi0 pi0 pi0 nu)
                .Define("n_TauPto3Pi0Nu",  "TauPto3Pi0Nu_idx.size()" )
                .Define("n_TauMto3Pi0Nu",  "TauMto3Pi0Nu_idx.size()" )
                #a1 nu decay - three prongs (pi pi pi nu)
                .Define("n_TauPto3PiNu",  "TauPto3PiNu_idx.size()" )
                .Define("n_TauMto3PiNu",  "TauMto3PiNu_idx.size()" )
                #a1 nu decay - three prongs (pi pi pi pi0 nu)
                .Define("n_TauPto3PiPi0Nu",  "TauPto3PiPi0Nu_idx.size()" )
                .Define("n_TauMto3PiPi0Nu",  "TauMto3PiPi0Nu_idx.size()" )

                
                ##################
                # Reco particles #
                ##################

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
                .Define("RecoPhoton_mass",  "ReconstructedParticle::get_mass(RecoPhotons)")

                .Define("NoMuons", "ReconstructedParticle::remove(ReconstructedParticles, RecoMuons)")
                .Define("NoLeptons", "ReconstructedParticle::remove(NoMuons, RecoElectrons)")

                # different definition of missing energy from fccanalysis classes instead of edm4hep
                .Define("RecoEmiss", "FCCAnalyses::ZHfunctions::missingEnergy(91, ReconstructedParticles)") #ecm 
                .Define("RecoEmiss_px",  "RecoEmiss[0].momentum.x")
                .Define("RecoEmiss_py",  "RecoEmiss[0].momentum.y")
                .Define("RecoEmiss_pz",  "RecoEmiss[0].momentum.z")
                .Define("RecoEmiss_pt",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py)")
                .Define("RecoEmiss_p",  "return sqrt(RecoEmiss_px*RecoEmiss_px + RecoEmiss_py*RecoEmiss_py + RecoEmiss_pz*RecoEmiss_pz)")
                .Define("RecoEmiss_e",   "RecoEmiss[0].energy")
                .Define("RecoEmiss_p4",  "TLorentzVector(RecoEmiss_px, RecoEmiss_py, RecoEmiss_pz, RecoEmiss_e)")
                .Define("RecoEmiss_eta",    "RecoEmiss_p4.Eta()")
                .Define("RecoEmiss_phi",    "RecoEmiss_p4.Phi()")
                .Define("RecoEmiss_theta",    "RecoEmiss_p4.Theta()")
                .Define("RecoEmiss_y",    "RecoEmiss_p4.Rapidity()")
                .Define("RecoEmiss_costheta",   "abs(std::cos(RecoEmiss_theta))")

                ####################
                ##### FILTER #######
                ####################

                # two leptons in the whole event that make the Z boson, even if using tagged jets taus should not have leptons in the jets!!! should help with background rejection
                #.Define("OnePair",     "(((n_RecoElectrons==2 and n_RecoMuons==0) or (n_RecoElectrons==0 and n_RecoMuons==2)) and (RecoLepton_charge.at(0) + RecoLepton_charge.at(1))==0)*1.0")

                #.Filter("OnePair==1")

                .Define("ReconstructedParticlesJET",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,RecoLeptons)")
            
        )
        #### tagging
        
        global jetClusteringHelper_R5
        global jetFlavourHelper_R5
        ## define jet and run clustering parameters
        ## name of collections in EDM root files
        collections = {
            "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticlesJET",
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
        #INCLUSIVE R=0.5
        ## def __init__(self, coll, njets, tag="")
        jetClusteringHelper_R5  = InclusiveJetClusteringHelper(
            collections["PFParticles"], 0.5, 2, "R5"
        )
        df2 = jetClusteringHelper_R5.define(df2)

        ## define jet flavour tagging parameters
        jetFlavourHelper_R5 = JetFlavourHelper(
            collections,
            jetClusteringHelper_R5.jets,
            jetClusteringHelper_R5.constituents,
            "R5",
        )
        ## define observables for tagger
        df2 = jetFlavourHelper_R5.define(df2)

        ## tagger inference
        df2 = jetFlavourHelper_R5.inference(weaver_preproc, weaver_model, df2)

        df2 = (df2
                .Define("TagJet_R5_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_p",           "JetClusteringUtils::get_p({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_pt",           "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_theta",          "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_e",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_R5.jets))
                .Define("TagJet_R5_charge",         "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_R5.constituents))
                .Define("TagJet_R5_flavor",        "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_R5.jets))
                .Define("n_TagJet_R5_constituents",        "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_R5.constituents))
                .Define("n_TagJet_R5_charged_constituents",        "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_R5.constituents))
                .Define("n_TagJet_R5_neutral_constituents",        "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_R5.constituents))
                .Define("n_TagJet_R5",           "return TagJet_R5_e.size()")
                .Define("TagJet_R5_cleanup",       "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_R5.constituents))

                .Define("TagJet_R5_isG",    "recojet_isG_R5")
                .Define("TagJet_R5_isU",    "recojet_isU_R5")
                .Define("TagJet_R5_isD",    "recojet_isD_R5")
                .Define("TagJet_R5_isS",    "recojet_isS_R5")
                .Define("TagJet_R5_isC",    "recojet_isC_R5")
                .Define("TagJet_R5_isB",    "recojet_isB_R5")
                .Define("TagJet_R5_isTAU",    "recojet_isTAU_R5")

                .Define("TauFromJet_R5", "FCCAnalyses::ZHfunctions::findTauInJet_pi0({})".format(jetClusteringHelper_R5.constituents)) 
                .Define("TauFromJet_R5_type_sel","ReconstructedParticle::get_type(TauFromJet_R5)")
                .Define("TauFromJet_R5_tau", "TauFromJet_R5[TauFromJet_R5_type_sel>=0]") 
                .Define("TauFromJet_R5_p","ReconstructedParticle::get_p(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_pt","ReconstructedParticle::get_pt(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_px","ReconstructedParticle::get_px(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_py","ReconstructedParticle::get_py(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_pz","ReconstructedParticle::get_pz(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_theta","ReconstructedParticle::get_theta(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_phi","ReconstructedParticle::get_phi(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_eta","ReconstructedParticle::get_eta(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_y","ReconstructedParticle::get_y(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_e","ReconstructedParticle::get_e(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_charge","ReconstructedParticle::get_charge(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_type","ReconstructedParticle::get_type(TauFromJet_R5_tau)")
                .Define("TauFromJet_R5_mass","ReconstructedParticle::get_mass(TauFromJet_R5_tau)")
                .Define("n_TauFromJet_R5","TauFromJet_R5_pt.size()")

                .Define("TagJet_R5_sel_e",      "TagJet_R5_e[TauFromJet_R5_type_sel<0 ]")
                .Define("TagJet_R5_sel_p",      "TagJet_R5_p[TauFromJet_R5_type_sel<0 ]")
                .Define("TagJet_R5_sel_pt",      "TagJet_R5_pt[TauFromJet_R5_type_sel<0 ]")
                .Define("TagJet_R5_sel_px",      "TagJet_R5_px[TauFromJet_R5_type_sel<0 ]")
                .Define("TagJet_R5_sel_py",      "TagJet_R5_py[TauFromJet_R5_type_sel<0 ]")
                .Define("TagJet_R5_sel_pz",      "TagJet_R5_pz[TauFromJet_R5_type_sel<0 ]")
		        .Define("TagJet_R5_sel_eta",     "TagJet_R5_eta[TauFromJet_R5_type_sel<0 ]")
                .Define("TagJet_R5_sel_theta",   "TagJet_R5_theta[TauFromJet_R5_type_sel<0 ]")
		        .Define("TagJet_R5_sel_phi",     "TagJet_R5_phi[TauFromJet_R5_type_sel<0 ]")
                .Define("TagJet_R5_sel_mass",      "TagJet_R5_mass[TauFromJet_R5_type_sel<0 ]")
                .Define("n_TagJet_R5_sel", "TagJet_R5_sel_e.size()")
        )

        #EXCLUSIVE 2 JETS=
        jetClusteringHelper_kt2  = ExclusiveJetClusteringHelper(
            collections["PFParticles"], 2, "kt2"
        )
        df2 = jetClusteringHelper_kt2.define(df2)

        ## define jet flavour tagging parameters
        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections,
            jetClusteringHelper_kt2.jets,
            jetClusteringHelper_kt2.constituents,
            "kt2",
        )
        ## define observables for tagger
        df2 = jetFlavourHelper_kt2.define(df2)

        ## tagger inference
        df2 = jetFlavourHelper_kt2.inference(weaver_preproc, weaver_model, df2)

        df2 = (df2
                .Define("TagJet_kt2_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_p",           "JetClusteringUtils::get_p({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_pt",           "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_theta",          "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_e",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt2.jets))
                .Define("TagJet_kt2_charge",         "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("TagJet_kt2_flavor",        "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt2.jets))
                .Define("n_TagJet_kt2_constituents",        "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("n_TagJet_kt2_charged_constituents",        "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("n_TagJet_kt2_neutral_constituents",        "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_kt2.constituents))
                .Define("n_TagJet_kt2",           "return int(TagJet_kt2_flavor.size())")
                .Define("TagJet_kt2_cleanup",       "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_kt2.constituents))

                .Define("TagJet_kt2_isG",    "recojet_isG_kt2")
                .Define("TagJet_kt2_isU",    "recojet_isU_kt2")
                .Define("TagJet_kt2_isD",    "recojet_isD_kt2")
                .Define("TagJet_kt2_isS",    "recojet_isS_kt2")
                .Define("TagJet_kt2_isC",    "recojet_isC_kt2")
                .Define("TagJet_kt2_isB",    "recojet_isB_kt2")
                .Define("TagJet_kt2_isTAU",    "recojet_isTAU_kt2")

                .Define("TauFromJet_kt2", "FCCAnalyses::ZHfunctions::findTauInJet_pi0({})".format(jetClusteringHelper_kt2.constituents)) 
                .Define("TauFromJet_kt2_type_sel","ReconstructedParticle::get_type(TauFromJet_kt2)")
                .Define("TauFromJet_kt2_tau", "TauFromJet_kt2[TauFromJet_kt2_type_sel>=0]") 
                .Define("TauFromJet_kt2_p","ReconstructedParticle::get_p(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_pt","ReconstructedParticle::get_pt(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_px","ReconstructedParticle::get_px(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_py","ReconstructedParticle::get_py(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_pz","ReconstructedParticle::get_pz(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_theta","ReconstructedParticle::get_theta(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_phi","ReconstructedParticle::get_phi(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_eta","ReconstructedParticle::get_eta(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_y","ReconstructedParticle::get_y(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_e","ReconstructedParticle::get_e(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_charge","ReconstructedParticle::get_charge(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_type","ReconstructedParticle::get_type(TauFromJet_kt2_tau)")
                .Define("TauFromJet_kt2_mass","ReconstructedParticle::get_mass(TauFromJet_kt2_tau)")
                .Define("n_TauFromJet_kt2","TauFromJet_kt2_pt.size()")

                .Define("TagJet_kt2_sel_e",      "TagJet_kt2_e[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_p",      "TagJet_kt2_p[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_pt",      "TagJet_kt2_pt[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_px",      "TagJet_kt2_px[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_py",      "TagJet_kt2_py[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_pz",      "TagJet_kt2_pz[TauFromJet_kt2_type_sel<0]")
		        .Define("TagJet_kt2_sel_eta",     "TagJet_kt2_eta[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_theta",   "TagJet_kt2_theta[TauFromJet_kt2_type_sel<0]")
		        .Define("TagJet_kt2_sel_phi",     "TagJet_kt2_phi[TauFromJet_kt2_type_sel<0]")
                .Define("TagJet_kt2_sel_mass",      "TagJet_kt2_mass[TauFromJet_kt2_type_sel<0]")
                .Define("n_TagJet_kt2_sel", "TagJet_kt2_sel_e.size()")

        )

        df2 = (df2

                ### now i want to study the thadronic tau reconstruction with the function and the jet tagger by comparing it to the gen info for taus decaying not to electrons or muons

                .Define("GenTau_el",       "FCCAnalyses::MCParticle::sel_daughterID(-11, false, true)(FSRGenTau,Particle,Particle1)")
                .Define("GenTau_had",       "FCCAnalyses::MCParticle::sel_daughterID(-13, false, true)(GenTau_el,Particle,Particle1)")
                .Define("HadGenTau_eta",    "FCCAnalyses::MCParticle::get_eta(GenTau_had)")
                .Define("HadGenTau_phi",    "FCCAnalyses::MCParticle::get_phi(GenTau_had)")
                .Define("HadGenTau_p",    "FCCAnalyses::MCParticle::get_p(GenTau_had)")
                .Define("HadGenTau_px",    "FCCAnalyses::MCParticle::get_px(GenTau_had)")
                .Define("HadGenTau_py",    "FCCAnalyses::MCParticle::get_py(GenTau_had)")
                .Define("HadGenTau_pz",    "FCCAnalyses::MCParticle::get_pz(GenTau_had)")
                .Define("HadGenTau_e",    "FCCAnalyses::MCParticle::get_e(GenTau_had)")
                .Define("HadGenTau_p4",  "FCCAnalyses::ZHfunctions::build_p4(HadGenTau_px, HadGenTau_py, HadGenTau_pz, HadGenTau_e)")
                .Define("HadGenTau_charge",    "FCCAnalyses::MCParticle::get_charge(GenTau_had)")
                .Define("n_GenTau_had",     "HadGenTau_eta.size()")

                .Define("TauTag_eta_R5",      "TagJet_R5_eta[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_phi_R5",      "TagJet_R5_phi[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_p_R5",      "TagJet_R5_p[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_R5_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_R5, HadGenTau_phi, TauTag_eta_R5, HadGenTau_eta, 0.2)")
                .Define("TauTag_R5_Gen_p",       "FCCAnalyses::ZHfunctions::deltaR_sel_diff(TauTag_p_R5, HadGenTau_p, TauTag_phi_R5, HadGenTau_phi, TauTag_eta_R5, HadGenTau_eta, 0.2)")
                .Define("n_TauTag_R5_match",          "if (n_GenTau_had>0) return TauTag_R5_idx.size(); else return TauTag_eta_R5.size();")

                .Define("TauTag_eta_kt2",      "TagJet_kt2_eta[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_phi_kt2",      "TagJet_kt2_phi[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_p_kt2",      "TagJet_kt2_p[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_kt2_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_kt2, HadGenTau_phi, TauTag_eta_kt2, HadGenTau_eta, 0.2)")
                .Define("TauTag_kt2_Gen_p",       "FCCAnalyses::ZHfunctions::deltaR_sel_diff(TauTag_p_kt2, HadGenTau_p, TauTag_phi_kt2, HadGenTau_phi, TauTag_eta_kt2, HadGenTau_eta, 0.2)")
                .Define("n_TauTag_kt2_match",          "if (n_GenTau_had>0) return TauTag_kt2_idx.size(); else return TauTag_eta_kt2.size();")

                .Define("TauFromJet_R5_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauFromJet_R5_phi, HadGenTau_phi, TauFromJet_R5_eta, HadGenTau_eta, 0.2)")
                .Define("n_TauFromJet_R5_match",          "if (n_GenTau_had>0) return TauFromJet_R5_idx.size(); else return n_TauFromJet_R5;")

                .Define("TauFromJet_kt2_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauFromJet_kt2_phi, HadGenTau_phi, TauFromJet_kt2_eta, HadGenTau_eta, 0.2)")
                .Define("n_TauFromJet_kt2_match",          "if (n_GenTau_had>0) return TauFromJet_kt2_idx.size(); else return n_TauFromJet_kt2;")

                .Define("n_events_R5tag",       "if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==0) return 0; else return -1;")
                .Define("n_events_R5excl",       "if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==0) return 0; else return -1;")

                .Define("n_events_ktNtag",       "if (n_GenTau_had==n_TauTag_kt2_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_kt2_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauTag_kt2_match && n_GenTau_had==0) return 0; else return -1;")
                .Define("n_events_ktNexcl",       "if (n_GenTau_had==n_TauFromJet_kt2_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauFromJet_kt2_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauFromJet_kt2_match && n_GenTau_had==0) return 0; else return -1;")
                
                ## matching by decay mode, save the tau type and then plot it against the gen decay mode

                .Define("TauP_kt2_type",     "if (n_events_ktNexcl==2 && TauFromJet_kt2_charge.at(0)==1) return TauFromJet_kt2_type.at(0); else if (n_events_ktNexcl==2 && TauFromJet_kt2_charge.at(1)==1) return TauFromJet_kt2_type.at(1); else return int(-99.)")
                .Define("TauM_kt2_type",     "if (n_events_ktNexcl==2 && TauFromJet_kt2_charge.at(0)==(-1)) return TauFromJet_kt2_type.at(0); else if (n_events_ktNexcl==2 && TauFromJet_kt2_charge.at(1)==(-1)) return TauFromJet_kt2_type.at(1); else return int(-99.)")

                .Define("TauP_R5_type",     "if (n_events_R5excl==2 && TauFromJet_R5_charge.at(0)==1) return TauFromJet_R5_type.at(0); else if (n_events_R5excl==2 && TauFromJet_R5_charge.at(1)==1) return TauFromJet_R5_type.at(1); else return int(-99.)")
                .Define("TauM_R5_type",     "if (n_events_R5excl==2 && TauFromJet_R5_charge.at(0)==(-1)) return TauFromJet_R5_type.at(0); else if (n_events_R5excl==2 && TauFromJet_R5_charge.at(1)==(-1)) return TauFromJet_R5_type.at(1); else return int(-99.)")

                # following Belle reconstruction https://arxiv.org/pdf/1310.8503 to get the tau 4 vector in the recoil frame, then get the neutrino momentum by subtraction
                # then following ILC polarimetric vectors for the cp angle
                # the reconstruction does not work, the taus have about 5 gev more energy than they should

                .Filter("n_TauFromJet_kt2==2 && n_TagJet_kt2_sel==0 && n_RecoLeptons==0")
                .Filter("(TauFromJet_kt2_charge.at(0) + TauFromJet_kt2_charge.at(1))==0") 

                .Filter("n_GenTau_had==2")

                .Define("TauFromJet_kt2_p4",  "FCCAnalyses::ZHfunctions::build_p4(TauFromJet_kt2_px, TauFromJet_kt2_py, TauFromJet_kt2_pz, TauFromJet_kt2_e)")

                .Define("RecoZ_p4",         "TauFromJet_kt2_p4.at(0)+TauFromJet_kt2_p4.at(1)")
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

                .Define("Total_p4",     "TLorentzVector(0.,0.,1.,91.)")
                .Define("Recoil_True_Tau_p4",        "FCCAnalyses::ZHfunctions::build_tau_p4(Total_p4, RecoEmiss_p4, TauFromJet_kt2_p4, TauFromJet_kt2_charge)")
                #filtering events where the discriminant to solve is negative and so the reconstruction didn't work out
                .Define("Belle_Filter",     "if (Recoil_True_Tau_p4.at(0).P()!=0 && Recoil_True_Tau_p4.at(1).P()!=0) return 1; else return 0;")

                .Define("True_TauP_p4",     "Recoil_True_Tau_p4.at(0)")
                .Define("True_TauM_p4",     "Recoil_True_Tau_p4.at(1)")

                .Define("True_NuP_p4",      "Recoil_True_Tau_p4.at(0) - TauFromJet_kt2_p4.at(0)")
                .Define("True_NuM_p4",      "Recoil_True_Tau_p4.at(1) - TauFromJet_kt2_p4.at(1)")

                .Define("Total_E",      "(True_TauP_p4+True_TauM_p4).E()")
                .Define("RecoGen_TauP",     "if (HadGenTau_charge.at(0)==1) return (True_TauP_p4-HadGenTau_p4.at(0)); else return (True_TauP_p4-HadGenTau_p4.at(1));")
                .Define("RecoGen_TauM",     "if (HadGenTau_charge.at(0)==1) return (True_TauM_p4-HadGenTau_p4.at(1)); else return (True_TauM_p4-HadGenTau_p4.at(0));")



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

            "TagJet_kt2_px", 
            "TagJet_kt2_py",    
            "TagJet_kt2_pz",      
            "TagJet_kt2_p",  
            "TagJet_kt2_pt",    
            "TagJet_kt2_phi", 
            "TagJet_kt2_eta",     
            "TagJet_kt2_theta",          
            "TagJet_kt2_e",     
            "TagJet_kt2_mass",        
            "TagJet_kt2_charge",       
            "TagJet_kt2_flavor", 
            "n_TagJet_kt2_constituents",   
            "n_TagJet_kt2_charged_constituents",   
            "n_TagJet_kt2_neutral_constituents",   
            "n_TagJet_kt2",          

            "TagJet_kt2_isG",  
            "TagJet_kt2_isU",
            "TagJet_kt2_isD",   
            "TagJet_kt2_isS",  
            "TagJet_kt2_isC",
            "TagJet_kt2_isB",  
            "TagJet_kt2_isTAU",

            "TauFromJet_kt2_p",
            "TauFromJet_kt2_pt",
            "TauFromJet_kt2_px",
            "TauFromJet_kt2_py",
            "TauFromJet_kt2_pz",
            "TauFromJet_kt2_theta",
            "TauFromJet_kt2_phi",
            "TauFromJet_kt2_e",
            "TauFromJet_kt2_eta",
            "TauFromJet_kt2_y",
            "TauFromJet_kt2_charge",
            "TauFromJet_kt2_type",
            "TauFromJet_kt2_mass",
            "n_TauFromJet_kt2",

            "TagJet_kt2_sel_e",     
            "TagJet_kt2_sel_p",     
            "TagJet_kt2_sel_pt",     
            "TagJet_kt2_sel_px",   
            "TagJet_kt2_sel_py",   
            "TagJet_kt2_sel_pz",     
            "TagJet_kt2_sel_eta",    
            "TagJet_kt2_sel_theta",   
            "TagJet_kt2_sel_phi",     
            "TagJet_kt2_sel_mass",      
            "n_TagJet_kt2_sel",

            "n_GenTau_had", 
            "n_TauTag_R5_match",  
            "TauTag_R5_Gen_p",
            "n_events_R5tag",  
            "n_events_R5excl",

            "n_TauTag_kt2_match",  
            "TauTag_kt2_Gen_p",
            "n_events_ktNtag",  
            "n_events_ktNexcl",

            "n_TauPtoRhoNu", 
            "n_TauMtoRhoNu",  
            "n_TauPtoPiNu", 
            "n_TauMtoPiNu",  
            "n_TauPto2Pi0Nu", 
            "n_TauMto2Pi0Nu",  
            "n_TauPto3Pi0Nu", 
            "n_TauMto3Pi0Nu", 
            "n_TauPto3PiNu",  
            "n_TauMto3PiNu", 
            "n_TauPto3PiPi0Nu",  
            "n_TauMto3PiPi0Nu",

            "TauP_kt2_type", 
            "TauM_kt2_type",
            "TauP_R5_type", 
            "TauM_R5_type",

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

            "Recoil_True_Tau_p4", 
            "True_TauP_p4",  
            "True_TauM_p4",  
            "True_NuP_p4",  
            "True_NuM_p4",
            "Total_E",
            "RecoGen_TauP",
            "RecoGen_TauM",
            "Belle_Filter",

        ]

        return branchList