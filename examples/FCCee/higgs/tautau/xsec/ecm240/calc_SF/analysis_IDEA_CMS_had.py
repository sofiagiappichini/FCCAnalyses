import os, copy # tagging
import ROOT
import urllib.request
from copy import deepcopy

processList = {
    'IDEA_events_002119867': {},
    'CMS_Phase2_events_002119867': {},
    'CMS_Phase1_events_002119867': {},
}

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/winter2023/IDEA/"

inputDir = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/ecm240/EDM4HEP/wzp6_ee_nunuH_Hbb_ecm240/"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "/ceph/awiedl/FCCee/HiggsCP/detector_studies/stage1_res/had/"
#outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/"

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
#compGroup = "group_u_FCC.local_gen"

## tagging -------------------------------
## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = "/ceph/sgiappic/FCCAnalyses/addons/jet_flavor_tagging/winter2023/wc_pt_7classes_12_04_2023/"
#model_dir = "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_7classes_12_04_2023/"

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

                .Define("genBottom",   "FCCAnalyses::MCParticle::sel_pdgID(5, true)(Particle)")
                .Define("n_genBottoms",      "FCCAnalyses::MCParticle::get_n(genBottom)")
                .Define("genBottom_p",     "FCCAnalyses::MCParticle::get_p(genBottom)")
                .Define("genBottom_e", "FCCAnalyses::MCParticle::get_e(genBottom)")
                .Define("genBottom_pt", "FCCAnalyses::MCParticle::get_pt(genBottom)")
                .Define("genBottom_px", "FCCAnalyses::MCParticle::get_px(genBottom)")
                .Define("genBottom_py", "FCCAnalyses::MCParticle::get_py(genBottom)")
                .Define("genBottom_pz", "FCCAnalyses::MCParticle::get_pz(genBottom)")
                .Define("genBottom_y", "FCCAnalyses::MCParticle::get_y(genBottom)") #rapidity
                .Define("genBottom_eta", "FCCAnalyses::MCParticle::get_eta(genBottom)")
                .Define("genBottom_theta", "FCCAnalyses::MCParticle::get_theta(genBottom)")
                .Define("genBottom_phi", "FCCAnalyses::MCParticle::get_phi(genBottom)")
                .Define("genBottom_charge", "FCCAnalyses::MCParticle::get_charge(genBottom)")
                .Define("genBottom_mass",   "FCCAnalyses::MCParticle::get_mass(genBottom)")

                .Define("GenProton_PID", "FCCAnalyses::MCParticle::sel_pdgID(2212, true)(Particle)")
                .Define("GenKaonPlus_PID", "FCCAnalyses::MCParticle::sel_pdgID(321, true)(Particle)")
                .Define("GenPionPlus_PID", "FCCAnalyses::MCParticle::sel_pdgID(211, true)(Particle)")
                .Define("GenPiK_PID", "FCCAnalyses::MCParticle::mergeParticles(GenKaonPlus_PID, GenPionPlus_PID)")
                .Define("GenChargedHadrons_PID", "FCCAnalyses::MCParticle::mergeParticles(GenProton_PID, GenPiK_PID)")
                .Define("FSGenChargedHadrons", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenChargedHadrons_PID)")
                .Define("n_FSGenChargedHadrons", "FCCAnalyses::MCParticle::get_n(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_p", "FCCAnalyses::MCParticle::get_p(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_e", "FCCAnalyses::MCParticle::get_e(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_pt", "FCCAnalyses::MCParticle::get_pt(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_px", "FCCAnalyses::MCParticle::get_px(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_py", "FCCAnalyses::MCParticle::get_py(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_pz", "FCCAnalyses::MCParticle::get_pz(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_y", "FCCAnalyses::MCParticle::get_y(FSGenChargedHadrons)") #rapidity
                .Define("FSGenChargedHadrons_eta", "FCCAnalyses::MCParticle::get_eta(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_theta", "FCCAnalyses::MCParticle::get_theta(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_phi", "FCCAnalyses::MCParticle::get_phi(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_charge", "FCCAnalyses::MCParticle::get_charge(FSGenChargedHadrons)")
                .Define("FSGenChargedHadrons_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenChargedHadrons)")


                .Define("GenNeutron_PID", "FCCAnalyses::MCParticle::sel_pdgID(2112, true)(Particle)")
                .Define("GenKaon0L_PID", "FCCAnalyses::MCParticle::sel_pdgID(130, true)(Particle)")
                .Define("GenPion0_PID", "FCCAnalyses::MCParticle::sel_pdgID(111, true)(Particle)")
                .Define("GenKn_PID", "FCCAnalyses::MCParticle::mergeParticles(GenNeutron_PID, GenKaon0L_PID)")
                .Define("GenNeutralHadrons_PID", "FCCAnalyses::MCParticle::mergeParticles(GenKn_PID, GenPion0_PID)")
                .Define("FSGenNeutralHadrons", "FCCAnalyses::MCParticle::sel_genStatus(1)(GenNeutralHadrons_PID)")
                .Define("n_FSGenNeutralHadrons", "FCCAnalyses::MCParticle::get_n(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_p", "FCCAnalyses::MCParticle::get_p(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_e", "FCCAnalyses::MCParticle::get_e(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_pt", "FCCAnalyses::MCParticle::get_pt(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_px", "FCCAnalyses::MCParticle::get_px(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_py", "FCCAnalyses::MCParticle::get_py(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_pz", "FCCAnalyses::MCParticle::get_pz(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_y", "FCCAnalyses::MCParticle::get_y(FSGenNeutralHadrons)") #rapidity
                .Define("FSGenNeutralHadrons_eta", "FCCAnalyses::MCParticle::get_eta(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_theta", "FCCAnalyses::MCParticle::get_theta(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_phi", "FCCAnalyses::MCParticle::get_phi(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_charge", "FCCAnalyses::MCParticle::get_charge(FSGenNeutralHadrons)")
                .Define("FSGenNeutralHadrons_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenNeutralHadrons)")



                .Define("reco_mc_index","ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)")



                .Alias("Muon0", "Muon#0.index")
                .Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
                .Alias("Electron0", "Electron#0.index")
                .Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")

                .Define("NeutralHadron_cand",   "ReconstructedParticles[ReconstructedParticles.type != 22]") #this instead excludes all photons with type 22, type 0 is charged particles and then type 130 is K0 that we are interested in, pi0 always decay in gamma-gamma
                .Define("NeutralHadron",       "ReconstructedParticle::sel_charge(0, true) (NeutralHadron_cand)")
                .Define("n_NeutralHadron",  "ReconstructedParticle::get_n(NeutralHadron)")
                .Define("NeutralHadron_type",  "ReconstructedParticle::get_type(NeutralHadron)")
                .Define("NeutralHadron_p",      "ReconstructedParticle::get_p(NeutralHadron)")                
                .Define("NeutralHadron_e",      "ReconstructedParticle::get_e(NeutralHadron)")
                .Define("NeutralHadron_pt",      "ReconstructedParticle::get_pt(NeutralHadron)")
                .Define("NeutralHadron_px",      "ReconstructedParticle::get_px(NeutralHadron)")
                .Define("NeutralHadron_py",      "ReconstructedParticle::get_py(NeutralHadron)")
                .Define("NeutralHadron_pz",      "ReconstructedParticle::get_pz(NeutralHadron)")
                .Define("NeutralHadron_y",      "ReconstructedParticle::get_y(NeutralHadron)")
                .Define("NeutralHadron_eta",     "ReconstructedParticle::get_eta(NeutralHadron)") #pseudorapidity eta
                .Define("NeutralHadron_theta",   "ReconstructedParticle::get_theta(NeutralHadron)")
                .Define("NeutralHadron_phi",     "ReconstructedParticle::get_phi(NeutralHadron)") #polar angle in the transverse plane phi
                .Define("NeutralHadron_charge",  "ReconstructedParticle::get_charge(NeutralHadron)")
                .Define("NeutralHadron_mass",     "ReconstructedParticle::get_mass(NeutralHadron)")

                .Define("NoMuons", "ReconstructedParticle::remove(ReconstructedParticles, RecoMuons)")
                .Define("NoLeptons", "ReconstructedParticle::remove(NoMuons, RecoElectrons)")
                .Define("ChargedHadron", "ReconstructedParticle::sel_charge(1, true) (NoLeptons)")
                .Define("n_ChargedHadron",  "ReconstructedParticle::get_n(ChargedHadron)")
                .Define("ChargedHadron_p",  "ReconstructedParticle::get_p(ChargedHadron)")
                .Define("ChargedHadron_e",      "ReconstructedParticle::get_e(ChargedHadron)")
                .Define("ChargedHadron_pt",      "ReconstructedParticle::get_pt(ChargedHadron)")
                .Define("ChargedHadron_px",      "ReconstructedParticle::get_px(ChargedHadron)")
                .Define("ChargedHadron_py",      "ReconstructedParticle::get_py(ChargedHadron)")
                .Define("ChargedHadron_pz",      "ReconstructedParticle::get_pz(ChargedHadron)")
                .Define("ChargedHadron_y",      "ReconstructedParticle::get_y(ChargedHadron)")
                .Define("ChargedHadron_eta",     "ReconstructedParticle::get_eta(ChargedHadron)") #pseudorapidity eta
                .Define("ChargedHadron_theta",   "ReconstructedParticle::get_theta(ChargedHadron)")
                .Define("ChargedHadron_phi",     "ReconstructedParticle::get_phi(ChargedHadron)") #polar angle in the transverse plane phi
                .Define("ChargedHadron_charge",  "ReconstructedParticle::get_charge(ChargedHadron)")
                .Define("ChargedHadron_mass",     "ReconstructedParticle::get_mass(ChargedHadron)")



                .Define("chadron_idx", "FCCAnalyses::ZHfunctions::getIndex(ChargedHadron, ReconstructedParticles)")
                .Define("nhadron_idx", "FCCAnalyses::ZHfunctions::getIndex(NeutralHadron, ReconstructedParticles)")

                .Define("n_DeltaNeutralHadrons", "return n_NeutralHadron-n_FSGenNeutralHadrons")
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
        
        collections_res = deepcopy(collections)

        df2 = (df2
                #.Redefine(collections_res["PFParticles"],ROOT.SmearObjects.SmearedReconstructedParticle(15.68643, 0, 1, False),[collections["PFParticles"], "reco_mc_index", collections["GenParticles"]]) # 15.68643
                #.Redefine(collections_res["PFParticles"],ROOT.SmearObjects.SmearedReconstructedParticle(15.68643, 130, 1, False),[collections["PFParticles"], "reco_mc_index", collections["GenParticles"]]) # 190.50382

                .Define("S_NoMuons", "ReconstructedParticle::remove({}, RecoMuons)".format(collections_res["PFParticles"]))
                .Define("S_NoLeptons", "ReconstructedParticle::remove(S_NoMuons, RecoElectrons)")
                .Define("smeared_ChargedHadron", "ReconstructedParticle::sel_charge(1, true) (S_NoLeptons)")

                .Define("S_NeutralHadron_cand",   "ReconstructedParticles[{}.type != 22]".format(collections_res["PFParticles"])) #this instead excludes all photons with type 22, type 0 is charged particles and then type 130 is K0 that we are interested in, pi0 always decay in gamma-gamma
                .Define("smeared_NeutralHadron",       "ReconstructedParticle::sel_charge(0, true) (S_NeutralHadron_cand)")

                .Define("smeared_chadron_idx", "FCCAnalyses::ZHfunctions::getIndex(smeared_ChargedHadron, {})".format(collections_res["PFParticles"])) 
                .Define("smeared_nhadron_idx", "FCCAnalyses::ZHfunctions::getIndex(smeared_NeutralHadron, {})".format(collections_res["PFParticles"])) 

                .Define("CHadron_dR", "FCCAnalyses::ZHfunctions::dR_matching(ChargedHadron, chadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle)".format(collections["PFParticles"]))

                #.Define("CHadron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(ChargedHadron, chadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections["PFParticles"]))
                .Define("CHadron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(smeared_ChargedHadron, smeared_chadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections_res["PFParticles"]))

                .Define("NHadron_dR", "FCCAnalyses::ZHfunctions::dR_matching(NeutralHadron, nhadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle)".format(collections["PFParticles"]))

                #.Define("NHadron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(NeutralHadron, nhadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections["PFParticles"]))
                .Define("NHadron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(smeared_NeutralHadron, smeared_nhadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections_res["PFParticles"]))

                .Define("NHadron_low_dR",       "smeared_NeutralHadron[NHadron_dR < 0.01]")
                .Define("NHadron_low_dR_idx",     "smeared_nhadron_idx[NHadron_dR<0.01]")
                .Define("n_NHadron_low_dR",       "ReconstructedParticle::get_n(NHadron_low_dR)")
                .Define("NHadron_low_dR_p",         "ReconstructedParticle::get_p(NHadron_low_dR)")                
                .Define("NHadron_low_dR_e",       "ReconstructedParticle::get_e(NHadron_low_dR)")
                .Define("NHadron_low_dR_pt",      "ReconstructedParticle::get_pt(NHadron_low_dR)")
                .Define("NHadron_low_dR_px",      "ReconstructedParticle::get_px(NHadron_low_dR)")
                .Define("NHadron_low_dR_py",      "ReconstructedParticle::get_py(NHadron_low_dR)")
                .Define("NHadron_low_dR_pz",      "ReconstructedParticle::get_pz(NHadron_low_dR)")
                .Define("NHadron_low_dR_y",       "ReconstructedParticle::get_y(NHadron_low_dR)")
                .Define("NHadron_low_dR_eta",     "ReconstructedParticle::get_eta(NHadron_low_dR)") #pseudorapidity eta
                .Define("NHadron_low_dR_theta",   "ReconstructedParticle::get_theta(NHadron_low_dR)")
                .Define("NHadron_low_dR_phi",     "ReconstructedParticle::get_phi(NHadron_low_dR)") #polar angle in the transverse plane phi
                .Define("NHadron_low_dR_charge",  "ReconstructedParticle::get_charge(NHadron_low_dR)")
                .Define("NHadron_low_dR_mass",    "ReconstructedParticle::get_mass(NHadron_low_dR)")
                .Define("NHadron_low_dR_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(NHadron_low_dR, NHadron_low_dR_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections_res["PFParticles"]))
                .Define("NHadron_low_dR_MCPDG", "FCCAnalyses::ZHfunctions::Reco2MCpdg(NHadron_low_dR, NHadron_low_dR_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle)".format(collections["PFParticles"]))

                .Define("NHadron_high_dR",       "smeared_NeutralHadron[NHadron_dR>0.06]")
                .Define("NHadron_high_dR_idx",     "smeared_nhadron_idx[NHadron_dR>0.06]")
                .Define("n_NHadron_high_dR",       "ReconstructedParticle::get_n(NHadron_high_dR)")
                .Define("NHadron_high_dR_p",       "ReconstructedParticle::get_p(NHadron_high_dR)")                
                .Define("NHadron_high_dR_e",       "ReconstructedParticle::get_e(NHadron_high_dR)")
                .Define("NHadron_high_dR_pt",      "ReconstructedParticle::get_pt(NHadron_high_dR)")
                .Define("NHadron_high_dR_px",      "ReconstructedParticle::get_px(NHadron_high_dR)")
                .Define("NHadron_high_dR_py",      "ReconstructedParticle::get_py(NHadron_high_dR)")
                .Define("NHadron_high_dR_pz",      "ReconstructedParticle::get_pz(NHadron_high_dR)")
                .Define("NHadron_high_dR_y",       "ReconstructedParticle::get_y(NHadron_high_dR)")
                .Define("NHadron_high_dR_eta",     "ReconstructedParticle::get_eta(NHadron_high_dR)") #pseudorapidity eta
                .Define("NHadron_high_dR_theta",   "ReconstructedParticle::get_theta(NHadron_high_dR)")
                .Define("NHadron_high_dR_phi",     "ReconstructedParticle::get_phi(NHadron_high_dR)") #polar angle in the transverse plane phi
                .Define("NHadron_high_dR_charge",  "ReconstructedParticle::get_charge(NHadron_high_dR)")
                .Define("NHadron_high_dR_mass",    "ReconstructedParticle::get_mass(NHadron_high_dR)")
                .Define("NHadron_high_dR_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(NHadron_high_dR, NHadron_high_dR_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections_res["PFParticles"]))
                .Define("NHadron_high_dR_MCPDG", "FCCAnalyses::ZHfunctions::Reco2MCpdg(NHadron_high_dR, NHadron_high_dR_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle)".format(collections["PFParticles"]))

                #.Define("RecoElectrons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoElectrons)")
                #.Define("RecoElectrons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoElectrons_hard, ReconstructedParticles)")
                #.Define("RecoElectrons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoElectrons_hard, RecoElectrons_iso)")
                #.Define("RecoMuons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(RecoMuons)")
                #.Define("RecoMuons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(RecoMuons_hard, ReconstructedParticles)")
                #.Define("RecoMuons_sel", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(RecoMuons_hard, RecoMuons_iso)")
                #.Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove({},RecoMuons)".format(collections_res["PFParticles"]))
                #.Define("ReconstructedParticlesNoLeps",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons,RecoElectrons)")

                #.Define("Photons_excl",   "ReconstructedParticles[ReconstructedParticles.type == 22 && ReconstructedParticles.energy < 2]") #this considers all photons with type 22 

                #.Define("ReconstructedParticlesJET",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoLeps,Photons_excl)")
        )
        #collections_noleps = copy.deepcopy(collections_res)
        #collections_noleps["PFParticles"] = "ReconstructedParticlesJET"

        ## def __init__(self, coll, njets, tag="")
        jetClusteringHelper_kt2  = ExclusiveJetClusteringHelper(
            collections_res["PFParticles"], 2, "kt2"
        )
        df2 = jetClusteringHelper_kt2.define(df2)

        ## define jet flavour tagging parameters
        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections_res,
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

                .Define("jet_p4",               "FCCAnalyses::ZHfunctions::build_p4(TagJet_kt2_px, TagJet_kt2_py, TagJet_kt2_pz, TagJet_kt2_e)")
                .Define("Dijet_p4",             "jet_p4.at(0) + jet_p4.at(1)")
                .Define("Dijet_mass",           "Dijet_p4.M()")
                .Define("smeared_jet_p4",       "FCCAnalyses::ZHfunctions::smear_jet(jet_p4, 52.5, 6.96, Dijet_mass)")
                .Define("smeared_Dijet_p4",     "smeared_jet_p4.at(0) + smeared_jet_p4.at(1)")
                .Define("smeared_Dijet_mass",   "Dijet_p4.M()")

                .Define("jet_reso", "FCCAnalyses::ZHfunctions::jet_reso(TagJet_kt2_px,TagJet_kt2_py,TagJet_kt2_pz,TagJet_kt2_mass,genBottom)")
        )






        return df2
    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [

            "n_FSGenNeutralHadrons",
            "FSGenNeutralHadrons_p",
            "FSGenNeutralHadrons_e",
            "FSGenNeutralHadrons_pt",
            "FSGenNeutralHadrons_px",
            "FSGenNeutralHadrons_py",
            "FSGenNeutralHadrons_pz",
            "FSGenNeutralHadrons_y",
            "FSGenNeutralHadrons_eta",
            "FSGenNeutralHadrons_theta",
            "FSGenNeutralHadrons_phi",
            "FSGenNeutralHadrons_charge",
            "FSGenNeutralHadrons_mass",

            "n_FSGenChargedHadrons",
            "FSGenChargedHadrons_p",
            "FSGenChargedHadrons_e",
            "FSGenChargedHadrons_pt",
            "FSGenChargedHadrons_px",
            "FSGenChargedHadrons_py",
            "FSGenChargedHadrons_pz",
            "FSGenChargedHadrons_y",
            "FSGenChargedHadrons_eta",
            "FSGenChargedHadrons_theta",
            "FSGenChargedHadrons_phi",
            "FSGenChargedHadrons_charge",
            "FSGenChargedHadrons_mass",
            
            "n_genBottoms",
            "genBottom_p",
            "genBottom_e",
            "genBottom_pt",
            "genBottom_px",
            "genBottom_py",
            "genBottom_pz",
            "genBottom_y",
            "genBottom_eta",
            "genBottom_theta",
            "genBottom_phi",
            "genBottom_charge",
            "genBottom_mass",


            "n_NeutralHadron",
            "NeutralHadron_type",
            "NeutralHadron_p",
            "NeutralHadron_e",
            "NeutralHadron_pt",
            "NeutralHadron_px",
            "NeutralHadron_py",
            "NeutralHadron_pz",
            "NeutralHadron_y",
            "NeutralHadron_eta",
            "NeutralHadron_theta",
            "NeutralHadron_phi",
            "NeutralHadron_charge",
            "NeutralHadron_mass",

            "n_ChargedHadron",
            "ChargedHadron_p",
            "ChargedHadron_e",
            "ChargedHadron_pt",
            "ChargedHadron_px",
            "ChargedHadron_py",
            "ChargedHadron_pz",
            "ChargedHadron_y",
            "ChargedHadron_eta",
            "ChargedHadron_theta",
            "ChargedHadron_phi",
            "ChargedHadron_charge",
            "ChargedHadron_mass",

            "CHadron_dR",
            "NHadron_dR",

            "n_DeltaNeutralHadrons",

            "n_NHadron_low_dR",  
            "NHadron_low_dR_p",     
            "NHadron_low_dR_e",
            "NHadron_low_dR_pt",
            "NHadron_low_dR_px",
            "NHadron_low_dR_py",
            "NHadron_low_dR_pz",
            "NHadron_low_dR_y",
            "NHadron_low_dR_eta",
            "NHadron_low_dR_theta",
            "NHadron_low_dR_phi",
            "NHadron_low_dR_charge",
            "NHadron_low_dR_mass",
            "NHadron_low_dR_p_res_total",
            "NHadron_low_dR_MCPDG",


            "n_NHadron_high_dR",
            "NHadron_high_dR_p",        
            "NHadron_high_dR_e",
            "NHadron_high_dR_pt",
            "NHadron_high_dR_px",
            "NHadron_high_dR_py",
            "NHadron_high_dR_pz",
            "NHadron_high_dR_y",
            "NHadron_high_dR_eta",
            "NHadron_high_dR_theta",
            "NHadron_high_dR_phi",
            "NHadron_high_dR_charge",
            "NHadron_high_dR_mass",
            "NHadron_high_dR_p_res_total", 
            "NHadron_high_dR_MCPDG",

            "n_TagJet_kt2",
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
            "Dijet_mass",
            "smeared_Dijet_mass",

            "CHadron_p_res_total",
            "NHadron_p_res_total",
            "jet_reso",
        ]

        return branchList