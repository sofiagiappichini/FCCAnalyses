import os, copy # tagging
import ROOT
import urllib.request

#Mandatory: List of processes
processList = {

    #'p8_ee_WW_ecm365':{'chunks':100000},
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

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#inputDir = "/ceph/sgiappic/HiggsCP/winter23"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"

#Optional: output directory, default is local running directory
#outputDir   = "/ceph/sgiappic/HiggsCP/stage1_241105/" 
outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm365/stage1_250502/ktN-tag/QQ/LL/"

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
                
                .Define("HiggsGenTau",           "FCCAnalyses::MCParticle::sel_HTauTau()(AllGenTau, Particle, Particle0, Particle1)")
                .Define("n_HiggsGenTau",      "FCCAnalyses::MCParticle::get_n(HiggsGenTau)")
                .Define("HiggsGenTau_e",     "FCCAnalyses::MCParticle::get_e(HiggsGenTau)")
                .Define("HiggsGenTau_p",     "FCCAnalyses::MCParticle::get_p(HiggsGenTau)")
                .Define("HiggsGenTau_pt",     "FCCAnalyses::MCParticle::get_pt(HiggsGenTau)")
                .Define("HiggsGenTau_px",     "FCCAnalyses::MCParticle::get_px(HiggsGenTau)")
                .Define("HiggsGenTau_py",     "FCCAnalyses::MCParticle::get_py(HiggsGenTau)")
                .Define("HiggsGenTau_pz",     "FCCAnalyses::MCParticle::get_pz(HiggsGenTau)")
                .Define("HiggsGenTau_y",    "FCCAnalyses::MCParticle::get_y(HiggsGenTau)")
                .Define("HiggsGenTau_eta",    "FCCAnalyses::MCParticle::get_eta(HiggsGenTau)")
                .Define("HiggsGenTau_theta",     "FCCAnalyses::MCParticle::get_theta(HiggsGenTau)")
                .Define("HiggsGenTau_phi",    "FCCAnalyses::MCParticle::get_phi(HiggsGenTau)")
                .Define("HiggsGenTau_parentPDG", "FCCAnalyses::MCParticle::get_leptons_origin(HiggsGenTau,Particle,Particle0)")
                .Define("HiggsGenTau_charge", "FCCAnalyses::MCParticle::get_charge(HiggsGenTau)")
                .Define("HiggsGenTau_mass",   "FCCAnalyses::MCParticle::get_mass(HiggsGenTau)")
                .Define("HiggsGenTau_vertex_x", "FCCAnalyses::MCParticle::get_vertex_x( HiggsGenTau )")
                .Define("HiggsGenTau_vertex_y", "FCCAnalyses::MCParticle::get_vertex_y( HiggsGenTau )")
                .Define("HiggsGenTau_vertex_z", "FCCAnalyses::MCParticle::get_vertex_z( HiggsGenTau )")

                .Define("WW_candidates",        "FCCAnalyses::MCParticle::sel_pdgID(24, true)(Particle)")
                .Define("WW_daughter",      "FCCAnalyses::MCParticle::sel_daughterID(15, true, true) (WW_candidates, Particle, Particle1)")

                # to exclude WW->tau tau events so they are not counted twice with WW->tau tau dedicated samples
                #.Filter("WW_daughter.size()<2")
                
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
                .Define("RecoEmiss", "FCCAnalyses::ZHfunctions::missingEnergy(365, ReconstructedParticles)") #ecm 
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

                # find leading lepton and subleading and remove them from the clustering so it's not double counting, may not be the best strategy but what else
                .Define("TauLeptons",        "FCCAnalyses::ZHfunctions::Find_LeadingPair(RecoLeptons_sel)")

                .Define("n_TauLeptons",      "ReconstructedParticle::get_n(TauLeptons)")
                .Define("TauLeptons_e",      "ReconstructedParticle::get_e(TauLeptons)")
                .Define("TauLeptons_p",      "ReconstructedParticle::get_p(TauLeptons)")
                .Define("TauLeptons_pt",      "ReconstructedParticle::get_pt(TauLeptons)")
                .Define("TauLeptons_px",      "ReconstructedParticle::get_px(TauLeptons)")
                .Define("TauLeptons_py",      "ReconstructedParticle::get_py(TauLeptons)")
                .Define("TauLeptons_pz",      "ReconstructedParticle::get_pz(TauLeptons)")
                .Define("TauLeptons_y",      "ReconstructedParticle::get_y(TauLeptons)")
                .Define("TauLeptons_eta",     "ReconstructedParticle::get_eta(TauLeptons)") #pseudorapidity eta
                .Define("TauLeptons_theta",   "ReconstructedParticle::get_theta(TauLeptons)")
                .Define("TauLeptons_phi",     "ReconstructedParticle::get_phi(TauLeptons)") #polar angle in the transverse plane phi
                .Define("TauLeptons_charge",  "ReconstructedParticle::get_charge(TauLeptons)")
                .Define("TauLeptons_mass",     "ReconstructedParticle::get_mass(TauLeptons)")
                .Define("RecoTauLeptons_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(TauLeptons,EFlowTrack_1))")
                .Define("RecoTauLeptons_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(TauLeptons,EFlowTrack_1))")
                .Define("RecoTauLeptons_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(TauLeptons,EFlowTrack_1))") #significance
                .Define("RecoTauLeptons_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(TauLeptons,EFlowTrack_1))")
                .Define("RecoTauLeptons_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(TauLeptons,EFlowTrack_1)") #variance (not sigma)
                .Define("RecoTauLeptons_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(TauLeptons,EFlowTrack_1)")

                .Define("LeadingLepton_e",      "TauLeptons_e.at(0)")
                .Define("LeadingLepton_p",      "TauLeptons_p.at(0)")
                .Define("LeadingLepton_pt",      "TauLeptons_pt.at(0)")
                .Define("LeadingLepton_px",      "TauLeptons_px.at(0)")
                .Define("LeadingLepton_py",      "TauLeptons_py.at(0)")
                .Define("LeadingLepton_pz",      "TauLeptons_pz.at(0)")
                .Define("LeadingLepton_y",      "TauLeptons_y.at(0)")
                .Define("LeadingLepton_eta",     "TauLeptons_eta.at(0)") #pseudorapidity eta
                .Define("LeadingLepton_theta",   "TauLeptons_theta.at(0)")
                .Define("LeadingLepton_phi",     "TauLeptons_phi.at(0)") #polar angle in the transverse plane phi
                .Define("LeadingLepton_charge",  "TauLeptons_charge.at(0)")
                .Define("LeadingLepton_mass",     "TauLeptons_mass.at(0)")
                .Define("RecoLeadingLepton_absD0", "RecoTauLeptons_absD0.at(0)")
                .Define("RecoLeadingLepton_absZ0", "RecoTauLeptons_absZ0.at(0)")
                .Define("RecoLeadingLepton_absD0sig", "RecoTauLeptons_absD0sig.at(0)") #significance
                .Define("RecoLeadingLepton_absZ0sig", "RecoTauLeptons_absZ0sig.at(0)")
                .Define("RecoLeadingLepton_D0cov", "RecoTauLeptons_D0cov.at(0)") #variance (not sigma)
                .Define("RecoLeadingLepton_Z0cov", "RecoTauLeptons_Z0cov.at(0)")

                .Define("SubleadingLepton_e",      "TauLeptons_e.at(1)")
                .Define("SubleadingLepton_p",      "TauLeptons_p.at(1)")
                .Define("SubleadingLepton_pt",      "TauLeptons_pt.at(1)")
                .Define("SubleadingLepton_px",      "TauLeptons_px.at(1)")
                .Define("SubleadingLepton_py",      "TauLeptons_py.at(1)")
                .Define("SubleadingLepton_pz",      "TauLeptons_pz.at(1)")
                .Define("SubleadingLepton_y",      "TauLeptons_y.at(1)")
                .Define("SubleadingLepton_eta",     "TauLeptons_eta.at(1)") #pseudorapidity eta
                .Define("SubleadingLepton_theta",   "TauLeptons_theta.at(1)")
                .Define("SubleadingLepton_phi",     "TauLeptons_phi.at(1)") #polar angle in the transverse plane phi
                .Define("SubleadingLepton_charge",  "TauLeptons_charge.at(1)")
                .Define("SubleadingLepton_mass",     "TauLeptons_mass.at(1)")
                .Define("RecoSubleadingLepton_absD0", "RecoTauLeptons_absD0.at(1)")
                .Define("RecoSubleadingLepton_absZ0", "RecoTauLeptons_absZ0.at(1)")
                .Define("RecoSubleadingLepton_absD0sig", "RecoTauLeptons_absD0sig.at(1)") #significance
                .Define("RecoSubleadingLepton_absZ0sig", "RecoTauLeptons_absZ0sig.at(1)")
                .Define("RecoSubleadingLepton_D0cov", "RecoTauLeptons_D0cov.at(1)") #variance (not sigma)
                .Define("RecoSubleadingLepton_Z0cov", "RecoTauLeptons_Z0cov.at(1)")

                .Filter("n_TauLeptons==2") #making sure the pair is found

                .Define("ReconstructedParticlesJET",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,TauLeptons)")
            
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

                .Define("TauFromJet_R5", "FCCAnalyses::ZHfunctions::findTauInJet({})".format(jetClusteringHelper_R5.constituents)) 
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

                .Define("TauFromJet_kt2", "FCCAnalyses::ZHfunctions::findTauInJet({})".format(jetClusteringHelper_kt2.constituents)) 
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

                ##########################
                ###### Ex. stage2 ########
                ##########################

                ### to find already made functions, this is where they are or where they can be added instead of writing them here
                ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

                ### defining filters for two sel lepotons, two no tau jets

                ### when working with Z jets, remember to use the Leptons_sel class because they are the ones not in the jets
                ### when working with tau jets it does not matter since the tau jets don't have any lepton in them so there is no confusion

                .Define("TauTag_px",      "TagJet_kt2_px[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_py",      "TagJet_kt2_py[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_pz",      "TagJet_kt2_pz[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_pt",      "TagJet_kt2_pt[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_p",      "TagJet_kt2_p[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_e",      "TagJet_kt2_e[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_phi",      "TagJet_kt2_phi[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_eta",      "TagJet_kt2_eta[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_theta",      "TagJet_kt2_theta[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_charge",      "TagJet_kt2_charge[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_mass",      "TagJet_kt2_mass[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_isG",      "TagJet_kt2_isG[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_isU",      "TagJet_kt2_isU[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_isD",      "TagJet_kt2_isD[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_isS",      "TagJet_kt2_isS[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_isC",      "TagJet_kt2_isC[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_isB",      "TagJet_kt2_isB[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_isTAU",      "TagJet_kt2_isTAU[TagJet_kt2_isTAU>0.5]")
                .Define("TauTag_flavor",      "TagJet_kt2_flavor[TagJet_kt2_isTAU>0.5]")
                .Define("n_TauTag_constituents",        "n_TagJet_kt2_constituents[TagJet_kt2_isTAU>0.5]")
                .Define("n_TauTag_charged_constituents",        "n_TagJet_kt2_charged_constituents[TagJet_kt2_isTAU>0.5]")
                .Define("n_TauTag_neutral_constituents",        "n_TagJet_kt2_neutral_constituents[TagJet_kt2_isTAU>0.5]")
                .Define("n_TauTag",          "TauTag_px.size()")

                .Define("QuarkTag_px",      "TagJet_kt2_px[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_py",      "TagJet_kt2_py[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_pz",      "TagJet_kt2_pz[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_pt",      "TagJet_kt2_pt[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_p",      "TagJet_kt2_p[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_e",      "TagJet_kt2_e[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_phi",      "TagJet_kt2_phi[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_eta",      "TagJet_kt2_eta[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_theta",      "TagJet_kt2_theta[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_charge",      "TagJet_kt2_charge[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_mass",      "TagJet_kt2_mass[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_isG",      "TagJet_kt2_isG[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_isU",      "TagJet_kt2_isU[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_isD",      "TagJet_kt2_isD[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_isS",      "TagJet_kt2_isS[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_isC",      "TagJet_kt2_isC[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_isB",      "TagJet_kt2_isB[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_isTAU",      "TagJet_kt2_isTAU[TagJet_kt2_isTAU<=0.5]")
                .Define("QuarkTag_flavor",      "TagJet_kt2_flavor[TagJet_kt2_isTAU<=0.5]")
                .Define("n_QuarkTag_constituents",        "n_TagJet_kt2_constituents[TagJet_kt2_isTAU<=0.5]")
                .Define("n_QuarkTag_charged_constituents",        "n_TagJet_kt2_charged_constituents[TagJet_kt2_isTAU<=0.5]")
                .Define("n_QuarkTag_neutral_constituents",        "n_TagJet_kt2_neutral_constituents[TagJet_kt2_isTAU<=0.5]")
                .Define("n_QuarkTag",     "QuarkTag_charge.size()")

                ##########################
                ######## FILTER 2 ########
                ##########################

                .Filter("n_TauTag==0 && n_QuarkTag==2 && n_RecoLeptons_sel==2")

                ##################

                .Define("RecoZ1_p4",      "TLorentzVector(QuarkTag_px.at(0), QuarkTag_py.at(0), QuarkTag_pz.at(0), QuarkTag_e.at(0))")
                .Define("RecoZ2_p4",      "TLorentzVector(QuarkTag_px.at(1), QuarkTag_py.at(1), QuarkTag_pz.at(1), QuarkTag_e.at(1))")
                
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

                .Define("RecoTau1_p4",      "TLorentzVector(LeadingLepton_px, LeadingLepton_py, LeadingLepton_pz, LeadingLepton_e)")
                .Define("RecoTau2_p4",      "TLorentzVector(SubleadingLepton_px, SubleadingLepton_py, SubleadingLepton_pz, SubleadingLepton_e)")
                .Define("RecoTau1_type",        "if (LeadingLepton_mass<0.05) return float(-0.11); else return float(-0.13);")
                .Define("RecoTau2_type",        "if (SubleadingLepton_mass<0.05) return float(-0.13); else return float(-0.11);")
                .Define("n_RecoTau1_constituents",        "return float(1);")
                .Define("n_RecoTau2_constituents",        "return float(1);")
                .Define("n_RecoTau1_charged_constituents",        "return float(1);")
                .Define("n_RecoTau2_charged_constituents",        "return float(1);")
                .Define("n_RecoTau1_neutral_constituents",        "return float(0);")
                .Define("n_RecoTau2_neutral_constituents",        "return float(0);")

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

                .Define("Total_p4",     "TLorentzVector(0.,0.,1.,365.)")
                .Define("Recoil",       "(Total_p4-RecoZ_p4).M()")

                .Define("p12",      "(TauLead_py*TauSub_px-TauLead_px*TauSub_py)")
                .Define("r0",       "abs((RecoEmiss_py*TauLead_px-RecoEmiss_px*TauLead_py)/p12)")
                .Define("f0",       "1./(1.+r0)")
                .Define("r1",       "abs((RecoEmiss_py*TauSub_px-RecoEmiss_px*TauSub_py)/p12)")
                .Define("f1",       "1./(1.+r1)")
                .Define("Collinear_mass",       "RecoH_mass/sqrt(f0*f1)")

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

            "LeadingLepton_e",
            "LeadingLepton_p",
            "LeadingLepton_pt",
            "LeadingLepton_px",
            "LeadingLepton_py",
            "LeadingLepton_pz",
            "LeadingLepton_y",
            "LeadingLepton_eta",
            "LeadingLepton_theta",
            "LeadingLepton_phi",
            "LeadingLepton_charge",
            "LeadingLepton_mass",
            "RecoLeadingLepton_absD0",
            "RecoLeadingLepton_absZ0",
            "RecoLeadingLepton_absD0sig",
            "RecoLeadingLepton_absZ0sig",
            "RecoLeadingLepton_D0cov",
            "RecoLeadingLepton_Z0cov",

            "SubleadingLepton_e",
            "SubleadingLepton_p",
            "SubleadingLepton_pt",
            "SubleadingLepton_px",
            "SubleadingLepton_py",
            "SubleadingLepton_pz",
            "SubleadingLepton_y",
            "SubleadingLepton_eta",
            "SubleadingLepton_theta",
            "SubleadingLepton_phi",
            "SubleadingLepton_charge",
            "SubleadingLepton_mass",
            "RecoSubleadingLepton_absD0",
            "RecoSubleadingLepton_absZ0",
            "RecoSubleadingLepton_absD0sig",
            "RecoSubleadingLepton_absZ0sig",
            "RecoSubleadingLepton_D0cov",
            "RecoSubleadingLepton_Z0cov",

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

        ]

        return branchList