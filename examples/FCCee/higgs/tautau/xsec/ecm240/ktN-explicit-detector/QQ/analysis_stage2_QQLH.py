import os, copy # tagging
import ROOT
import urllib.request
from copy import deepcopy
#Mandatory: List of processes
processList = {

    'p8_ee_WW_ecm240':{'chunks':3740},
    'p8_ee_Zqq_ecm240':{'chunks':1007},
    'p8_ee_ZZ_ecm240':{'chunks':1000},
    
    'wzp6_ee_tautau_ecm240':{'chunks':1000},
    'wzp6_ee_mumu_ecm240':{'chunks':1000},
    'wzp6_ee_ee_Mee_30_150_ecm240':{'chunks':1000},

    'wzp6_ee_tautauH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_tautauH_HZZ_ecm240': {'chunks':100},

    'wzp6_egamma_eZ_Zmumu_ecm240': {'chunks':1000},
    'wzp6_egamma_eZ_Zee_ecm240': {'chunks':1000},
    'wzp6_gammae_eZ_Zmumu_ecm240': {'chunks':1000},
    'wzp6_gammae_eZ_Zee_ecm240': {'chunks':1000},

    'wzp6_gaga_tautau_60_ecm240': {'chunks':1000},
    'wzp6_gaga_mumu_60_ecm240': {'chunks':1000},
    'wzp6_gaga_ee_60_ecm240': {'chunks':1000},

    'wzp6_ee_nuenueZ_ecm240': {'chunks':1000},
    'wzp6_ee_nunuH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_nunuH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_eeH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_eeH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_eeH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_eeH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_eeH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_eeH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_eeH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_mumuH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_mumuH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_bbH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_bbH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_bbH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_bbH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_bbH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_bbH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_bbH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_ccH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_ccH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_ccH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_ccH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_ccH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_ccH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_ccH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_ssH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_ssH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_ssH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_ssH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_ssH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_ssH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_ssH_HZZ_ecm240': {'chunks':100},

    'wzp6_ee_qqH_Htautau_ecm240': {'chunks':100},
    'wzp6_ee_qqH_Hbb_ecm240': {'chunks':100},
    'wzp6_ee_qqH_Hcc_ecm240': {'chunks':100},
    'wzp6_ee_qqH_Hss_ecm240': {'chunks':100},
    'wzp6_ee_qqH_Hgg_ecm240': {'chunks':100},
    'wzp6_ee_qqH_HWW_ecm240': {'chunks':100},
    'wzp6_ee_qqH_HZZ_ecm240': {'chunks':100},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/winter2023/IDEA/"

inputDir = "/ceph/sgiappic/HiggsCP/winter23"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/ecm240/stage2_CMS2/QQ/HH/" 
#outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/stage1_250302/ktN-explicit/QQ/LH/"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

### necessary to run on HTCondor ###
#eosType = "eosuser"

#Optional running on HTCondor, default is False
#runBatch = True

#nCPUS = 6

#Optional batch queue name when running on HTCondor, default is workday
#batchQueue = "longlunch"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
#compGroup = "group_u_CMS.u_zh.users"

## tagging -------------------------------
## latest particle transformer model, trained on 9M jets in winter2023 samples
#model_name = "fccee_flavtagging_edm4hep_wc"

## model files needed for unit testing in CI
#url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
#url_preproc = "{}/{}.json".format(url_model_dir, model_name)
#url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
#model_dir = "/ceph/sgiappic/FCCAnalyses/addons/jet_flavor_tagging/winter2023/wc_pt_7classes_12_04_2023/"
#model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_7classes_12_04_2023/"

#local_preproc = "{}/{}.json".format(model_dir, model_name)
#local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    #else:
    #    urllib.request.urlretrieve(url, os.path.basename(url))
    #    return os.path.basename(url)
    ## this is the old version of the tagger and we don't care about it


#weaver_preproc = get_file_path(url_preproc, local_preproc)
#weaver_model = get_file_path(url_model, local_model)

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
                .Define("reco_mc_index","ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)")

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
                
                ##################
                # Reco particles #
                ##################

        )
        collections = {
            "GenParticles": "Particle",
            "MCRecoMap": "MCRecoAssociations",
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
        collections_smeared = deepcopy(collections)

        df2 = (df2
                .Redefine(collections_smeared["PFParticles"],    ROOT.SmearObjects.SmearedReconstructedParticle(21.7, 11, 1, False),[collections_smeared["PFParticles"], "reco_mc_index", collections_smeared["GenParticles"]])
                .Redefine(collections_smeared["PFParticles"],    ROOT.SmearObjects.SmearedReconstructedParticle(3.5631, 13, 1, False),[collections_smeared["PFParticles"], "reco_mc_index", collections_smeared["GenParticles"]])
                .Redefine(collections_smeared["PFParticles"],    ROOT.SmearObjects.SmearedReconstructedParticle(1.2671, 22, 1, False),[collections_smeared["PFParticles"], "reco_mc_index", collections_smeared["GenParticles"]])
        )
        
                
        df2 = (df2
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
                # .Define("RecoElectronTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
                # .Define("RecoElectronTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
                # .Define("RecoElectronTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") #significance
                # .Define("RecoElectronTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
                # .Define("RecoElectronTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
                # .Define("RecoElectronTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")

                .Define("RecoElectrons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoElectrons)")
                .Define("RecoElectrons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoElectrons_hard, ReconstructedParticles)")
                .Define("RecoElectrons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoElectrons_hard, RecoElectrons_iso)")
                

                # SMEARED ELECTRONS
                .Define("RecoElectrons_smeared",  "ReconstructedParticle::get(Electron0, {})".format(collections_smeared["PFParticles"]))
                .Define("n_RecoElectrons_smeared",  "ReconstructedParticle::get_n(RecoElectrons)") #count how many electrons are in the event in total
                .Define("RecoElectron_e_smeared",      "ReconstructedParticle::get_e(RecoElectrons)")
                .Define("RecoElectron_p_smeared",      "ReconstructedParticle::get_p(RecoElectrons)")
                .Define("RecoElectron_pt_smeared",      "ReconstructedParticle::get_pt(RecoElectrons)")
                .Define("RecoElectron_px_smeared",      "ReconstructedParticle::get_px(RecoElectrons)")
                .Define("RecoElectron_py_smeared",      "ReconstructedParticle::get_py(RecoElectrons)")
                .Define("RecoElectron_pz_smeared",      "ReconstructedParticle::get_pz(RecoElectrons)")
                .Define("RecoElectron_y_smeared",     "ReconstructedParticle::get_y(RecoElectrons)")
                .Define("RecoElectron_eta_smeared",     "ReconstructedParticle::get_eta(RecoElectrons)") #pseudorapidity eta
                .Define("RecoElectron_theta_smeared",   "ReconstructedParticle::get_theta(RecoElectrons)")
                .Define("RecoElectron_phi_smeared",     "ReconstructedParticle::get_phi(RecoElectrons)") #polar angle in the transverse plane phi
                .Define("RecoElectron_charge_smeared",  "ReconstructedParticle::get_charge(RecoElectrons)")
                .Define("RecoElectron_mass_smeared",     "ReconstructedParticle::get_mass(RecoElectrons)")
#                .Define("RecoElectronTrack_absD0_smeared", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoElectrons,EFlowTrack_1))")
#                .Define("RecoElectronTrack_absZ0_smeared", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoElectrons,EFlowTrack_1))")
#                .Define("RecoElectronTrack_absD0sig_smeared", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoElectrons,EFlowTrack_1))") #significance
#                .Define("RecoElectronTrack_absZ0sig_smeared", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoElectrons,EFlowTrack_1))")
#                .Define("RecoElectronTrack_D0cov_smeared", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoElectrons,EFlowTrack_1)") #variance (not sigma)
#                .Define("RecoElectronTrack_Z0cov_smeared", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoElectrons,EFlowTrack_1)")

                .Define("RecoElectrons_hard_smeared", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoElectrons_smeared)")
                .Define("RecoElectrons_iso_smeared",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoElectrons_hard_smeared, {})".format(collections_smeared["PFParticles"]))
                .Define("RecoElectrons_sel_smeared", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoElectrons_hard_smeared, RecoElectrons_iso_smeared)")

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
        )
        df2=(df2
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

                #SMEARED MUONS
                .Define("RecoMuons_smeared",  "ReconstructedParticle::get(Muon0, {})".format(collections_smeared["PFParticles"]))
                .Define("n_RecoMuons_smeared",  "ReconstructedParticle::get_n(RecoMuons)") #count how many muons are in the event in total
                .Define("RecoMuon_e_smeared",      "ReconstructedParticle::get_e(RecoMuons)")
                .Define("RecoMuon_p_smeared",      "ReconstructedParticle::get_p(RecoMuons)")
                .Define("RecoMuon_pt_smeared",      "ReconstructedParticle::get_pt(RecoMuons)")
                .Define("RecoMuon_px_smeared",      "ReconstructedParticle::get_px(RecoMuons)")
                .Define("RecoMuon_py_smeared",      "ReconstructedParticle::get_py(RecoMuons)")
                .Define("RecoMuon_pz_smeared",      "ReconstructedParticle::get_pz(RecoMuons)")
                .Define("RecoMuon_y_smeared",     "ReconstructedParticle::get_y(RecoMuons)")
                .Define("RecoMuon_eta_smeared",     "ReconstructedParticle::get_eta(RecoMuons)") #pseudorapidity eta
                .Define("RecoMuon_theta_smeared",   "ReconstructedParticle::get_theta(RecoMuons)")
                .Define("RecoMuon_phi_smeared",     "ReconstructedParticle::get_phi(RecoMuons)") #polar angle in the transverse plane phi
                .Define("RecoMuon_charge_smeared",  "ReconstructedParticle::get_charge(RecoMuons)")
                .Define("RecoMuon_mass_smeared",     "ReconstructedParticle::get_mass(RecoMuons)")
#                .Define("RecoMuonTrack_absD0_smeared", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons,EFlowTrack_1))")
#                .Define("RecoMuonTrack_absZ0_smeared", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons,EFlowTrack_1))")
#                .Define("RecoMuonTrack_absD0sig_smeared", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons,EFlowTrack_1))") #significance
#                .Define("RecoMuonTrack_absZ0sig_smeared", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons,EFlowTrack_1))")
#                .Define("RecoMuonTrack_D0cov_smeared", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons,EFlowTrack_1)") #variance (not sigma)
#                .Define("RecoMuonTrack_Z0cov_smeared", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons,EFlowTrack_1)")

                .Define("RecoMuons_hard_smeared", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoMuons_smeared)")
                .Define("RecoMuons_iso_smeared",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoMuons_hard_smeared, {})".format(collections_smeared["PFParticles"]))
                .Define("RecoMuons_sel_smeared", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoMuons_hard_smeared, RecoMuons_iso_smeared)")
                
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
                # .Define("RecoMuonTrack_sel_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoMuons_sel,EFlowTrack_1))")
                # .Define("RecoMuonTrack_sel_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoMuons_sel,EFlowTrack_1))")
                # .Define("RecoMuonTrack_sel_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoMuons_sel,EFlowTrack_1))") #significance
                # .Define("RecoMuonTrack_sel_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoMuons_sel,EFlowTrack_1))")
                # .Define("RecoMuonTrack_sel_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoMuons_sel,EFlowTrack_1)") #variance (not sigma)
                # .Define("RecoMuonTrack_sel_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoMuons_sel,EFlowTrack_1)")
        )
        df2=(df2
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
                # .Define("RecoLeptonTrack_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons,EFlowTrack_1))")
                # .Define("RecoLeptonTrack_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons,EFlowTrack_1))")
                # .Define("RecoLeptonTrack_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons,EFlowTrack_1))") #significance
                # .Define("RecoLeptonTrack_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons,EFlowTrack_1))")
                # .Define("RecoLeptonTrack_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoLeptons,EFlowTrack_1)") #variance (not sigma)
                # .Define("RecoLeptonTrack_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoLeptons,EFlowTrack_1)")

                #SMEARED LEPTONS
                .Define("RecoLeptons_smeared", "ReconstructedParticle::merge(RecoElectrons_smeared, RecoMuons_smeared)")
                .Define("n_RecoLeptons_smeared",  "ReconstructedParticle::get_n(RecoLeptons_smeared)") 
                .Define("RecoLepton_e_smeared",      "ReconstructedParticle::get_e(RecoLeptons_smeared)")
                .Define("RecoLepton_p_smeared",      "ReconstructedParticle::get_p(RecoLeptons_smeared)")
                .Define("RecoLepton_pt_smeared",      "ReconstructedParticle::get_pt(RecoLeptons_smeared)")
                .Define("RecoLepton_px_smeared",      "ReconstructedParticle::get_px(RecoLeptons_smeared)")
                .Define("RecoLepton_py_smeared",      "ReconstructedParticle::get_py(RecoLeptons_smeared)")
                .Define("RecoLepton_pz_smeared",      "ReconstructedParticle::get_pz(RecoLeptons_smeared)")
                .Define("RecoLepton_y_smeared",      "ReconstructedParticle::get_y(RecoLeptons_smeared)")
                .Define("RecoLepton_eta_smeared",     "ReconstructedParticle::get_eta(RecoLeptons_smeared)") #pseudorapidity eta
                .Define("RecoLepton_theta_smeared",   "ReconstructedParticle::get_theta(RecoLeptons_smeared)")
                .Define("RecoLepton_phi_smeared",     "ReconstructedParticle::get_phi(RecoLeptons_smeared)") #polar angle in the transverse plane phi
                .Define("RecoLepton_charge_smeared",  "ReconstructedParticle::get_charge(RecoLeptons_smeared)")
                .Define("RecoLepton_mass_smeared",     "ReconstructedParticle::get_mass(RecoLeptons_smeared)")

                .Define("RecoLeptons_sel_smeared", "ReconstructedParticle::merge(RecoElectrons_sel_smeared, RecoMuons_sel_smeared)")

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
                # .Define("RecoLeptonTrack_sel_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(RecoLeptons_sel,EFlowTrack_1))")
                # .Define("RecoLeptonTrack_sel_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(RecoLeptons_sel,EFlowTrack_1))")
                # .Define("RecoLeptonTrack_sel_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoLeptons_sel,EFlowTrack_1))") #significance
                # .Define("RecoLeptonTrack_sel_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoLeptons_sel,EFlowTrack_1))")
                # .Define("RecoLeptonTrack_sel_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(RecoLeptons_sel,EFlowTrack_1)") #variance (not sigma)
                # .Define("RecoLeptonTrack_sel_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(RecoLeptons_sel,EFlowTrack_1)")

                #PHOTONS
                .Alias("Photon0", "Photon#0.index") 
                .Define("RecoPhotons",  "ReconstructedParticle::get(Photon0, {})".format(collections_smeared["PFParticles"]))
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
                .Define("RecoEmiss", "FCCAnalyses::ZHfunctions::missingEnergy(240, {})".format(collections_smeared["PFParticles"])) #ecm 
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

                # find leading lepton and remove it from the clustering so it's not double counting, may not be the best strategy but what else
                .Define("LeadingLepton",        "FCCAnalyses::ZHfunctions::Find_Leading(RecoLeptons_sel)")
                .Define("n_LeadingLepton",      "ReconstructedParticle::get_n(LeadingLepton)")
                .Define("LeadingLepton_e",      "ReconstructedParticle::get_e(LeadingLepton)")
                .Define("LeadingLepton_p",      "ReconstructedParticle::get_p(LeadingLepton)")
                .Define("LeadingLepton_pt",      "ReconstructedParticle::get_pt(LeadingLepton)")
                .Define("LeadingLepton_px",      "ReconstructedParticle::get_px(LeadingLepton)")
                .Define("LeadingLepton_py",      "ReconstructedParticle::get_py(LeadingLepton)")
                .Define("LeadingLepton_pz",      "ReconstructedParticle::get_pz(LeadingLepton)")
                .Define("LeadingLepton_y",      "ReconstructedParticle::get_y(LeadingLepton)")
                .Define("LeadingLepton_eta",     "ReconstructedParticle::get_eta(LeadingLepton)") #pseudorapidity eta
                .Define("LeadingLepton_theta",   "ReconstructedParticle::get_theta(LeadingLepton)")
                .Define("LeadingLepton_phi",     "ReconstructedParticle::get_phi(LeadingLepton)") #polar angle in the transverse plane phi
                .Define("LeadingLepton_charge",  "ReconstructedParticle::get_charge(LeadingLepton)")
                .Define("LeadingLepton_mass",     "ReconstructedParticle::get_mass(LeadingLepton)")
                # .Define("RecoLeadingLepton_absD0", "return abs(ReconstructedParticle2Track::getRP2TRK_D0(LeadingLepton,EFlowTrack_1))")
                # .Define("RecoLeadingLepton_absZ0", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0(LeadingLepton,EFlowTrack_1))")
                # .Define("RecoLeadingLepton_absD0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_D0_sig(LeadingLepton,EFlowTrack_1))") #significance
                # .Define("RecoLeadingLepton_absZ0sig", "return abs(ReconstructedParticle2Track::getRP2TRK_Z0_sig(LeadingLepton,EFlowTrack_1))")
                # .Define("RecoLeadingLepton_D0cov", "ReconstructedParticle2Track::getRP2TRK_D0_cov(LeadingLepton,EFlowTrack_1)") #variance (not sigma)
                # .Define("RecoLeadingLepton_Z0cov", "ReconstructedParticle2Track::getRP2TRK_Z0_cov(LeadingLepton,EFlowTrack_1)")

                # find leading lepton and remove it from the clustering so it's not double counting, may not be the best strategy but what else
                .Define("LeadingLepton_smeared",        "FCCAnalyses::ZHfunctions::Find_Leading(RecoLeptons_sel_smeared)")
                .Define("n_LeadingLepton_smeared",      "ReconstructedParticle::get_n(LeadingLepton_smeared)")
                .Define("LeadingLepton_e_smeared",      "ReconstructedParticle::get_e(LeadingLepton_smeared)")
                .Define("LeadingLepton_p_smeared",      "ReconstructedParticle::get_p(LeadingLepton_smeared)")
                .Define("LeadingLepton_pt_smeared",      "ReconstructedParticle::get_pt(LeadingLepton_smeared)")
                .Define("LeadingLepton_px_smeared",      "ReconstructedParticle::get_px(LeadingLepton_smeared)")
                .Define("LeadingLepton_py_smeared",      "ReconstructedParticle::get_py(LeadingLepton_smeared)")
                .Define("LeadingLepton_pz_smeared",      "ReconstructedParticle::get_pz(LeadingLepton_smeared)")
                .Define("LeadingLepton_y_smeared",      "ReconstructedParticle::get_y(LeadingLepton_smeared)")
                .Define("LeadingLepton_eta_smeared",     "ReconstructedParticle::get_eta(LeadingLepton_smeared)") #pseudorapidity eta
                .Define("LeadingLepton_theta_smeared",   "ReconstructedParticle::get_theta(LeadingLepton_smeared)")
                .Define("LeadingLepton_phi_smeared",     "ReconstructedParticle::get_phi(LeadingLepton_smeared)") #polar angle in the transverse plane phi
                .Define("LeadingLepton_charge_smeared",  "ReconstructedParticle::get_charge(LeadingLepton_smeared)")
                .Define("LeadingLepton_mass_smeared",     "ReconstructedParticle::get_mass(LeadingLepton_smeared)")

                .Define("ReconstructedParticlesJET",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,LeadingLepton)")
            
        )
        #### tagging
        
        # global jetClusteringHelper_R5
        # global jetFlavourHelper_R5
        # ## define jet and run clustering parameters
        # ## name of collections in EDM root files
        # collections = {
        #     "GenParticles": "Particle",
        #     "PFParticles": "ReconstructedParticlesJET",
        #     "PFTracks": "EFlowTrack",
        #     "PFPhotons": "EFlowPhoton",
        #     "PFNeutralHadrons": "EFlowNeutralHadron",
        #     "TrackState": "EFlowTrack_1",
        #     "TrackerHits": "TrackerHits",
        #     "CalorimeterHits": "CalorimeterHits",
        #     "dNdx": "EFlowTrack_2",
        #     "PathLength": "EFlowTrack_L",
        #     "Bz": "magFieldBz",
        # }
        # #INCLUSIVE R=0.5
        # ## def __init__(self, coll, njets, tag="")
        # jetClusteringHelper_R5  = InclusiveJetClusteringHelper(
        #     collections["PFParticles"], 0.5, 2, "R5"
        # )
        # df2 = jetClusteringHelper_R5.define(df2)

        # ## define jet flavour tagging parameters
        # jetFlavourHelper_R5 = JetFlavourHelper(
        #     collections,
        #     jetClusteringHelper_R5.jets,
        #     jetClusteringHelper_R5.constituents,
        #     "R5",
        # )
        # ## define observables for tagger
        # df2 = jetFlavourHelper_R5.define(df2)

        # ## tagger inference
        # df2 = jetFlavourHelper_R5.inference(weaver_preproc, weaver_model, df2)

        # df2 = (df2
        #         .Define("TagJet_R5_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_p",           "JetClusteringUtils::get_p({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_pt",           "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_theta",          "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_e",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_R5.jets))
        #         .Define("TagJet_R5_charge",         "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_R5.constituents))
        #         .Define("TagJet_R5_flavor",        "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_R5.jets))
        #         .Define("n_TagJet_R5_constituents",        "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_R5.constituents))
        #         .Define("n_TagJet_R5_charged_constituents",        "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_R5.constituents))
        #         .Define("n_TagJet_R5_neutral_constituents",        "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_R5.constituents))
        #         .Define("n_TagJet_R5",           "return TagJet_R5_e.size()")
        #         .Define("TagJet_R5_cleanup",       "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_R5.constituents))

        #         .Define("TagJet_R5_isG",    "recojet_isG_R5")
        #         .Define("TagJet_R5_isU",    "recojet_isU_R5")
        #         .Define("TagJet_R5_isD",    "recojet_isD_R5")
        #         .Define("TagJet_R5_isS",    "recojet_isS_R5")
        #         .Define("TagJet_R5_isC",    "recojet_isC_R5")
        #         .Define("TagJet_R5_isB",    "recojet_isB_R5")
        #         .Define("TagJet_R5_isTAU",    "recojet_isTAU_R5")

        #         .Define("TauFromJet_R5", "FCCAnalyses::ZHfunctions::findTauInJet({})".format(jetClusteringHelper_R5.constituents)) 
        #         .Define("TauFromJet_R5_type_sel","ReconstructedParticle::get_type(TauFromJet_R5)")
        #         .Define("TauFromJet_R5_tau", "TauFromJet_R5[TauFromJet_R5_type_sel>=0]") 
        #         .Define("TauFromJet_R5_p","ReconstructedParticle::get_p(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_pt","ReconstructedParticle::get_pt(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_px","ReconstructedParticle::get_px(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_py","ReconstructedParticle::get_py(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_pz","ReconstructedParticle::get_pz(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_theta","ReconstructedParticle::get_theta(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_phi","ReconstructedParticle::get_phi(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_eta","ReconstructedParticle::get_eta(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_y","ReconstructedParticle::get_y(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_e","ReconstructedParticle::get_e(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_charge","ReconstructedParticle::get_charge(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_type","ReconstructedParticle::get_type(TauFromJet_R5_tau)")
        #         .Define("TauFromJet_R5_mass","ReconstructedParticle::get_mass(TauFromJet_R5_tau)")
        #         .Define("n_TauFromJet_R5","TauFromJet_R5_pt.size()")

        #         .Define("TagJet_R5_sel_e",      "TagJet_R5_e[TauFromJet_R5_type_sel<0 ]")
        #         .Define("TagJet_R5_sel_p",      "TagJet_R5_p[TauFromJet_R5_type_sel<0 ]")
        #         .Define("TagJet_R5_sel_pt",      "TagJet_R5_pt[TauFromJet_R5_type_sel<0 ]")
        #         .Define("TagJet_R5_sel_px",      "TagJet_R5_px[TauFromJet_R5_type_sel<0 ]")
        #         .Define("TagJet_R5_sel_py",      "TagJet_R5_py[TauFromJet_R5_type_sel<0 ]")
        #         .Define("TagJet_R5_sel_pz",      "TagJet_R5_pz[TauFromJet_R5_type_sel<0 ]")
		#         .Define("TagJet_R5_sel_eta",     "TagJet_R5_eta[TauFromJet_R5_type_sel<0 ]")
        #         .Define("TagJet_R5_sel_theta",   "TagJet_R5_theta[TauFromJet_R5_type_sel<0 ]")
		#         .Define("TagJet_R5_sel_phi",     "TagJet_R5_phi[TauFromJet_R5_type_sel<0 ]")
        #         .Define("TagJet_R5_sel_mass",      "TagJet_R5_mass[TauFromJet_R5_type_sel<0 ]")
        #         .Define("n_TagJet_R5_sel", "TagJet_R5_sel_e.size()")
        # )

        #EXCLUSIVE 2 JETS=
        jetClusteringHelper_kt3  = ExclusiveJetClusteringHelper(
            collections["PFParticles"], 3, "kt3"
        )
        df2 = jetClusteringHelper_kt3.define(df2)

        ## define jet flavour tagging parameters
        jetFlavourHelper_kt3 = JetFlavourHelper(
            collections,
            jetClusteringHelper_kt3.jets,
            jetClusteringHelper_kt3.constituents,
            "kt3",
        )
        ## define observables for tagger
        df2 = jetFlavourHelper_kt3.define(df2)

        ## tagger inference
        #f2 = jetFlavourHelper_kt3.inference(weaver_preproc, weaver_model, df2)

        df2 = (df2
                .Define("TagJet_kt3_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_p",           "JetClusteringUtils::get_p({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_pt",           "JetClusteringUtils::get_pt({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_theta",          "JetClusteringUtils::get_theta({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_e",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt3.jets))
                .Define("TagJet_kt3_charge",         "JetConstituentsUtils::get_charge_constituents({})".format(jetClusteringHelper_kt3.constituents))
                .Define("TagJet_kt3_flavor",        "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt3.jets))
                .Define("n_TagJet_kt3_constituents",        "JetConstituentsUtils::get_n_constituents({})".format(jetClusteringHelper_kt3.constituents))
                .Define("n_TagJet_kt3_charged_constituents",        "JetConstituentsUtils::get_ncharged_constituents({})".format(jetClusteringHelper_kt3.constituents))
                .Define("n_TagJet_kt3_neutral_constituents",        "JetConstituentsUtils::get_nneutral_constituents({})".format(jetClusteringHelper_kt3.constituents))
                .Define("n_TagJet_kt3",           "return int(TagJet_kt3_flavor.size())")
                .Define("TagJet_kt3_cleanup",       "JetConstituentsUtils::cleanup_taggedjet({})".format(jetClusteringHelper_kt3.constituents))

                # .Define("TagJet_kt3_isG",    "recojet_isG_kt3")
                # .Define("TagJet_kt3_isU",    "recojet_isU_kt3")
                # .Define("TagJet_kt3_isD",    "recojet_isD_kt3")
                # .Define("TagJet_kt3_isS",    "recojet_isS_kt3")
                # .Define("TagJet_kt3_isC",    "recojet_isC_kt3")
                # .Define("TagJet_kt3_isB",    "recojet_isB_kt3")
                # .Define("TagJet_kt3_isTAU",    "recojet_isTAU_kt3")

                .Define("TauFromJet_kt3", "FCCAnalyses::ZHfunctions::findTauInJet_smearing({},Particle,21.7,3.5631, 1.2671, 18.3)".format(jetClusteringHelper_kt3.constituents)) 
                .Define("TauFromJet_kt3_type_sel","ReconstructedParticle::get_type(TauFromJet_kt3)")
                .Define("TauFromJet_kt3_tau", "TauFromJet_kt3[TauFromJet_kt3_type_sel>=0]") 
                .Define("TauFromJet_kt3_p","ReconstructedParticle::get_p(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_pt","ReconstructedParticle::get_pt(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_px","ReconstructedParticle::get_px(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_py","ReconstructedParticle::get_py(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_pz","ReconstructedParticle::get_pz(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_theta","ReconstructedParticle::get_theta(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_phi","ReconstructedParticle::get_phi(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_eta","ReconstructedParticle::get_eta(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_y","ReconstructedParticle::get_y(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_e","ReconstructedParticle::get_e(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_charge","ReconstructedParticle::get_charge(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_type","ReconstructedParticle::get_type(TauFromJet_kt3_tau)")
                .Define("TauFromJet_kt3_mass","ReconstructedParticle::get_mass(TauFromJet_kt3_tau)")
                .Define("n_TauFromJet_kt3","TauFromJet_kt3_pt.size()")

                .Define("TagJet_kt3_sel_e",      "TagJet_kt3_e[TauFromJet_kt3_type_sel<0]")
                .Define("TagJet_kt3_sel_p",      "TagJet_kt3_p[TauFromJet_kt3_type_sel<0]")
                .Define("TagJet_kt3_sel_pt",      "TagJet_kt3_pt[TauFromJet_kt3_type_sel<0]")
                .Define("TagJet_kt3_sel_px",      "TagJet_kt3_px[TauFromJet_kt3_type_sel<0]")
                .Define("TagJet_kt3_sel_py",      "TagJet_kt3_py[TauFromJet_kt3_type_sel<0]")
                .Define("TagJet_kt3_sel_pz",      "TagJet_kt3_pz[TauFromJet_kt3_type_sel<0]")
		        .Define("TagJet_kt3_sel_eta",     "TagJet_kt3_eta[TauFromJet_kt3_type_sel<0]")
                .Define("TagJet_kt3_sel_theta",   "TagJet_kt3_theta[TauFromJet_kt3_type_sel<0]")
		        .Define("TagJet_kt3_sel_phi",     "TagJet_kt3_phi[TauFromJet_kt3_type_sel<0]")
                .Define("TagJet_kt3_sel_mass",      "TagJet_kt3_mass[TauFromJet_kt3_type_sel<0]")
                .Define("n_TagJet_kt3_sel", "TagJet_kt3_sel_e.size()")
                .Define("jet_p4",               "FCCAnalyses::ZHfunctions::build_p4(TagJet_kt3_sel_px, TagJet_kt3_sel_py, TagJet_kt3_sel_pz, TagJet_kt3_sel_e)")
                .Define("smeared_jet_p4",       "FCCAnalyses::ZHfunctions::smear_jet(jet_p4, 25.2, 6.96, 125.)")

        )

        df2 = (df2

                # ### now i want to study the thadronic tau reconstruction with the function and the jet tagger by comparing it to the gen info for taus decaying not to electrons or muons

                # .Define("GenTau_el",       "FCCAnalyses::MCParticle::sel_daughterID(-11, false, true)(HiggsGenTau,Particle,Particle1)")
                # .Define("GenTau_had",       "FCCAnalyses::MCParticle::sel_daughterID(-13, false, true)(GenTau_el,Particle,Particle1)")
                # .Define("HadGenTau_eta",    "FCCAnalyses::MCParticle::get_eta(GenTau_had)")
                # .Define("HadGenTau_phi",    "FCCAnalyses::MCParticle::get_phi(GenTau_had)")
                # .Define("n_GenTau_had",     "HadGenTau_eta.size()")

                # .Define("TauTag_eta_R5",      "TagJet_R5_eta[TagJet_R5_isTAU>0.5 ]")
                # .Define("TauTag_phi_R5",      "TagJet_R5_phi[TagJet_R5_isTAU>0.5 ]")
                # .Define("TauTag_R5_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_R5, HadGenTau_phi, TauTag_eta_R5, HadGenTau_eta, 0.2)")
                # .Define("n_TauTag_R5_match",          "if (n_GenTau_had>0) return TauTag_R5_idx.size(); else return TauTag_eta_R5.size();")
                # .Define("TauTag_eta_R5mass",      "TagJet_R5_eta[TagJet_R5_isTAU>0.5  && TagJet_R5_mass<3]")
                # .Define("TauTag_phi_R5mass",      "TagJet_R5_phi[TagJet_R5_isTAU>0.5  && TagJet_R5_mass<3]")
                # .Define("TauTag_R5mass_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_R5mass, HadGenTau_phi, TauTag_eta_R5mass, HadGenTau_eta, 0.2)")
                # .Define("n_TauTag_R5mass_match",          "if (n_GenTau_had>0) return TauTag_R5mass_idx.size(); else return TauTag_eta_R5mass.size();")

                # .Define("TauTag_eta_kt3",      "TagJet_kt3_eta[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_phi_kt3",      "TagJet_kt3_phi[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_kt3_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_kt3, HadGenTau_phi, TauTag_eta_kt3, HadGenTau_eta, 0.2)")
                # .Define("n_TauTag_kt3_match",          "if (n_GenTau_had>0) return TauTag_kt3_idx.size(); else return TauTag_eta_kt3.size();")
                # .Define("TauTag_eta_kt3mass",      "TagJet_kt3_eta[TagJet_kt3_isTAU>0.5  && TagJet_kt3_mass<3]")
                # .Define("TauTag_phi_kt3mass",      "TagJet_kt3_phi[TagJet_kt3_isTAU>0.5  && TagJet_kt3_mass<3]")
                # .Define("TauTag_kt3mass_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauTag_phi_kt3mass, HadGenTau_phi, TauTag_eta_kt3mass, HadGenTau_eta, 0.2)")
                # .Define("n_TauTag_kt3mass_match",          "if (n_GenTau_had>0) return TauTag_kt3mass_idx.size(); else return TauTag_eta_kt3mass.size();")

                # .Define("TauFromJet_R5_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauFromJet_R5_phi, HadGenTau_phi, TauFromJet_R5_eta, HadGenTau_eta, 0.2)")
                # .Define("n_TauFromJet_R5_match",          "if (n_GenTau_had>0) return TauFromJet_R5_idx.size(); else return n_TauFromJet_R5;")

                # .Define("TauFromJet_kt3_idx",       "FCCAnalyses::ZHfunctions::deltaR_sel_idx_v2(TauFromJet_kt3_phi, HadGenTau_phi, TauFromJet_kt3_eta, HadGenTau_eta, 0.2)")
                # .Define("n_TauFromJet_kt3_match",          "if (n_GenTau_had>0) return TauFromJet_kt3_idx.size(); else return n_TauFromJet_kt3;")

                # .Define("n_events_R5tag",       "if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauTag_R5_match && n_GenTau_had==0) return 0; else return -1;")
                # .Define("n_events_R5masstag",       "if (n_GenTau_had==n_TauTag_R5mass_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_R5mass_match && n_GenTau_had==2) return 2;  else if (n_GenTau_had==n_TauTag_R5mass_match && n_GenTau_had==0) return 0; else return -1;")
                # .Define("n_events_R5excl",       "if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauFromJet_R5_match && n_GenTau_had==0) return 0; else return -1;")

                # .Define("n_events_kt3tag",       "if (n_GenTau_had==n_TauTag_kt3_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_kt3_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauTag_kt3_match && n_GenTau_had==0) return 0; else return -1;")
                # .Define("n_events_kt3masstag",       "if (n_GenTau_had==n_TauTag_kt3mass_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauTag_kt3mass_match && n_GenTau_had==2) return 2;  else if (n_GenTau_had==n_TauTag_kt3mass_match && n_GenTau_had==0) return 0; else return -1;")
                # .Define("n_events_kt3excl",       "if (n_GenTau_had==n_TauFromJet_kt3_match && n_GenTau_had==1) return 1; else if (n_GenTau_had==n_TauFromJet_kt3_match && n_GenTau_had==2) return 2; else if (n_GenTau_had==n_TauFromJet_kt3_match && n_GenTau_had==0) return 0; else return -1;")

                # ##########################
                # ###### Ex. stage2 ########
                # ##########################

                # ### to find already made functions, this is where they are or where they can be added instead of writing them here
                # ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

                # ### defining filters for one sel lepotons, two no tau jets, one tau jet

                # ### when working with Z jets, remember to use the Leptons_sel class because they are the ones not in the jets
                # ### when working with tau jets it does not matter since the tau jets don't have any lepton in them so there is no confusion 

                # .Define("TauTag_px",      "TagJet_kt3_px[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_py",      "TagJet_kt3_py[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_pz",      "TagJet_kt3_pz[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_pt",      "TagJet_kt3_pt[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_p",      "TagJet_kt3_p[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_e",      "TagJet_kt3_e[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_phi",      "TagJet_kt3_phi[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_eta",      "TagJet_kt3_eta[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_theta",      "TagJet_kt3_theta[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_charge",      "TagJet_kt3_charge[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_mass",      "TagJet_kt3_mass[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_isG",      "TagJet_kt3_isG[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_isU",      "TagJet_kt3_isU[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_isD",      "TagJet_kt3_isD[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_isS",      "TagJet_kt3_isS[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_isC",      "TagJet_kt3_isC[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_isB",      "TagJet_kt3_isB[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_isTAU",      "TagJet_kt3_isTAU[TagJet_kt3_isTAU>0.5]")
                # .Define("TauTag_flavor",      "TagJet_kt3_flavor[TagJet_kt3_isTAU>0.5]")
                # .Define("n_TauTag_constituents",        "n_TagJet_kt3_constituents[TagJet_kt3_isTAU>0.5]")
                # .Define("n_TauTag_charged_constituents",        "n_TagJet_kt3_charged_constituents[TagJet_kt3_isTAU>0.5]")
                # .Define("n_TauTag_neutral_constituents",        "n_TagJet_kt3_neutral_constituents[TagJet_kt3_isTAU>0.5]")
                # .Define("n_TauTag",          "TauTag_px.size()")

                # .Define("QuarkTag_px",      "TagJet_kt3_px[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_py",      "TagJet_kt3_py[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_pz",      "TagJet_kt3_pz[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_pt",      "TagJet_kt3_pt[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_p",      "TagJet_kt3_p[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_e",      "TagJet_kt3_e[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_phi",      "TagJet_kt3_phi[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_eta",      "TagJet_kt3_eta[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_theta",      "TagJet_kt3_theta[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_charge",      "TagJet_kt3_charge[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_mass",      "TagJet_kt3_mass[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_isG",      "TagJet_kt3_isG[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_isU",      "TagJet_kt3_isU[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_isD",      "TagJet_kt3_isD[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_isS",      "TagJet_kt3_isS[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_isC",      "TagJet_kt3_isC[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_isB",      "TagJet_kt3_isB[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_isTAU",      "TagJet_kt3_isTAU[TagJet_kt3_isTAU<=0.5]")
                # .Define("QuarkTag_flavor",      "TagJet_kt3_flavor[TagJet_kt3_isTAU<=0.5]")
                # .Define("n_QuarkTag_constituents",        "n_TagJet_kt3_constituents[TagJet_kt3_isTAU<=0.5]")
                # .Define("n_QuarkTag_charged_constituents",        "n_TagJet_kt3_charged_constituents[TagJet_kt3_isTAU<=0.5]")
                # .Define("n_QuarkTag_neutral_constituents",        "n_TagJet_kt3_neutral_constituents[TagJet_kt3_isTAU<=0.5]")
                # .Define("n_QuarkTag",     "QuarkTag_charge.size()")

                ###########################
                ######### FILTER ##########
                ###########################

                .Filter("n_TauFromJet_kt3==1 && n_TagJet_kt3_sel==2 && n_RecoLeptons_sel==1")
                .Filter("(TauFromJet_kt3_charge.at(0) + LeadingLepton_charge_smeared.at(0))==0") 

                ################################

                .Define("RecoZ1_p4",      "smeared_jet_p4.at(0)")
                .Define("RecoZ2_p4",      "smeared_jet_p4.at(1)")
                
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

                .Define("RecoTau1_p4",      "TLorentzVector(LeadingLepton_px_smeared.at(0), LeadingLepton_py_smeared.at(0), LeadingLepton_pz_smeared.at(0), LeadingLepton_e_smeared.at(0))")
                .Define("RecoTau2_p4",      "TLorentzVector(TauFromJet_kt3_px.at(0), TauFromJet_kt3_py.at(0), TauFromJet_kt3_pz.at(0), TauFromJet_kt3_e.at(0))")
                .Define("RecoTau1_type",        "if (LeadingLepton_mass_smeared.at(0)<0.05) return float(-0.11); else return float(-0.13);")
                .Define("RecoTau2_type",        "float(TauFromJet_kt3_type.at(0))")

                .Define("TauLepton_type",        "if (LeadingLepton_mass_smeared.at(0)<0.05) return float(-0.11); else return float(-0.13);")
                .Define("TauHadron_type",        "float(TauFromJet_kt3_type.at(0))")

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

                .Define("TauP_p4","if (TauFromJet_kt3_charge.at(0)==1) return RecoTau2_p4; else return RecoTau1_p4;")
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
                .Define("TauP_type","if (TauFromJet_kt3_charge.at(0)==1) return RecoTau2_type; else return RecoTau1_type;")

                .Define("TauM_p4",       "if (TauFromJet_kt3_charge.at(0)==1) return RecoTau1_p4; else return RecoTau2_p4;")
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
                .Define("TauM_type","if (TauFromJet_kt3_charge.at(0)==1) return RecoTau1_type; else return RecoTau2_type;")

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

                .Define("Total_p4",     "TLorentzVector(0.,0.,1.,240.)")
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
            # "RecoElectronTrack_absD0",
            # "RecoElectronTrack_absZ0",
            # "RecoElectronTrack_absD0sig",
            # "RecoElectronTrack_absZ0sig",
            # "RecoElectronTrack_D0cov",
            # "RecoElectronTrack_Z0cov",

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
            # "RecoElectronTrack_sel_absD0",
            # "RecoElectronTrack_sel_absZ0",
            # "RecoElectronTrack_sel_absD0sig",
            # "RecoElectronTrack_sel_absZ0sig",
            # "RecoElectronTrack_sel_D0cov",
            # "RecoElectronTrack_sel_Z0cov",

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
            # "RecoMuonTrack_absD0",
            # "RecoMuonTrack_absZ0",
            # "RecoMuonTrack_absD0sig",
            # "RecoMuonTrack_absZ0sig",
            # "RecoMuonTrack_D0cov",
            # "RecoMuonTrack_Z0cov",

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
            # "RecoMuonTrack_sel_absD0",
            # "RecoMuonTrack_sel_absZ0",
            # "RecoMuonTrack_sel_absD0sig",
            # "RecoMuonTrack_sel_absZ0sig",
            # "RecoMuonTrack_sel_D0cov",
            # "RecoMuonTrack_sel_Z0cov",

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
            # "RecoLeptonTrack_absD0",
            # "RecoLeptonTrack_absZ0",
            # "RecoLeptonTrack_absD0sig",
            # "RecoLeptonTrack_absZ0sig",
            # "RecoLeptonTrack_D0cov",
            # "RecoLeptonTrack_Z0cov",

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
            # "RecoLeptonTrack_sel_absD0",
            # "RecoLeptonTrack_sel_absZ0",
            # "RecoLeptonTrack_sel_absD0sig",
            # "RecoLeptonTrack_sel_absZ0sig",
            # "RecoLeptonTrack_sel_D0cov",
            # "RecoLeptonTrack_sel_Z0cov",

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
            # "RecoLeadingLepton_absD0",
            # "RecoLeadingLepton_absZ0",
            # "RecoLeadingLepton_absD0sig",
            # "RecoLeadingLepton_absZ0sig",
            # "RecoLeadingLepton_D0cov",
            # "RecoLeadingLepton_Z0cov",

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

            # "TagJet_R5_px", 
            # "TagJet_R5_py",    
            # "TagJet_R5_pz",      
            # "TagJet_R5_p",  
            # "TagJet_R5_pt",    
            # "TagJet_R5_phi", 
            # "TagJet_R5_eta",     
            # "TagJet_R5_theta",          
            # "TagJet_R5_e",     
            # "TagJet_R5_mass",        
            # "TagJet_R5_charge",       
            # "TagJet_R5_flavor", 
            # "n_TagJet_R5_constituents",   
            # "n_TagJet_R5_charged_constituents",   
            # "n_TagJet_R5_neutral_constituents",   
            # "n_TagJet_R5",    
            # "TagJet_R5_cleanup",        

            # "TagJet_R5_isG",  
            # "TagJet_R5_isU",
            # "TagJet_R5_isD",   
            # "TagJet_R5_isS",  
            # "TagJet_R5_isC",
            # "TagJet_R5_isB",  
            # "TagJet_R5_isTAU",

            # "TauFromJet_R5_p",
            # "TauFromJet_R5_pt",
            # "TauFromJet_R5_px",
            # "TauFromJet_R5_py",
            # "TauFromJet_R5_pz",
            # "TauFromJet_R5_theta",
            # "TauFromJet_R5_phi",
            # "TauFromJet_R5_e",
            # "TauFromJet_R5_eta",
            # "TauFromJet_R5_y",
            # "TauFromJet_R5_charge",
            # "TauFromJet_R5_type",
            # "TauFromJet_R5_mass",
            # "n_TauFromJet_R5",

            # "TagJet_R5_sel_e",     
            # "TagJet_R5_sel_p",     
            # "TagJet_R5_sel_pt",     
            # "TagJet_R5_sel_px",   
            # "TagJet_R5_sel_py",   
            # "TagJet_R5_sel_pz",     
            # "TagJet_R5_sel_eta",    
            # "TagJet_R5_sel_theta",   
            # "TagJet_R5_sel_phi",     
            # "TagJet_R5_sel_mass",      
            # "n_TagJet_R5_sel", 

            "TagJet_kt3_px", 
            "TagJet_kt3_py",    
            "TagJet_kt3_pz",      
            "TagJet_kt3_p",  
            "TagJet_kt3_pt",    
            "TagJet_kt3_phi", 
            "TagJet_kt3_eta",     
            "TagJet_kt3_theta",          
            "TagJet_kt3_e",     
            "TagJet_kt3_mass",        
            "TagJet_kt3_charge",       
            "TagJet_kt3_flavor", 
            "n_TagJet_kt3_constituents",   
            "n_TagJet_kt3_charged_constituents",   
            "n_TagJet_kt3_neutral_constituents",   
            "n_TagJet_kt3",          

            # "TagJet_kt3_isG",  
            # "TagJet_kt3_isU",
            # "TagJet_kt3_isD",   
            # "TagJet_kt3_isS",  
            # "TagJet_kt3_isC",
            # "TagJet_kt3_isB",  
            # "TagJet_kt3_isTAU",

            "TauFromJet_kt3_p",
            "TauFromJet_kt3_pt",
            "TauFromJet_kt3_px",
            "TauFromJet_kt3_py",
            "TauFromJet_kt3_pz",
            "TauFromJet_kt3_theta",
            "TauFromJet_kt3_phi",
            "TauFromJet_kt3_e",
            "TauFromJet_kt3_eta",
            "TauFromJet_kt3_y",
            "TauFromJet_kt3_charge",
            "TauFromJet_kt3_type",
            "TauFromJet_kt3_mass",
            "n_TauFromJet_kt3",

            "TagJet_kt3_sel_e",     
            "TagJet_kt3_sel_p",     
            "TagJet_kt3_sel_pt",     
            "TagJet_kt3_sel_px",   
            "TagJet_kt3_sel_py",   
            "TagJet_kt3_sel_pz",     
            "TagJet_kt3_sel_eta",    
            "TagJet_kt3_sel_theta",   
            "TagJet_kt3_sel_phi",     
            "TagJet_kt3_sel_mass",      
            "n_TagJet_kt3_sel",

            # "n_GenTau_had", 
            # "n_TauTag_R5_match",  
            # "n_TauTag_R5mass_match",
            # "n_events_R5tag",  
            # "n_events_R5masstag",
            # "n_events_R5excl",

            # "n_TauTag_kt3_match",  
            # "n_TauTag_kt3mass_match",
            # "n_events_kt3tag",  
            # "n_events_kt3masstag",
            # "n_events_kt3excl",  

        ]
        #complex variables added here at stage2
        branchList += [
            # "TauTag_px", 
            # "TauTag_py",    
            # "TauTag_pz",      
            # "TauTag_p",  
            # "TauTag_pt",    
            # "TauTag_phi", 
            # "TauTag_eta",     
            # "TauTag_theta",          
            # "TauTag_e",     
            # "TauTag_mass",        
            # "TauTag_charge",       
            # "TauTag_flavor",       
            # "n_TauTag",          
            # "TauTag_isG",  
            # "TauTag_isU",
            # "TauTag_isD",   
            # "TauTag_isS",  
            # "TauTag_isC",
            # "TauTag_isB",  
            # "TauTag_isTAU",

            # "QuarkTag_px", 
            # "QuarkTag_py",    
            # "QuarkTag_pz",      
            # "QuarkTag_p",  
            # "QuarkTag_pt",    
            # "QuarkTag_phi", 
            # "QuarkTag_eta",     
            # "QuarkTag_theta",          
            # "QuarkTag_e",     
            # "QuarkTag_mass",        
            # "QuarkTag_charge",       
            # "QuarkTag_flavor",       
            # "n_QuarkTag",          
            # "QuarkTag_isG",  
            # "QuarkTag_isU",
            # "QuarkTag_isD",   
            # "QuarkTag_isS",  
            # "QuarkTag_isC",
            # "QuarkTag_isB",  
            # "QuarkTag_isTAU",

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