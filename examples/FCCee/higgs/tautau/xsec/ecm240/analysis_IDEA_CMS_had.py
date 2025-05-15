import os, copy # tagging
import ROOT
import urllib.request
from copy import deepcopy

processList = {
    'IDEA_events_002119867': {},
    #'CMS_Phase2_events_002119867': {},
    #'CMS_Phase1_events_002119867': {},
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
#def get_file_path(url, filename):
#    if os.path.exists(filename):
#        return os.path.abspath(filename)
    #else:
    #    urllib.request.urlretrieve(url, os.path.basename(url))
    #    return os.path.basename(url)
    ## this is the old version of the tagger and we don't care about it


#weaver_preproc = get_file_path(url_preproc, local_preproc)
#weaver_model = get_file_path(url_model, local_model)

#from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
#from addons.FastJet.jetClusteringHelper import (
#    ExclusiveJetClusteringHelper,
#    InclusiveJetClusteringHelper,
#)

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

                .Define("reco_mc_index","ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)")

                .Alias("Muon0", "Muon#0.index")
                .Define("RecoMuons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
                .Alias("Electron0", "Electron#0.index")
                .Define("RecoElectrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)")

                .Define("NeutralHadron_cand",   "ReconstructedParticles[ReconstructedParticles.type != 22]") #this instead excludes all photons with type 22, type 0 is charged particles and then type 130 is K0 that we are interested in, pi0 always decay in gamma-gamma
                .Define("NeutralHadron",       "ReconstructedParticle::sel_charge(0, true) (NeutralHadron_cand)")

                .Define("NoMuons", "ReconstructedParticle::remove(ReconstructedParticles, RecoMuons)")
                .Define("NoLeptons", "ReconstructedParticle::remove(NoMuons, RecoElectrons)")
                .Define("ChargedHadron", "ReconstructedParticle::sel_charge(1, true) (NoLeptons)")

                .Define("chadron_idx", "FCCAnalyses::ZHfunctions::getIndex(ChargedHadron, ReconstructedParticles)")
                .Define("nhadron_idx", "FCCAnalyses::ZHfunctions::getIndex(NeutralHadron, ReconstructedParticles)")
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
                .Redefine(collections_res["PFParticles"],ROOT.SmearObjects.SmearedReconstructedParticle(190.50382, 0, 1, False),[collections["PFParticles"], "reco_mc_index", collections["GenParticles"]])
                #.Redefine(collections_res["PFParticles"],ROOT.SmearObjects.SmearedReconstructedParticle(1.24322, 130, 1, False),[collections["PFParticles"], "reco_mc_index", collections["GenParticles"]])

                .Define("S_NoMuons", "ReconstructedParticle::remove({}, RecoMuons)".format(collections_res["PFParticles"]))
                .Define("S_NoLeptons", "ReconstructedParticle::remove(S_NoMuons, RecoElectrons)")
                .Define("smeared_ChargedHadron", "ReconstructedParticle::sel_charge(1, true) (S_NoLeptons)")

                #.Define("S_NeutralHadron_cand",   "ReconstructedParticles[{}.type != 22]".format(collections_res["PFParticles"])) #this instead excludes all photons with type 22, type 0 is charged particles and then type 130 is K0 that we are interested in, pi0 always decay in gamma-gamma
                #.Define("smeared_NeutralHadron",       "ReconstructedParticle::sel_charge(0, true) (S_NeutralHadron_cand)")

                .Define("smeared_chadron_idx", "FCCAnalyses::ZHfunctions::getIndex(smeared_ChargedHadron, {})".format(collections_res["PFParticles"])) 
                #.Define("smeared_nhadron_idx", "FCCAnalyses::ZHfunctions::getIndex(smeared_NeutralHadron, {})".format(collections_res["PFParticles"])) 

                #.Define("CHadron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(ChargedHadron, chadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections["PFParticles"]))
                .Define("CHadron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(smeared_ChargedHadron, smeared_chadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections_res["PFParticles"]))

                #.Define("NHadron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(NeutralHadron, nhadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections["PFParticles"]))
                #.Define("NHadron_p_res_total", "FCCAnalyses::ZHfunctions::particleResolution(smeared_NeutralHadron, smeared_nhadron_idx, MCRecoAssociations0, MCRecoAssociations1, {}, Particle, 0)".format(collections_res["PFParticles"]))
        )
        return df2
    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
            "CHadron_p_res_total",
            #"NHadron_p_res_total",
        ]

        return branchList