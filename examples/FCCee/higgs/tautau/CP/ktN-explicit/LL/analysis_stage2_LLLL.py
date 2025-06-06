import os, copy # tagging
import ROOT
import urllib.request

#Mandatory: List of processes
processList_ = {
    "mg_ee_eetata_ecm240":{},
    "mg_ee_eetata_smeft_cehim_m1_ecm240":{},
    "mg_ee_eetata_smeft_cehim_p1_ecm240":{},
    "mg_ee_eetata_smeft_cehre_m1_ecm240":{},
    "mg_ee_eetata_smeft_cehre_p1_ecm240":{},
    "mg_ee_jjtata_ecm240":{'chunks':10},
    "mg_ee_jjtata_smeft_cehim_m1_ecm240":{'chunks':10},
    "mg_ee_jjtata_smeft_cehim_p1_ecm240":{'chunks':10},
    "mg_ee_jjtata_smeft_cehre_m1_ecm240":{'chunks':10},
    "mg_ee_jjtata_smeft_cehre_p1_ecm240":{'chunks':10},
    "mg_ee_mumutata_ecm240":{},
    "mg_ee_mumutata_smeft_cehim_m1_ecm240":{},
    "mg_ee_mumutata_smeft_cehim_p1_ecm240":{},
    "mg_ee_mumutata_smeft_cehre_m1_ecm240":{},
    "mg_ee_mumutata_smeft_cehre_p1_ecm240":{},

    "p8_ee_bbH_Htautau_CPeven":{},
    "p8_ee_bbH_Htautau_CPodd":{},
    "p8_ee_ccH_Htautau_CPeven":{},
    "p8_ee_ccH_Htautau_CPodd":{},
    "p8_ee_eeH_Htautau_CPeven":{},
    "p8_ee_eeH_Htautau_CPodd":{},
    "p8_ee_mumuH_Htautau_CPeven":{},
    "p8_ee_mumuH_Htautau_CPodd":{},
    "p8_ee_ssH_Htautau_CPeven":{},
    "p8_ee_ssH_Htautau_CPodd":{},
    "p8_ee_qqH_Htautau_CPeven":{},
    "p8_ee_qqH_Htautau_CPodd":{},
}
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
prodTag     = "FCCee/winter2023/IDEA/"
#inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/MCgenCP/"

#inputDir = "/ceph/sgiappic/HiggsCP/winter23"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"

#Optional: output directory, default is local running directory
#outputDir   = "/ceph/sgiappic/HiggsCP/stage1_241105/" 
outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/stage1_250530/ktN-explicit/LL/LL"

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
compGroup = "group_u_FCC.local_gen"

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
                .Define("RecoEmiss", "FCCAnalyses::ZHfunctions::missingEnergy(240, ReconstructedParticles)") #ecm 
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

                # four leptons in the whole event that make the Z boson, find the pair later, even if using tagged jets taus should not have leptons in the jets!!! should help with background rejection
                # anyway now i want zero jets so it doesn't even matter
                .Define("AllLeptons",    "(((n_RecoElectrons==4 and n_RecoMuons==0) or (n_RecoElectrons==0 and n_RecoMuons==4)) and (RecoLepton_charge.at(0) + RecoLepton_charge.at(1) + RecoLepton_charge.at(2) + RecoLepton_charge.at(3))==0)*1.0")
                .Define("TwoPairs",     "((n_RecoElectrons==2 and n_RecoMuons==2) and (RecoElectron_charge.at(0) + RecoElectron_charge.at(1))==0 and (RecoMuon_charge.at(0) + RecoMuon_charge.at(1))==0)*1.0")
                .Define("OnePair",     "(((n_RecoElectrons==3 and n_RecoMuons==1) or (n_RecoElectrons==1 and n_RecoMuons==3))  and (RecoLepton_charge.at(0) + RecoLepton_charge.at(1) + RecoLepton_charge.at(2) + RecoLepton_charge.at(3))==0)*1.0")

                .Filter("(AllLeptons==1 || TwoPairs==1 || OnePair==1)")

                .Define("NoPhotons",   "ReconstructedParticles[ReconstructedParticles.type != 22]")

                .Filter("n_RecoLeptons==NoPhotons.size()")

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

                .Define("TauFromJet_R5", "FCCAnalyses::ZHfunctions::findTauInJet_All({}, 0)".format(jetClusteringHelper_R5.constituents)) 
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

                .Define("TagJet_R5_sel_e",      "TagJet_R5_e[TauFromJet_R5_type_sel<0]")
                .Define("TagJet_R5_sel_p",      "TagJet_R5_p[TauFromJet_R5_type_sel<0]")
                .Define("TagJet_R5_sel_pt",      "TagJet_R5_pt[TauFromJet_R5_type_sel<0]")
                .Define("TagJet_R5_sel_px",      "TagJet_R5_px[TauFromJet_R5_type_sel<0]")
                .Define("TagJet_R5_sel_py",      "TagJet_R5_py[TauFromJet_R5_type_sel<0]")
                .Define("TagJet_R5_sel_pz",      "TagJet_R5_pz[TauFromJet_R5_type_sel<0]")
		        .Define("TagJet_R5_sel_eta",     "TagJet_R5_eta[TauFromJet_R5_type_sel<0]")
                .Define("TagJet_R5_sel_theta",   "TagJet_R5_theta[TauFromJet_R5_type_sel<0]")
		        .Define("TagJet_R5_sel_phi",     "TagJet_R5_phi[TauFromJet_R5_type_sel<0]")
                .Define("TagJet_R5_sel_mass",      "TagJet_R5_mass[TauFromJet_R5_type_sel<0]")
                .Define("n_TagJet_R5_sel", "TagJet_R5_sel_e.size()")

                #get the leading charged particle in the tau jet, if only neutral particles are present then the particle is null
                .Define("ChargedTau_R5_all",      "FCCAnalyses::ZHfunctions::findTauInJet_All({}, 1)".format(jetClusteringHelper_R5.constituents))
                .Define("ChargedTau_R5_type",      "ReconstructedParticle::get_type(ChargedTau_R5_all)") 
                .Define("ChargedTau_R5",      "ChargedTau_R5_all[ChargedTau_R5_type>=0]") 
                .Define("n_ChargedTau_R5",      "ReconstructedParticle::get_n(ChargedTau_R5)") 
                .Define("ChargedTau_R5_e",      "ReconstructedParticle::get_e(ChargedTau_R5)")
                .Define("ChargedTau_R5_p",      "ReconstructedParticle::get_p(ChargedTau_R5)")
                .Define("ChargedTau_R5_pt",      "ReconstructedParticle::get_pt(ChargedTau_R5)")
                .Define("ChargedTau_R5_px",      "ReconstructedParticle::get_px(ChargedTau_R5)")
                .Define("ChargedTau_R5_py",      "ReconstructedParticle::get_py(ChargedTau_R5)")
                .Define("ChargedTau_R5_pz",      "ReconstructedParticle::get_pz(ChargedTau_R5)")
                .Define("ChargedTau_R5_eta",     "ReconstructedParticle::get_eta(ChargedTau_R5)") #pseudorapidity eta
                .Define("ChargedTau_R5_theta",   "ReconstructedParticle::get_theta(ChargedTau_R5)")
                .Define("ChargedTau_R5_phi",     "ReconstructedParticle::get_phi(ChargedTau_R5)") #polar angle in the transverse plane phi
                .Define("ChargedTau_R5_charge",  "ReconstructedParticle::get_charge(ChargedTau_R5)")
                .Define("ChargedTau_R5_mass",  "ReconstructedParticle::get_mass(ChargedTau_R5)")
                .Define("ChargedTau_R5_p4",  "FCCAnalyses::ZHfunctions::build_p4(ChargedTau_R5_px, ChargedTau_R5_py, ChargedTau_R5_pz, ChargedTau_R5_e)")

                #get the neutral hadronic system for the tau jet, all in one "particle" variable, photons are kept separetely but would be related in pairs to pi0
                .Define("NeutralTau_R5_all",      "FCCAnalyses::ZHfunctions::findTauInJet_All({}, 2)".format(jetClusteringHelper_R5.constituents))
                .Define("NeutralTau_R5_type",      "ReconstructedParticle::get_type(NeutralTau_R5_all)") 
                .Define("NeutralTau_R5",      "NeutralTau_R5_all[NeutralTau_R5_type>=0]") 
                .Define("n_NeutralTau_R5",      "ReconstructedParticle::get_n(NeutralTau_R5)") 
                .Define("NeutralTau_R5_e",      "ReconstructedParticle::get_e(NeutralTau_R5)")
                .Define("NeutralTau_R5_p",      "ReconstructedParticle::get_p(NeutralTau_R5)")
                .Define("NeutralTau_R5_pt",      "ReconstructedParticle::get_pt(NeutralTau_R5)")
                .Define("NeutralTau_R5_px",      "ReconstructedParticle::get_px(NeutralTau_R5)")
                .Define("NeutralTau_R5_py",      "ReconstructedParticle::get_py(NeutralTau_R5)")
                .Define("NeutralTau_R5_pz",      "ReconstructedParticle::get_pz(NeutralTau_R5)")
                .Define("NeutralTau_R5_eta",     "ReconstructedParticle::get_eta(NeutralTau_R5)") #pseudorapidity eta
                .Define("NeutralTau_R5_theta",   "ReconstructedParticle::get_theta(NeutralTau_R5)")
                .Define("NeutralTau_R5_phi",     "ReconstructedParticle::get_phi(NeutralTau_R5)") #polar angle in the transverse plane phi
                .Define("NeutralTau_R5_charge",  "ReconstructedParticle::get_charge(NeutralTau_R5)")
                .Define("NeutralTau_R5_mass",  "ReconstructedParticle::get_mass(NeutralTau_R5)")
                .Define("NeutralTau_R5_p4",  "FCCAnalyses::ZHfunctions::build_p4(NeutralTau_R5_px, NeutralTau_R5_py, NeutralTau_R5_pz, NeutralTau_R5_e)") 
        )

        df2 = (df2

                ##########################
                ###### Ex. stage2 ########
                ##########################

                ### to find already made functions, this is where they are or where they can be added instead of writing them here
                ### https://github.com/Edler1/FCCAnalyses-1/tree/7f6006a1e4579c9bc01a149732ea39685cbad951/analyzers/dataframe/src

                ### defining filters for 4 lepton final state based on flavor combination: 4 same flavor, 2 pairs, 1 pair plus one mixed from the taus

                .Define("TauTag_px",      "TagJet_R5_px[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_py",      "TagJet_R5_py[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_pz",      "TagJet_R5_pz[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_pt",      "TagJet_R5_pt[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_p",      "TagJet_R5_p[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_e",      "TagJet_R5_e[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_phi",      "TagJet_R5_phi[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_eta",      "TagJet_R5_eta[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_theta",      "TagJet_R5_theta[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_charge",      "TagJet_R5_charge[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_mass",      "TagJet_R5_mass[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_isG",      "TagJet_R5_isG[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_isU",      "TagJet_R5_isU[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_isD",      "TagJet_R5_isD[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_isS",      "TagJet_R5_isS[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_isC",      "TagJet_R5_isC[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_isB",      "TagJet_R5_isB[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_isTAU",      "TagJet_R5_isTAU[TagJet_R5_isTAU>0.5 ]")
                .Define("TauTag_flavor",      "TagJet_R5_flavor[TagJet_R5_isTAU>0.5 ]")
                .Define("n_TauTag_constituents",        "n_TagJet_R5_constituents[TagJet_R5_isTAU>0.5 ]")
                .Define("n_TauTag_charged_constituents",        "n_TagJet_R5_charged_constituents[TagJet_R5_isTAU>0.5 ]")
                .Define("n_TauTag_neutral_constituents",        "n_TagJet_R5_neutral_constituents[TagJet_R5_isTAU>0.5 ]")
                .Define("n_TauTag",          "TauTag_px.size()")

                .Define("QuarkTag_px",      "TagJet_R5_px[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_py",      "TagJet_R5_py[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_pz",      "TagJet_R5_pz[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_pt",      "TagJet_R5_pt[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_p",      "TagJet_R5_p[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_e",      "TagJet_R5_e[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_phi",      "TagJet_R5_phi[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_eta",      "TagJet_R5_eta[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_theta",      "TagJet_R5_theta[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_charge",      "TagJet_R5_charge[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_mass",      "TagJet_R5_mass[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_isG",      "TagJet_R5_isG[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_isU",      "TagJet_R5_isU[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_isD",      "TagJet_R5_isD[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_isS",      "TagJet_R5_isS[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_isC",      "TagJet_R5_isC[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_isB",      "TagJet_R5_isB[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_isTAU",      "TagJet_R5_isTAU[TagJet_R5_isTAU<=0.5 ]")
                .Define("QuarkTag_flavor",      "TagJet_R5_flavor[TagJet_R5_isTAU<=0.5 ]")
                .Define("n_QuarkTag_constituents",        "n_TagJet_R5_constituents[TagJet_R5_isTAU<=0.5 ]")
                .Define("n_QuarkTag_charged_constituents",        "n_TagJet_R5_charged_constituents[TagJet_R5_isTAU<=0.5 ]")
                .Define("n_QuarkTag_neutral_constituents",        "n_TagJet_R5_neutral_constituents[TagJet_R5_isTAU<=0.5 ]")
                .Define("n_QuarkTag",     "QuarkTag_charge.size()")

                ####################
                ##### FILTER 2 #####
                ####################

                #.Filter("n_TauTag==0 && n_QuarkTag==0") 

                ##################

                .Define("RecoLepton_p4",  "FCCAnalyses::ZHfunctions::build_p4(RecoLepton_px, RecoLepton_py, RecoLepton_pz, RecoLepton_e)")

                .Define("RecoZH_idx",        "FCCAnalyses::ZHfunctions::FindBest_4(RecoLepton_p4, RecoLepton_charge, RecoLepton_mass, 91.188, 125.25)")

                .Define("RecoZ1_p4",      "RecoLepton_p4.at(RecoZH_idx[0])")
                .Define("RecoZ2_p4",        "RecoLepton_p4.at(RecoZH_idx[1])")
                
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

                .Define("RecoTau1_p4",      "RecoLepton_p4.at(RecoZH_idx[2])")
                .Define("RecoTau2_p4",      "RecoLepton_p4.at(RecoZH_idx[3])")
                .Define("RecoTau1_type",        "if (RecoLepton_mass.at(RecoZH_idx[2])<0.05) return float(-0.11); else return float(-0.13);")
                .Define("RecoTau2_type",        "if (RecoLepton_mass.at(RecoZH_idx[2])<0.05) return float(-0.13); else return float(-0.11);")

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
                .Define("Recoil_p4",       "Total_p4-RecoZ_p4")
                .Define("Recoil_mass",       "Recoil_p4.M()")
                .Define("Recoil_px",       "Recoil_p4.Px()")
                .Define("Recoil_py",       "Recoil_p4.Py()")
                .Define("Recoil_pz",       "Recoil_p4.Pz()")
                .Define("Recoil_e",       "Recoil_p4.E()")

                .Define("p12",      "(TauLead_py*TauSub_px-TauLead_px*TauSub_py)")
                .Define("r0",       "abs((RecoEmiss_py*TauLead_px-RecoEmiss_px*TauLead_py)/p12)")
                .Define("f0",       "1./(1.+r0)")
                .Define("r1",       "abs((RecoEmiss_py*TauSub_px-RecoEmiss_px*TauSub_py)/p12)")
                .Define("f1",       "1./(1.+r1)")
                .Define("Collinear_mass",       "RecoH_mass/sqrt(f0*f1)")

                ##############################
                ###### Tracks and Impact ####
                ##############################

                .Define("RecoTauLeptons", "ReconstructedParticle::merge(ROOT::VecOps::RVec{RecoLeptons.at(RecoZH_idx[2])}, ROOT::VecOps::RVec{RecoLeptons.at(RecoZH_idx[3])})")
             
                .Define("RecoLeptonTrack",   "ReconstructedParticle2Track::getRP2TRK( RecoTauLeptons, EFlowTrack_1)")
                .Define("RecoLeptonTrack_D0", "ReconstructedParticle2Track::getRP2TRK_D0(RecoTauLeptons,EFlowTrack_1)")
                .Define("RecoLeptonTrack_Z0", "ReconstructedParticle2Track::getRP2TRK_Z0(RecoTauLeptons,EFlowTrack_1)")
                .Define("RecoLeptonTrack_D0sig", "ReconstructedParticle2Track::getRP2TRK_D0_sig(RecoTauLeptons,EFlowTrack_1)") #significance
                .Define("RecoLeptonTrack_Z0sig", "ReconstructedParticle2Track::getRP2TRK_Z0_sig(RecoTauLeptons,EFlowTrack_1)")
                .Define("RecoLeptonTrack_charge", "ReconstructedParticle2Track::getRP2TRK_charge(RecoTauLeptons,EFlowTrack_1)")
                .Define("RecoLeptonTrack_omega", "ReconstructedParticle2Track::getRP2TRK_omega(RecoTauLeptons,EFlowTrack_1)")

                .Define("TauLeptons_p4",        "FCCAnalyses::ZHfunctions::build_p4_class( RecoLepton_p4.at(RecoZH_idx[2]), RecoLepton_p4.at(RecoZH_idx[3]) )")

                .Define("LeptonImpact_p4",     "FCCAnalyses::ZHfunctions::ImpactVector(TauLeptons_p4, RecoLeptonTrack_D0, RecoLeptonTrack_Z0)")

                ###########################
                ########### CP ############
                ###########################

                .Define("Z1Track",      "ReconstructedParticle2Track::getRP2TRK( ROOT::VecOps::RVec{RecoLeptons.at(RecoZH_idx[0])}, EFlowTrack_1)")
                .Define("Z2Track",      "ReconstructedParticle2Track::getRP2TRK( ROOT::VecOps::RVec{RecoLeptons.at(RecoZH_idx[1])}, EFlowTrack_1)")
                .Define("ZTracks",      "ReconstructedTrack::Merge(Z1Track, Z2Track)")

                .Define("RecoDecayVertexObjectZ",   "VertexFitterSimple::VertexFitter_Tk( 0, ZTracks)" ) ### reconstructing a vertex withour any request n=0 ###
                .Define("RecoDecayVertexZ",  "VertexingUtils::get_VertexData( RecoDecayVertexObjectZ )")
                .Define("RecoIP_p4",     "TLorentzVector(RecoDecayVertexZ.position.x, RecoDecayVertexZ.position.y, RecoDecayVertexZ.position.z, 0.)")
                .Define("RecoIP_px",        "RecoIP_p4.Px()")
                .Define("RecoIP_py",        "RecoIP_p4.Py()")
                .Define("RecoIP_pz",        "RecoIP_p4.Pz()")

                .Define("ChargedTauImpactP_p4",       "if (RecoLeptonTrack_charge.at(0)==1) return LeptonImpact_p4.at(0); else return LeptonImpact_p4.at(1);")
                .Define("RecoPiP_D0",       "if (RecoLeptonTrack_charge.at(0)==1) return RecoLeptonTrack_D0.at(0); else return RecoLeptonTrack_D0.at(1);")
                .Define("RecoPiP_Z0",       "if (RecoLeptonTrack_charge.at(0)==1) return RecoLeptonTrack_Z0.at(0); else return RecoLeptonTrack_Z0.at(1);")
                .Define("RecoPiP_D0sig",       "if (RecoLeptonTrack_charge.at(0)==1) return RecoLeptonTrack_D0sig.at(0); else return RecoLeptonTrack_D0sig.at(1);")
                .Define("RecoPiP_Z0sig",       "if (RecoLeptonTrack_charge.at(0)==1) return RecoLeptonTrack_Z0sig.at(0); else return RecoLeptonTrack_Z0sig.at(1);")
                .Define("RecoPiP_dx",        "ChargedTauImpactP_p4.Px()")
                .Define("RecoPiP_dy",        "ChargedTauImpactP_p4.Py()")
                .Define("RecoPiP_dz",        "ChargedTauImpactP_p4.Pz()")

                .Define("ChargedTauImpactM_p4",       "if (RecoLeptonTrack_charge.at(0)==1) return LeptonImpact_p4.at(1); else return LeptonImpact_p4.at(0);")
                .Define("RecoPiM_D0",       "if (RecoLeptonTrack_charge.at(0)==1) return RecoLeptonTrack_D0.at(1); else return RecoLeptonTrack_D0.at(0);")
                .Define("RecoPiM_Z0",       "if (RecoLeptonTrack_charge.at(0)==1) return RecoLeptonTrack_Z0.at(1); else return RecoLeptonTrack_Z0.at(0);")
                .Define("RecoPiM_D0sig",       "if (RecoLeptonTrack_charge.at(0)==1) return RecoLeptonTrack_D0sig.at(1); else return RecoLeptonTrack_D0sig.at(0);")
                .Define("RecoPiM_Z0sig",       "if (RecoLeptonTrack_charge.at(0)==1) return RecoLeptonTrack_Z0sig.at(1); else return RecoLeptonTrack_Z0sig.at(0);")
                .Define("RecoPiM_dx",        "ChargedTauImpactM_p4.Px()")
                .Define("RecoPiM_dy",        "ChargedTauImpactM_p4.Py()")
                .Define("RecoPiM_dz",        "ChargedTauImpactM_p4.Pz()")

                .Define("Impact_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(ChargedTauImpactP_p4, ChargedTauImpactM_p4)")

                .Define("RecoPiP_p4",       "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return RecoLepton_p4.at(RecoZH_idx[2]); else return RecoLepton_p4.at(RecoZH_idx[3]);")
                .Define("RecoPiM_p4",       "if (RecoLepton_charge.at(RecoZH_idx[2])==1) return RecoLepton_p4.at(RecoZH_idx[3]); else return RecoLepton_p4.at(RecoZH_idx[2]);")
                .Define("RecoPi_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(RecoPiP_p4, RecoPiM_p4)")

                .Define("RecoPiP_px",        "RecoPiP_p4.Px()")
                .Define("RecoPiP_py",        "RecoPiP_p4.Py()")
                .Define("RecoPiP_pz",        "RecoPiP_p4.Pz()")
                .Define("RecoPiP_e",        "RecoPiP_p4.E()")
                .Define("RecoPiP_p",        "RecoPiP_p4.P()")
                .Define("RecoPiP_phi",        "RecoPiP_p4.Phi()")
                .Define("RecoPiP_eta",        "RecoPiP_p4.Eta()")
                .Define("RecoPiP_theta",        "RecoPiP_p4.Theta()")
                .Define("RecoPiP_charge",        "1")

                .Define("RecoPiM_px",        "RecoPiM_p4.Px()")
                .Define("RecoPiM_py",        "RecoPiM_p4.Py()")
                .Define("RecoPiM_pz",        "RecoPiM_p4.Pz()")
                .Define("RecoPiM_e",        "RecoPiM_p4.E()")
                .Define("RecoPiM_p",        "RecoPiM_p4.P()")
                .Define("RecoPiM_phi",        "RecoPiM_p4.Phi()")
                .Define("RecoPiM_eta",        "RecoPiM_p4.Eta()")
                .Define("RecoPiM_theta",        "RecoPiM_p4.Theta()")
                .Define("RecoPiM_charge",        "-1")

                .Define("RecoPi0P_p4",       "TLorentzVector(0.,0.,0.,0.)")
                .Define("RecoPi0M_p4",       "TLorentzVector(0.,0.,0.,0.)")
                .Define("RecoPi0_p4",      "FCCAnalyses::ZHfunctions::build_p4_class(RecoPi0P_p4, RecoPi0M_p4)")

                .Define("RecoPi0P_px",        "RecoPi0P_p4.Px()")
                .Define("RecoPi0P_py",        "RecoPi0P_p4.Py()")
                .Define("RecoPi0P_pz",        "RecoPi0P_p4.Pz()")
                .Define("RecoPi0P_e",        "RecoPi0P_p4.E()")
                .Define("RecoPi0P_phi",        "RecoPi0P_p4.Phi()")
                .Define("RecoPi0P_eta",        "RecoPi0P_p4.Eta()")
                .Define("RecoPi0P_theta",        "RecoPi0P_p4.Theta()")

                .Define("RecoPi0M_px",        "RecoPi0M_p4.Px()")
                .Define("RecoPi0M_py",        "RecoPi0M_p4.Py()")
                .Define("RecoPi0M_pz",        "RecoPi0M_p4.Pz()")
                .Define("RecoPi0M_e",        "RecoPi0M_p4.E()")
                .Define("RecoPi0M_phi",        "RecoPi0M_p4.Phi()")
                .Define("RecoPi0M_eta",        "RecoPi0M_p4.Eta()")
                .Define("RecoPi0M_theta",        "RecoPi0M_p4.Theta()")

                # impact parameter method from CMS for decay into one pion
                # we do know the higgs rest frame / recoil frame so we can use that instead of going around it with the visible taus

                .Define("ZMF_p4",       "RecoPiP_p4 + RecoPiM_p4")
                .Define("ZMF_px",       "ZMF_p4.Px()")
                .Define("ZMF_py",       "ZMF_p4.Py()")
                .Define("ZMF_pz",       "ZMF_p4.Pz()")
                .Define("ZMF_e",       "ZMF_p4.E()")

                .Define("ZMF_RecoPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, RecoPiP_p4)")
                .Define("ZMF_RecoPiP_px",       "ZMF_RecoPiP_p4.Px()")
                .Define("ZMF_RecoPiP_py",       "ZMF_RecoPiP_p4.Py()")
                .Define("ZMF_RecoPiP_pz",       "ZMF_RecoPiP_p4.Pz()")
                .Define("ZMF_RecoPiP_e",       "ZMF_RecoPiP_p4.E()")
                
                .Define("OP_ImpactP_p4",        "FCCAnalyses::ZHfunctions::ImpactFromIP(ChargedTauImpactP_p4, RecoPiP_p4, RecoIP_p4)")
                .Define("OP_ImpactP_px",        "OP_ImpactP_p4.Px()")
                .Define("OP_ImpactP_py",        "OP_ImpactP_p4.Py()")
                .Define("OP_ImpactP_pz",        "OP_ImpactP_p4.Pz()")
                .Define("OP_ImpactP_e",        "OP_ImpactP_p4.E()")

                .Define("ZMF_LambdaP_p4",    "if (RecoPi0P_p4.E()>0) return FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, RecoPi0P_p4); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, OP_ImpactP_p4);")
                .Define("ZMF_LambdaP_px",        "ZMF_LambdaP_p4.Px()")
                .Define("ZMF_LambdaP_py",        "ZMF_LambdaP_p4.Py()")
                .Define("ZMF_LambdaP_pz",        "ZMF_LambdaP_p4.Pz()")
                .Define("ZMF_LambdaP_e",        "ZMF_LambdaP_p4.E()")
                
                .Define("ZMF_LambdaP_par",       "((ZMF_LambdaP_p4.Vect()).Dot((ZMF_RecoPiP_p4.Vect())))/((ZMF_RecoPiP_p4.Vect()).Mag2())*ZMF_RecoPiP_p4.Vect()")
                .Define("ZMF_LambdaP_perp",      "(ZMF_LambdaP_p4.Vect() - ZMF_LambdaP_par).Unit()")
                .Define("ZMF_LambdaP_perp_x",      "ZMF_LambdaP_perp.X()")
                .Define("ZMF_LambdaP_perp_y",      "ZMF_LambdaP_perp.Y()")
                .Define("ZMF_LambdaP_perp_z",      "ZMF_LambdaP_perp.Z()")

                .Define("ZMF_RecoPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, RecoPiM_p4)")
                .Define("ZMF_RecoPiM_px",       "ZMF_RecoPiM_p4.Px()")
                .Define("ZMF_RecoPiM_py",       "ZMF_RecoPiM_p4.Py()")
                .Define("ZMF_RecoPiM_pz",       "ZMF_RecoPiM_p4.Pz()")
                .Define("ZMF_RecoPiM_e",       "ZMF_RecoPiM_p4.E()")

                .Define("OP_ImpactM_p4",        "FCCAnalyses::ZHfunctions::ImpactFromIP(ChargedTauImpactM_p4, RecoPiM_p4, RecoIP_p4)")
                .Define("OP_ImpactM_px",        "OP_ImpactM_p4.Px()")
                .Define("OP_ImpactM_py",        "OP_ImpactM_p4.Py()")
                .Define("OP_ImpactM_pz",        "OP_ImpactM_p4.Pz()")
                .Define("OP_ImpactM_e",        "OP_ImpactM_p4.E()")

                .Define("ZMF_LambdaM_p4",    "if (RecoPi0M_p4.E()>0) return FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, RecoPi0M_p4); else return FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, OP_ImpactM_p4);")
                .Define("ZMF_LambdaM_px",        "ZMF_LambdaM_p4.Px()")
                .Define("ZMF_LambdaM_py",        "ZMF_LambdaM_p4.Py()")
                .Define("ZMF_LambdaM_pz",        "ZMF_LambdaM_p4.Pz()")
                .Define("ZMF_LambdaM_e",        "ZMF_LambdaM_p4.E()")
                
                .Define("ZMF_LambdaM_par",       "((ZMF_LambdaM_p4.Vect()).Dot((ZMF_RecoPiM_p4.Vect())))/((ZMF_RecoPiM_p4.Vect()).Mag2())*ZMF_RecoPiM_p4.Vect()")
                .Define("ZMF_LambdaM_perp",      "(ZMF_LambdaM_p4.Vect() - ZMF_LambdaM_par).Unit()")
                .Define("ZMF_LambdaM_perp_x",      "ZMF_LambdaM_perp.X()")
                .Define("ZMF_LambdaM_perp_y",      "ZMF_LambdaM_perp.Y()")
                .Define("ZMF_LambdaM_perp_z",      "ZMF_LambdaM_perp.Z()")

                .Define("Phi_ZMF",       "acos(ZMF_LambdaP_perp.Dot(ZMF_LambdaM_perp))")
                .Define("y_plus",       "(RecoPiP_p4.E()-RecoPi0P_p4.E())/(RecoPiP_p4.E()+RecoPi0P_p4.E())")
                .Define("y_min",       "(RecoPiM_p4.E()-RecoPi0M_p4.E())/(RecoPiM_p4.E()+RecoPi0M_p4.E())")
                .Define("y_tau",        "(y_plus*y_min)") 
                .Define("O_ZMF",         "((ZMF_RecoPiM_p4.Vect()).Unit()).Dot(ZMF_LambdaP_perp.Cross(ZMF_LambdaM_perp))")

                ## y=1 if both pi0 are not there so it doesn't matter, if one is there then it's the single y, if both are present then it's still what i want
                .Define("PhiCP_y",        "if (y_tau>=0) return Phi_ZMF; else return (-3.1415 + Phi_ZMF);")
                ## if the selection prceeded with the y then it will not have an effect but jsut mirroring an already symmetric function, otherwise the phi_recoil is correclty separated when there is no pi0
                .Define("PhiCP_CMS",        "if (O_ZMF>=0) return PhiCP_y; else return (-PhiCP_y);")

        )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        #branches from stage1 to be kept for histogram booking in final and plotting
        branchList = [
            
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

            "Recoil_mass",
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
        branchList += [

            "RecoPiP_px",
            "RecoPiP_py",
            "RecoPiP_pz",
            "RecoPiP_e",
            "RecoPiP_phi",
            "RecoPiP_eta",
            "RecoPiP_theta",
            "RecoPiP_dx",
            "RecoPiP_dy",
            "RecoPiP_dz",
            "RecoPiP_D0",
            "RecoPiP_Z0",
            "RecoPiP_p",
            "RecoPiP_D0sig",
            "RecoPiP_Z0sig",
            "RecoPiP_charge",

            "RecoPiM_px",
            "RecoPiM_py",
            "RecoPiM_pz",
            "RecoPiM_dx",
            "RecoPiM_dy",
            "RecoPiM_dz",
            "RecoPiM_e",
            "RecoPiM_p",
            "RecoPiM_phi",
            "RecoPiM_eta",
            "RecoPiM_theta",
            "RecoPiM_D0",
            "RecoPiM_Z0",
            "RecoPiM_D0sig",
            "RecoPiM_Z0sig",
            "RecoPiM_charge",

            "RecoPi0P_px",
            "RecoPi0P_py",
            "RecoPi0P_pz",
            "RecoPi0P_e",
            "RecoPi0P_phi",
            "RecoPi0P_eta",
            "RecoPi0P_theta",

            "RecoPi0M_px",
            "RecoPi0M_py",
            "RecoPi0M_pz",
            "RecoPi0M_e",
            "RecoPi0M_phi",
            "RecoPi0M_eta",
            "RecoPi0M_theta",

            "ZMF_px",
            "ZMF_py",
            "ZMF_pz",
            "ZMF_e",

            "OP_ImpactP_px",
            "OP_ImpactP_py",
            "OP_ImpactP_pz",
            "OP_ImpactP_e",

            "OP_ImpactM_px",
            "OP_ImpactM_py",
            "OP_ImpactM_pz",
            "OP_ImpactM_e",

            "ZMF_RecoPiP_px",
            "ZMF_RecoPiP_py",
            "ZMF_RecoPiP_pz",
            "ZMF_RecoPiP_e",

            "ZMF_RecoPiM_px",
            "ZMF_RecoPiM_py",
            "ZMF_RecoPiM_pz",
            "ZMF_RecoPiM_e",

            "ZMF_LambdaP_px",
            "ZMF_LambdaP_py",
            "ZMF_LambdaP_pz",
            "ZMF_LambdaP_e",

            "ZMF_LambdaP_perp_x",
            "ZMF_LambdaP_perp_y",
            "ZMF_LambdaP_perp_z",

            "ZMF_LambdaM_px",
            "ZMF_LambdaM_py",
            "ZMF_LambdaM_pz",
            "ZMF_LambdaM_e",

            "ZMF_LambdaM_perp_x",
            "ZMF_LambdaM_perp_y",
            "ZMF_LambdaM_perp_z",

            "y_tau",
            "y_plus",
            "y_min",
            "Phi_ZMF",
            "O_ZMF",   
            "PhiCP_y",   
            "PhiCP_CMS",

        ]
        return branchList