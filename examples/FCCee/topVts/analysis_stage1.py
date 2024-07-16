import os, copy # tagging

#Mandatory: List of processes
processList = {
#             'wzp6_ee_SM_tt_tWbTWs_tallTlep_ecm365': {'chunks':1, 'fraction':0.0001}
             'wzp6_ee_SM_tt_tWbTWs_tallTlep_ecm365':   {'chunks':6},
             'wzp6_ee_SM_tt_tWbTWs_tallTlight_ecm365': {'chunks':6},
             'wzp6_ee_SM_tt_tWbTWs_tallTheavy_ecm365': {'chunks':6},
             'wzp6_ee_SM_tt_tWsTWb_tlepTall_ecm365':   {'chunks':6},
             'wzp6_ee_SM_tt_tWsTWb_tlightTall_ecm365': {'chunks':6},
             'wzp6_ee_SM_tt_tWsTWb_theavyTall_ecm365': {'chunks':6},

             'wzp6_ee_SM_tt_tlepTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
             'wzp6_ee_SM_tt_tlepThad_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
             'wzp6_ee_SM_tt_thadTlep_noCKMmix_keepPolInfo_ecm365': {'chunks':13},
             'wzp6_ee_SM_tt_thadThad_noCKMmix_keepPolInfo_ecm365': {'chunks':13}

#             'p8_ee_ZZ_ecm365': {'chunks':1, 'fraction':0.0001}
#             'p8_ee_WW_ecm365': {'chunks':50},
#             'p8_ee_ZZ_ecm365': {'chunks':50},

             # ZH samples, no inclusive ones
#             'wzp6_ee_bbH_ecm365': {'chunks':5},
#             'wzp6_ee_ccH_ecm365': {'chunks':5},
#             'wzp6_ee_ssH_ecm365': {'chunks':5},
#             'wzp6_ee_qqH_ecm365': {'chunks':5},
#             'wzp6_ee_tautauH_ecm365': {'chunks':5},
#             'wzp6_ee_mumuH_ecm365': {'chunks':5},
#             'wzp6_ee_eeH_ecm365': {'chunks':5},
#             'wzp6_ee_nunuH_ecm365': {'chunks':5}

            }

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
prodTag     = "FCCee/winter2023/IDEA/"

#Optional: output directory, default is local running directory
outputDir   = "outputs/FCCee/top/topVts/stage1_analysis_tuples/"

#EOS output directory for batch jobs
outputDirEos = "/eos/experiment/fcc/ee/analyses/case-studies/top/topVts/analysis_tuples_2024July10/winter2023"


#Optional
nCPUS       = 8
runBatch    = True
batchQueue = "nextweek"
compGroup = "group_u_FCC.local_gen"


# Additional/custom C++ functions, defined in header files
includePaths = ["functions.h"]

## tagging -------------------------------
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


jetClusteringHelper_kt2   = None
jetClusteringHelper_R5   = None
jetFlavourHelper_kt2   = None
jetFlavourHelper_R5   = None

## tagging ------------------------------



#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        df2 = (df
               .Alias("Particle0", "Particle#0.index")
               .Alias("Particle1", "Particle#1.index")

               .Define("MC_PrimaryVertex",  "FCCAnalyses::MCParticle::get_EventPrimaryVertex(3)( Particle )" )
               .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
               .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
               # the recoParticles corresponding  to the tracks that are primaries, according to MC-matching :
               .Define("MC_PrimaryTracks_RP",  "VertexingUtils::SelPrimaryTracks(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles,Particle, MC_PrimaryVertex)" )
               # and the corresponding tracks :
               .Define("MC_PrimaryTracks",  "ReconstructedParticle2Track::getRP2TRK( MC_PrimaryTracks_RP, EFlowTrack_1)" )
               .Define("n_PrimaryTracks", "ReconstructedParticle::get_n(MC_PrimaryTracks_RP)")

               .Define("genTop",      "FCCAnalyses::MCParticle::sel_pdgID(6, true)(Particle)")
               .Define("genW",        "FCCAnalyses::MCParticle::sel_pdgID(24, true)(Particle)")
               .Define("genBottom",   "FCCAnalyses::MCParticle::sel_pdgID(5, true)(Particle)")
               .Define("genStrange",  "FCCAnalyses::MCParticle::sel_pdgID(3, true)(Particle)")
               .Define("genMuon",     "FCCAnalyses::MCParticle::sel_pdgID(13, true)(Particle)")
               .Define("genElectron", "FCCAnalyses::MCParticle::sel_pdgID(11, true)(Particle)")
               .Define("n_genTops",      "FCCAnalyses::MCParticle::get_n(genTop)")
               .Define("n_genWs",        "FCCAnalyses::MCParticle::get_n(genW)")
               .Define("n_genBottoms",      "FCCAnalyses::MCParticle::get_n(genBottom)")
               .Define("n_genStranges",      "FCCAnalyses::MCParticle::get_n(genStrange)")
               .Define("n_genMuons",     "FCCAnalyses::MCParticle::get_n(genMuon)")
               .Define("n_genElectrons", "FCCAnalyses::MCParticle::get_n(genElectron)")

               .Filter("n_genTops==2")
               .Filter("n_genWs==2")
               #.Filter("n_genBottoms==1")
               #.Filter("n_genStranges==1")

               # This stupid function differentiate antiparticles in mother but only looks for absolute value in daughter
               .Define("Wp_elenu", "FCCAnalyses::MCParticle::get_decay( 24, 11, false)(Particle, Particle1)")
               .Define("Wp_munu",  "FCCAnalyses::MCParticle::get_decay( 24, 13, false)(Particle, Particle1)")
               .Define("Wp_taunu", "FCCAnalyses::MCParticle::get_decay( 24, 15, false)(Particle, Particle1)")
               .Define("Wp_d",     "FCCAnalyses::MCParticle::get_decay( 24, 1,  false)(Particle, Particle1)")
               .Define("Wp_s",     "FCCAnalyses::MCParticle::get_decay( 24, 3,  false)(Particle, Particle1)")
               .Define("Wp_b",     "FCCAnalyses::MCParticle::get_decay( 24, 5,  false)(Particle, Particle1)")
               .Define("Wm_elenu", "FCCAnalyses::MCParticle::get_decay(-24, 11, false)(Particle, Particle1)")
               .Define("Wm_munu",  "FCCAnalyses::MCParticle::get_decay(-24, 13, false)(Particle, Particle1)")
               .Define("Wm_taunu", "FCCAnalyses::MCParticle::get_decay(-24, 15, false)(Particle, Particle1)")
               .Define("Wm_d",     "FCCAnalyses::MCParticle::get_decay(-24, 1,  false)(Particle, Particle1)")
               .Define("Wm_s",     "FCCAnalyses::MCParticle::get_decay(-24, 3,  false)(Particle, Particle1)")
               .Define("Wm_b",     "FCCAnalyses::MCParticle::get_decay(-24, 5,  false)(Particle, Particle1)")

               .Define("genBottom_px",     "FCCAnalyses::MCParticle::get_px(genBottom)")
               .Define("genBottom_py",     "FCCAnalyses::MCParticle::get_py(genBottom)")
               .Define("genBottom_pz",     "FCCAnalyses::MCParticle::get_pz(genBottom)")
               .Define("genBottom_phi",    "FCCAnalyses::MCParticle::get_phi(genBottom)")
               .Define("genBottom_eta",    "FCCAnalyses::MCParticle::get_eta(genBottom)")
               .Define("genBottom_energy", "FCCAnalyses::MCParticle::get_e(genBottom)")
               .Define("genBottom_mass",   "FCCAnalyses::MCParticle::get_mass(genBottom)")
               .Define("genBottom_pdg",    "FCCAnalyses::MCParticle::get_pdg(genBottom)")

               .Define("genStrange_px",     "FCCAnalyses::MCParticle::get_px(genStrange)")
               .Define("genStrange_py",     "FCCAnalyses::MCParticle::get_py(genStrange)")
               .Define("genStrange_pz",     "FCCAnalyses::MCParticle::get_pz(genStrange)")
               .Define("genStrange_phi",    "FCCAnalyses::MCParticle::get_phi(genStrange)")
               .Define("genStrange_eta",    "FCCAnalyses::MCParticle::get_eta(genStrange)")
               .Define("genStrange_energy", "FCCAnalyses::MCParticle::get_e(genStrange)")
               .Define("genStrange_mass",   "FCCAnalyses::MCParticle::get_mass(genStrange)")
               .Define("genStrange_pdg",    "FCCAnalyses::MCParticle::get_pdg(genStrange)")


               .Define("genW_px",     "FCCAnalyses::MCParticle::get_px(genW)")
               .Define("genW_py",     "FCCAnalyses::MCParticle::get_py(genW)")
               .Define("genW_pz",     "FCCAnalyses::MCParticle::get_pz(genW)")
               .Define("genW_phi",    "FCCAnalyses::MCParticle::get_phi(genW)")
               .Define("genW_eta",    "FCCAnalyses::MCParticle::get_eta(genW)")
               .Define("genW_energy", "FCCAnalyses::MCParticle::get_e(genW)")
               .Define("genW_mass",   "FCCAnalyses::MCParticle::get_mass(genW)")
               .Define("genW_charge", "FCCAnalyses::MCParticle::get_charge(genW)")

               .Alias("Muon0",      "Muon#0.index")
               .Alias("Electron0",  "Electron#0.index")
               .Alias("Photon0",    "Photon#0.index")
               .Define("muons",     "ReconstructedParticle::get(Muon0, ReconstructedParticles)")
               .Define("electrons", "ReconstructedParticle::get(Electron0, ReconstructedParticles)")
               .Define("photons",   "ReconstructedParticle::get(Photon0, ReconstructedParticles)")

               .Define("n_muons",     "ReconstructedParticle::get_n(muons)")
               .Define("n_electrons", "ReconstructedParticle::get_n(electrons)")
               .Define("n_photons",   "ReconstructedParticle::get_n(photons)")

               .Define("muon_px",          "ReconstructedParticle::get_px(muons)")
               .Define("muon_py",          "ReconstructedParticle::get_py(muons)")
               .Define("muon_pz",          "ReconstructedParticle::get_pz(muons)")
               .Define("muon_phi",         "ReconstructedParticle::get_phi(muons)")
               .Define("muon_eta",         "ReconstructedParticle::get_eta(muons)")
               .Define("muon_energy",      "ReconstructedParticle::get_e(muons)")
               .Define("muon_mass",        "ReconstructedParticle::get_mass(muons)")
               .Define("muon_charge",      "ReconstructedParticle::get_charge(muons)")

               .Define("electron_px",          "ReconstructedParticle::get_px(electrons)")
               .Define("electron_py",          "ReconstructedParticle::get_py(electrons)")
               .Define("electron_pz",          "ReconstructedParticle::get_pz(electrons)")
               .Define("electron_phi",         "ReconstructedParticle::get_phi(electrons)")
               .Define("electron_eta",         "ReconstructedParticle::get_eta(electrons)")
               .Define("electron_energy",      "ReconstructedParticle::get_e(electrons)")
               .Define("electron_mass",        "ReconstructedParticle::get_mass(electrons)")
               .Define("electron_charge",      "ReconstructedParticle::get_charge(electrons)")

               .Define("muons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons)")
               .Define("muons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(muons_hard, ReconstructedParticles)")
               .Define("muons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(muons_hard, muons_iso)")

               .Define("n_muons_sel",     "ReconstructedParticle::get_n(muons_sel_iso)")
               .Define("muon_1_px",       "if (n_muons_sel>0) return ReconstructedParticle::get_px(muons_sel_iso)[0]; else return float(-99.);")
               .Define("muon_1_py",       "if (n_muons_sel>0) return ReconstructedParticle::get_py(muons_sel_iso)[0]; else return float(-99.);")
               .Define("muon_1_pz",       "if (n_muons_sel>0) return ReconstructedParticle::get_pz(muons_sel_iso)[0]; else return float(-99.);")
               .Define("muon_1_phi",      "if (n_muons_sel>0) return ReconstructedParticle::get_phi(muons_sel_iso)[0]; else return float(-99.);")
               .Define("muon_1_eta",      "if (n_muons_sel>0) return ReconstructedParticle::get_eta(muons_sel_iso)[0]; else return float(-99.);")
               .Define("muon_1_energy",   "if (n_muons_sel>0) return ReconstructedParticle::get_e(muons_sel_iso)[0]; else return float(-99.);")
               .Define("muon_1_charge",   "if (n_muons_sel>0) return ReconstructedParticle::get_charge(muons_sel_iso)[0]; else return float(-99.);")

               .Define("muon_2_px",       "if (n_muons_sel>1) return ReconstructedParticle::get_px(muons_sel_iso)[1]; else return float(-99.);")
               .Define("muon_2_py",       "if (n_muons_sel>1) return ReconstructedParticle::get_py(muons_sel_iso)[1]; else return float(-99.);")
               .Define("muon_2_pz",       "if (n_muons_sel>1) return ReconstructedParticle::get_pz(muons_sel_iso)[1]; else return float(-99.);")
               .Define("muon_2_phi",      "if (n_muons_sel>1) return ReconstructedParticle::get_phi(muons_sel_iso)[1]; else return float(-99.);")
               .Define("muon_2_eta",      "if (n_muons_sel>1) return ReconstructedParticle::get_eta(muons_sel_iso)[1]; else return float(-99.);")
               .Define("muon_2_energy",   "if (n_muons_sel>1) return ReconstructedParticle::get_e(muons_sel_iso)[1]; else return float(-99.);")
               .Define("muon_2_charge",   "if (n_muons_sel>1) return ReconstructedParticle::get_charge(muons_sel_iso)[1]; else return float(-99.);")

               .Define("electrons_hard", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons)")
               .Define("electrons_iso",  "FCCAnalyses::ZHfunctions::coneIsolation(0.01, 0.5)(electrons_hard, ReconstructedParticles)")
               .Define("electrons_sel_iso", "FCCAnalyses::ZHfunctions::sel_iso(0.25)(electrons_hard, electrons_iso)")
            
               .Define("n_electrons_sel",     "ReconstructedParticle::get_n(electrons_sel_iso)")
               .Define("electron_1_px",       "if (n_electrons_sel>0) return ReconstructedParticle::get_px(electrons_sel_iso)[0]; else return float(-99.);")
               .Define("electron_1_py",       "if (n_electrons_sel>0) return ReconstructedParticle::get_py(electrons_sel_iso)[0]; else return float(-99.);")
               .Define("electron_1_pz",       "if (n_electrons_sel>0) return ReconstructedParticle::get_pz(electrons_sel_iso)[0]; else return float(-99.);")
               .Define("electron_1_phi",      "if (n_electrons_sel>0) return ReconstructedParticle::get_phi(electrons_sel_iso)[0]; else return float(-99.);")
               .Define("electron_1_eta",      "if (n_electrons_sel>0) return ReconstructedParticle::get_eta(electrons_sel_iso)[0]; else return float(-99.);")
               .Define("electron_1_energy",   "if (n_electrons_sel>0) return ReconstructedParticle::get_e(electrons_sel_iso)[0]; else return float(-99.);")
               .Define("electron_1_charge",   "if (n_electrons_sel>0) return ReconstructedParticle::get_charge(electrons_sel_iso)[0]; else return float(-99.);")

               .Define("electron_2_px",       "if (n_electrons_sel>1) return ReconstructedParticle::get_px(electrons_sel_iso)[1]; else return float(-99.);")
               .Define("electron_2_py",       "if (n_electrons_sel>1) return ReconstructedParticle::get_py(electrons_sel_iso)[1]; else return float(-99.);")
               .Define("electron_2_pz",       "if (n_electrons_sel>1) return ReconstructedParticle::get_pz(electrons_sel_iso)[1]; else return float(-99.);")
               .Define("electron_2_phi",      "if (n_electrons_sel>1) return ReconstructedParticle::get_phi(electrons_sel_iso)[1]; else return float(-99.);")
               .Define("electron_2_eta",      "if (n_electrons_sel>1) return ReconstructedParticle::get_eta(electrons_sel_iso)[1]; else return float(-99.);")
               .Define("electron_2_energy",   "if (n_electrons_sel>1) return ReconstructedParticle::get_e(electrons_sel_iso)[1]; else return float(-99.);")
               .Define("electron_2_charge",   "if (n_electrons_sel>1) return ReconstructedParticle::get_charge(electrons_sel_iso)[1]; else return float(-99.);")

               .Define("photon_px",          "ReconstructedParticle::get_px(photons)")
               .Define("photon_py",          "ReconstructedParticle::get_py(photons)")
               .Define("photon_pz",          "ReconstructedParticle::get_pz(photons)")
               .Define("photon_phi",          "ReconstructedParticle::get_phi(photons)")
               .Define("photon_eta",          "ReconstructedParticle::get_eta(photons)")
               .Define("photon_energy",      "ReconstructedParticle::get_e(photons)")
               .Define("photon_mass",        "ReconstructedParticle::get_mass(photons)")

               .Define("Emiss_energy",  "ReconstructedParticle::get_e(MissingET)")
               .Define("Emiss_p",       "ReconstructedParticle::get_p(MissingET)")
               .Define("Emiss_px",      "ReconstructedParticle::get_px(MissingET)") #x-component of RecoMissingEnergy
               .Define("Emiss_py",      "ReconstructedParticle::get_py(MissingET)") #y-component of RecoMissingEnergy
               .Define("Emiss_pz",      "ReconstructedParticle::get_pz(MissingET)") #z-component of RecoMissingEnergy
               .Define("Emiss_phi",     "ReconstructedParticle::get_phi(MissingET)")
               .Define("Emiss_eta",     "ReconstructedParticle::get_eta(MissingET)")

               .Define("missingEnergy", "FCCAnalyses::ZHfunctions::missingEnergy(365., ReconstructedParticles)")
               .Define("recoEmiss_px",  "missingEnergy[0].momentum.x")
               .Define("recoEmiss_py",  "missingEnergy[0].momentum.y")
               .Define("recoEmiss_pz",  "missingEnergy[0].momentum.z")
               .Define("recoEmiss_e",   "missingEnergy[0].energy")
        )


        ## tagging ----------------------------------
        df3 = (df2
               .Define("muons_10",     "FCCAnalyses::ReconstructedParticle::sel_p(10)(muons)")
               .Define("electrons_10", "FCCAnalyses::ReconstructedParticle::sel_p(10)(electrons)")
               .Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles,muons_10)")
               .Define("ReconstructedParticlesNoLeps",  "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons,electrons_10)")
        )

        global jetClusteringHelper_kt2
        global jetClusteringHelper_kt4
        global jetClusteringHelper_kt6
        global jetClusteringHelper_R5
        global jetFlavourHelper_kt2
        global jetFlavourHelper_kt4
        global jetFlavourHelper_kt6
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
            collections_noleps["PFParticles"], 2, "kt2"
        )
        jetClusteringHelper_kt4 = ExclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 4, "kt4"
        )
        jetClusteringHelper_kt6 = ExclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 6, "kt6"
        )
        jetClusteringHelper_R5  = InclusiveJetClusteringHelper(
            collections_noleps["PFParticles"], 0.5, 1, "R5"
        )
        df3 = jetClusteringHelper_kt2.define(df3)
        df3 = jetClusteringHelper_kt4.define(df3)
        df3 = jetClusteringHelper_kt6.define(df3)
        df3 = jetClusteringHelper_R5. define(df3)

        ## define jet flavour tagging parameters

        jetFlavourHelper_kt2 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt2.jets,
            jetClusteringHelper_kt2.constituents,
            "kt2",
        )
        jetFlavourHelper_kt4 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt4.jets,
            jetClusteringHelper_kt4.constituents,
            "kt4",
        )
        jetFlavourHelper_kt6 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_kt6.jets,
            jetClusteringHelper_kt6.constituents,
            "kt6",
        )
        jetFlavourHelper_R5 = JetFlavourHelper(
            collections_noleps,
            jetClusteringHelper_R5.jets,
            jetClusteringHelper_R5.constituents,
            "R5",
        )
        ## define observables for tagger
        df3 = jetFlavourHelper_kt2.define(df3)
        df3 = jetFlavourHelper_kt4.define(df3)
        df3 = jetFlavourHelper_kt6.define(df3)
        df3 = jetFlavourHelper_R5. define(df3)

        ## tagger inference
        df3 = jetFlavourHelper_kt2.inference(weaver_preproc, weaver_model, df3)
        df3 = jetFlavourHelper_kt4.inference(weaver_preproc, weaver_model, df3)
        df3 = jetFlavourHelper_kt6.inference(weaver_preproc, weaver_model, df3)
        df3 = jetFlavourHelper_R5. inference(weaver_preproc, weaver_model, df3)

        df3 = (df3.Define("jet_kt2_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt2.jets))
                  .Define("jet_kt2_dPhi_b",       "if (n_genBottoms>0) return (3.1416 - abs(3.1416 - abs(jet_kt2_phi - genBottom_phi.at(0)))); else return (3.1416+jet_kt2_phi);")
                  .Define("jet_kt2_dEta_b",       "if (n_genBottoms>0) return abs(jet_kt2_eta - genBottom_eta.at(0)); else return (99+jet_kt2_eta);")
                  .Define("jet_kt2_dR_b",         "sqrt(jet_kt2_dPhi_b*jet_kt2_dPhi_b + jet_kt2_dEta_b*jet_kt2_dEta_b)")
                  .Define("jet_kt2_dPhi_s",       "if (n_genStranges>0) return (3.1416 - abs(3.1416 - abs(jet_kt2_phi - genStrange_phi.at(0)))); else return (3.1416+jet_kt2_phi);")
                  .Define("jet_kt2_dEta_s",       "if (n_genStranges>0) return abs(jet_kt2_eta - genStrange_eta.at(0)); else return (99+jet_kt2_eta);")
                  .Define("jet_kt2_dR_s",         "sqrt(jet_kt2_dPhi_s*jet_kt2_dPhi_s + jet_kt2_dEta_s*jet_kt2_dEta_s)")
                  .Define("jet_kt2_isSig",        "(jet_kt2_dR_s<0.3) * 1.0")
                  .Define("jet_kt2_Max_mass",     "Max(jet_kt2_mass)")
                  .Define("jet_kt2_Min_energy",   "Min(jet_kt2_energy)")
        )
        df3 = df3.Define("jet_kt2_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt2.jets) )
        df3 = df3.Define("n_jets_kt2",           "return int(jet_kt2_flavor.size())")

        df3 = (df3.Define("jet_kt4_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt4.jets))
                  .Define("jet_kt4_dPhi_b",       "if (n_genBottoms>0) return (3.1416 - abs(3.1416 - abs(jet_kt4_phi - genBottom_phi.at(0)))); else return (3.1416+jet_kt4_phi);")
                  .Define("jet_kt4_dEta_b",       "if (n_genBottoms>0) return abs(jet_kt4_eta - genBottom_eta.at(0)); else return (99+jet_kt4_eta);")
                  .Define("jet_kt4_dR_b",         "sqrt(jet_kt4_dPhi_b*jet_kt4_dPhi_b + jet_kt4_dEta_b*jet_kt4_dEta_b)")
                  .Define("jet_kt4_dPhi_s",       "if (n_genStranges>0) return (3.1416 - abs(3.1416 - abs(jet_kt4_phi - genStrange_phi.at(0)))); else return (3.1416+jet_kt4_phi);")
                  .Define("jet_kt4_dEta_s",       "if (n_genStranges>0) return abs(jet_kt4_eta - genStrange_eta.at(0)); else return (99+jet_kt4_eta);")
                  .Define("jet_kt4_dR_s",         "sqrt(jet_kt4_dPhi_s*jet_kt4_dPhi_s + jet_kt4_dEta_s*jet_kt4_dEta_s)")
                  .Define("jet_kt4_isSig",        "(jet_kt4_dR_s<0.3) * 1.0")
                  .Define("jet_kt4_Max_mass",     "Max(jet_kt4_mass)")
                  .Define("jet_kt4_Min_energy",   "Min(jet_kt4_energy)")
        )
        df3 = df3.Define("jet_kt4_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt4.jets) )
        df3 = df3.Define("n_jets_kt4",           "return int(jet_kt4_flavor.size())")

        df3 = (df3.Define("jet_kt6_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_kt6.jets))
                  .Define("jet_kt6_dPhi_b",       "if (n_genBottoms>0) return (3.1416 - abs(3.1416 - abs(jet_kt6_phi - genBottom_phi.at(0)))); else return (3.1416+jet_kt6_phi);")
                  .Define("jet_kt6_dEta_b",       "if (n_genBottoms>0) return abs(jet_kt6_eta - genBottom_eta.at(0)); else return (99+jet_kt6_eta);")
                  .Define("jet_kt6_dR_b",         "sqrt(jet_kt6_dPhi_b*jet_kt6_dPhi_b + jet_kt6_dEta_b*jet_kt6_dEta_b)")
                  .Define("jet_kt6_dPhi_s",       "if (n_genStranges>0) return (3.1416 - abs(3.1416 - abs(jet_kt6_phi - genStrange_phi.at(0)))); else return (3.1416+jet_kt6_phi);")
                  .Define("jet_kt6_dEta_s",       "if (n_genStranges>0) return abs(jet_kt6_eta - genStrange_eta.at(0)); else return (99+jet_kt6_eta);")
                  .Define("jet_kt6_dR_s",         "sqrt(jet_kt6_dPhi_s*jet_kt6_dPhi_s + jet_kt6_dEta_s*jet_kt6_dEta_s)")
                  .Define("jet_kt6_isSig",        "(jet_kt6_dR_s<0.3) * 1.0")
                  .Define("jet_kt6_Max_mass",     "Max(jet_kt6_mass)")
                  .Define("jet_kt6_Min_energy",   "Min(jet_kt6_energy)")
        )
        df3 = df3.Define("jet_kt6_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_kt6.jets) )
        df3 = df3.Define("n_jets_kt6",           "return int(jet_kt6_flavor.size())")

        df3 = (df3.Define("jet_R5_px",           "JetClusteringUtils::get_px({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_py",           "JetClusteringUtils::get_py({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_pz",           "JetClusteringUtils::get_pz({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_phi",          "JetClusteringUtils::get_phi({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_eta",          "JetClusteringUtils::get_eta({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_energy",       "JetClusteringUtils::get_e({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_mass",         "JetClusteringUtils::get_m({})".format(jetClusteringHelper_R5.jets))
                  .Define("jet_R5_dPhi_b",       "if (n_genBottoms>0) return (3.1416 - abs(3.1416 - abs(jet_R5_phi - genBottom_phi.at(0)))); else return (3.1416+jet_R5_phi);")
                  .Define("jet_R5_dEta_b",       "if (n_genBottoms>0) return abs(jet_R5_eta - genBottom_eta.at(0)); else return (99+jet_R5_eta);")
                  .Define("jet_R5_dR_b",         "sqrt(jet_R5_dPhi_b*jet_R5_dPhi_b + jet_R5_dEta_b*jet_R5_dEta_b)")
                  .Define("jet_R5_dPhi_s",       "if (n_genStranges>0) return (3.1416 - abs(3.1416 - abs(jet_R5_phi - genStrange_phi.at(0)))); else return (3.1416+jet_R5_phi);")
                  .Define("jet_R5_dEta_s",       "if (n_genStranges>0) return abs(jet_R5_eta - genStrange_eta.at(0)); else return (99+jet_R5_eta);")
                  .Define("jet_R5_dR_s",         "sqrt(jet_R5_dPhi_s*jet_R5_dPhi_s + jet_R5_dEta_s*jet_R5_dEta_s)")

        )
        df3 = df3.Define("jet_R5_flavor", "JetTaggingUtils::get_flavour({}, Particle)".format(jetClusteringHelper_R5.jets) )
        df3 = df3.Define("n_jets_R5",           "return int(jet_R5_flavor.size())")

        ## tagging ----------------------------------

        ## jet selection
        df3 = (df3.Define("jet_R5_pass", "(jet_R5_mass<50 and jet_R5_energy>15) * 1.0")
                  .Define("jet_pass_px",     "jet_R5_px[jet_R5_pass==1]")
                  .Define("jet_pass_py",     "jet_R5_py[jet_R5_pass==1]")
                  .Define("jet_pass_pz",     "jet_R5_pz[jet_R5_pass==1]")
                  .Define("jet_pass_phi",    "jet_R5_phi[jet_R5_pass==1]")
                  .Define("jet_pass_eta",    "jet_R5_eta[jet_R5_pass==1]")
                  .Define("jet_pass_energy", "jet_R5_energy[jet_R5_pass==1]")
                  .Define("jet_pass_mass",   "jet_R5_mass[jet_R5_pass==1]")
                  .Define("jet_pass_dR_b",   "jet_R5_dR_b[jet_R5_pass==1]")
                  .Define("jet_pass_dR_s",   "jet_R5_dR_s[jet_R5_pass==1]")
                  .Define("jet_pass_isSig",  "(jet_pass_dR_s<0.3) * 1.0")
                  .Define("jet_pass_flavor", "jet_R5_flavor[jet_R5_pass==1]")
                  .Define("jet_pass_isG",    "recojet_isG_R5[jet_R5_pass==1]")
                  .Define("jet_pass_isQ",    "recojet_isQ_R5[jet_R5_pass==1]")
                  .Define("jet_pass_isS",    "recojet_isS_R5[jet_R5_pass==1]")
                  .Define("jet_pass_isC",    "recojet_isC_R5[jet_R5_pass==1]")
                  .Define("jet_pass_isB",    "recojet_isB_R5[jet_R5_pass==1]")
                  .Define("n_jets_pass",     "return int(jet_pass_flavor.size())") #size() returns size_t, pandas does not recognize it
        )
        ## jet selection


        ## event selection
        df3 = (df3.Define("dilep_cat",   "(n_muons_sel+n_electrons_sel==2 and n_jets_kt2==2) * 1.0")
                  .Define("semilep_cat", "(n_muons_sel+n_electrons_sel==1 and n_jets_kt4==4) * 1.0")
                  .Define("dihad_cat",   "(n_muons_sel+n_electrons_sel==0 and n_jets_kt6==6) * 1.0")
        )
        df3 = (df3.Define("n_btags", "int(jet_pass_mass[jet_pass_isB>0.5].size())")
                  .Define("n_ctags", "int(jet_pass_mass[jet_pass_isC>0.5].size())")
                  .Define("n_stags", "int(jet_pass_mass[jet_pass_isS>0.5].size())")
                  .Define("jet_leadS_idx", "for (int i=0; i<jet_pass_mass.size();++i) {if (jet_pass_isS.at(i) == Max(jet_pass_isS)) return i;} return 0;")
                  .Define("jet_leadS_px",     "if (n_jets_pass>0) return (float)jet_pass_px.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_py",     "if (n_jets_pass>0) return (float)jet_pass_py.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_pz",     "if (n_jets_pass>0) return (float)jet_pass_pz.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_phi",    "if (n_jets_pass>0) return (float)jet_pass_phi.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_eta",    "if (n_jets_pass>0) return (float)jet_pass_eta.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_energy", "if (n_jets_pass>0) return (float)jet_pass_energy.at(jet_leadS_idx); else return float{-99.};")
                  .Define("jet_leadS_mass",   "if (n_jets_pass>0) return (float)jet_pass_mass.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_dR_b",   "if (n_jets_pass>0) return (float)jet_pass_dR_b.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_dR_s",   "if (n_jets_pass>0) return (float)jet_pass_dR_s.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_isSig",  "if (n_jets_pass>0) return (float)jet_pass_isSig.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_flavor", "if (n_jets_pass>0) return (float)jet_pass_flavor.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_isG",    "if (n_jets_pass>0) return (float)jet_pass_isG.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_isQ",    "if (n_jets_pass>0) return (float)jet_pass_isQ.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_isS",    "if (n_jets_pass>0) return (float)jet_pass_isS.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_isC",    "if (n_jets_pass>0) return (float)jet_pass_isC.at(jet_leadS_idx); else return float(-99.);")
                  .Define("jet_leadS_isB",    "if (n_jets_pass>0) return (float)jet_pass_isB.at(jet_leadS_idx); else return float(-99.);")

                  .Define("jet_subS_idx", "float max_S = 0.0; int idx = 0; for (int i=0; i<jet_pass_mass.size();++i) {if (jet_pass_isS.at(i) > max_S and jet_pass_isS.at(i) != Max(jet_pass_isS)) {max_S = jet_pass_isS.at(i); idx = i;}} return idx;")
                  .Define("jet_subS_px",     "if (n_jets_pass>0) return (float)jet_pass_px.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_py",     "if (n_jets_pass>0) return (float)jet_pass_py.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_pz",     "if (n_jets_pass>0) return (float)jet_pass_pz.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_phi",    "if (n_jets_pass>0) return (float)jet_pass_phi.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_eta",    "if (n_jets_pass>0) return (float)jet_pass_eta.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_energy", "if (n_jets_pass>0) return (float)jet_pass_energy.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_mass",   "if (n_jets_pass>0) return (float)jet_pass_mass.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_dR_b",   "if (n_jets_pass>0) return (float)jet_pass_dR_b.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_dR_s",   "if (n_jets_pass>0) return (float)jet_pass_dR_s.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_isSig",  "if (n_jets_pass>0) return (float)jet_pass_isSig.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_flavor", "if (n_jets_pass>0) return (float)jet_pass_flavor.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_isG",    "if (n_jets_pass>0) return (float)jet_pass_isG.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_isQ",    "if (n_jets_pass>0) return (float)jet_pass_isQ.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_isS",    "if (n_jets_pass>0) return (float)jet_pass_isS.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_isC",    "if (n_jets_pass>0) return (float)jet_pass_isC.at(jet_subS_idx); else return float(-99.);")
                  .Define("jet_subS_isB",    "if (n_jets_pass>0) return (float)jet_pass_isB.at(jet_subS_idx); else return float(-99.);")

                  .Define("jet_leadC_idx", "for (int i=0; i<jet_pass_mass.size();++i) {if (jet_pass_isC.at(i) == Max(jet_pass_isC)) return i;} return 0;")
                  .Define("jet_leadC_px",     "if (n_jets_pass>0) return (float)jet_pass_px.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_py",     "if (n_jets_pass>0) return (float)jet_pass_py.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_pz",     "if (n_jets_pass>0) return (float)jet_pass_pz.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_phi",    "if (n_jets_pass>0) return (float)jet_pass_phi.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_eta",    "if (n_jets_pass>0) return (float)jet_pass_eta.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_energy", "if (n_jets_pass>0) return (float)jet_pass_energy.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_mass",   "if (n_jets_pass>0) return (float)jet_pass_mass.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_dR_b",   "if (n_jets_pass>0) return (float)jet_pass_dR_b.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_dR_s",   "if (n_jets_pass>0) return (float)jet_pass_dR_s.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_isSig",  "if (n_jets_pass>0) return (float)jet_pass_isSig.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_flavor", "if (n_jets_pass>0) return (float)jet_pass_flavor.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_isG",    "if (n_jets_pass>0) return (float)jet_pass_isG.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_isQ",    "if (n_jets_pass>0) return (float)jet_pass_isQ.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_isS",    "if (n_jets_pass>0) return (float)jet_pass_isS.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_isC",    "if (n_jets_pass>0) return (float)jet_pass_isC.at(jet_leadC_idx); else return float(-99.);")
                  .Define("jet_leadC_isB",    "if (n_jets_pass>0) return (float)jet_pass_isB.at(jet_leadC_idx); else return float(-99.);")

                  .Define("jet_subC_idx", "float max_C = 0.0; int idx = 0; for (int i=0; i<jet_pass_mass.size();++i) {if (jet_pass_isC.at(i) > max_C and jet_pass_isC.at(i) != Max(jet_pass_isC)) {max_C = jet_pass_isC.at(i); idx = i;}} return idx;")
                  .Define("jet_subC_px",     "if (n_jets_pass>0) return (float)jet_pass_px.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_py",     "if (n_jets_pass>0) return (float)jet_pass_py.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_pz",     "if (n_jets_pass>0) return (float)jet_pass_pz.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_phi",    "if (n_jets_pass>0) return (float)jet_pass_phi.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_eta",    "if (n_jets_pass>0) return (float)jet_pass_eta.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_energy", "if (n_jets_pass>0) return (float)jet_pass_energy.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_mass",   "if (n_jets_pass>0) return (float)jet_pass_mass.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_dR_b",   "if (n_jets_pass>0) return (float)jet_pass_dR_b.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_dR_s",   "if (n_jets_pass>0) return (float)jet_pass_dR_s.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_isSig",  "if (n_jets_pass>0) return (float)jet_pass_isSig.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_flavor", "if (n_jets_pass>0) return (float)jet_pass_flavor.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_isG",    "if (n_jets_pass>0) return (float)jet_pass_isG.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_isQ",    "if (n_jets_pass>0) return (float)jet_pass_isQ.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_isS",    "if (n_jets_pass>0) return (float)jet_pass_isS.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_isC",    "if (n_jets_pass>0) return (float)jet_pass_isC.at(jet_subC_idx); else return float(-99.);")
                  .Define("jet_subC_isB",    "if (n_jets_pass>0) return (float)jet_pass_isB.at(jet_subC_idx); else return float(-99.);")
        )


        df3 = (df3.Define("n_btags_kt2", "int(jet_kt2_mass[recojet_isB_kt2>0.5].size())")
                  .Define("n_ctags_kt2", "int(jet_kt2_mass[recojet_isC_kt2>0.5].size())")
                  .Define("n_stags_kt2", "int(jet_kt2_mass[recojet_isS_kt2>0.5].size())")
                  .Define("jet_kt2_leadS_idx", "for (int i=0; i<jet_kt2_mass.size();++i) {if (recojet_isS_kt2.at(i) == Max(recojet_isS_kt2)) return i;} return 0;")
                  .Define("jet_kt2_leadS_px",     "if (n_jets_kt2>0) return (float)jet_kt2_px.at     (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_py",     "if (n_jets_kt2>0) return (float)jet_kt2_py.at     (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_pz",     "if (n_jets_kt2>0) return (float)jet_kt2_pz.at     (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_phi",    "if (n_jets_kt2>0) return (float)jet_kt2_phi.at    (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_eta",    "if (n_jets_kt2>0) return (float)jet_kt2_eta.at    (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_energy", "if (n_jets_kt2>0) return (float)jet_kt2_energy.at (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_mass",   "if (n_jets_kt2>0) return (float)jet_kt2_mass.at   (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_dR_b",   "if (n_jets_kt2>0) return (float)jet_kt2_dR_b.at   (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_dR_s",   "if (n_jets_kt2>0) return (float)jet_kt2_dR_s.at   (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_isSig",  "if (n_jets_kt2>0) return (float)jet_kt2_isSig.at  (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_flavor", "if (n_jets_kt2>0) return (float)jet_kt2_flavor.at (jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_isG",    "if (n_jets_kt2>0) return (float)recojet_isG_kt2.at(jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_isQ",    "if (n_jets_kt2>0) return (float)recojet_isQ_kt2.at(jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_isS",    "if (n_jets_kt2>0) return (float)recojet_isS_kt2.at(jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_isC",    "if (n_jets_kt2>0) return (float)recojet_isC_kt2.at(jet_kt2_leadS_idx); else return float(-99.);")
                  .Define("jet_kt2_leadS_isB",    "if (n_jets_kt2>0) return (float)recojet_isB_kt2.at(jet_kt2_leadS_idx); else return float(-99.);")

                  .Define("jet_kt2_subS_idx", "float max_S = 0.0; int idx = 0; for (int i=0; i<jet_kt2_mass.size();++i) {if (recojet_isS_kt2.at(i) > max_S and recojet_isS_kt2.at(i) != Max(recojet_isS_kt2)) {max_S = recojet_isS_kt2.at(i); idx = i;}} return idx;")
                  .Define("jet_kt2_subS_px",     "if (n_jets_kt2>0) return (float)jet_kt2_px.at     (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_py",     "if (n_jets_kt2>0) return (float)jet_kt2_py.at     (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_pz",     "if (n_jets_kt2>0) return (float)jet_kt2_pz.at     (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_phi",    "if (n_jets_kt2>0) return (float)jet_kt2_phi.at    (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_eta",    "if (n_jets_kt2>0) return (float)jet_kt2_eta.at    (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_energy", "if (n_jets_kt2>0) return (float)jet_kt2_energy.at (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_mass",   "if (n_jets_kt2>0) return (float)jet_kt2_mass.at   (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_dR_b",   "if (n_jets_kt2>0) return (float)jet_kt2_dR_b.at   (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_dR_s",   "if (n_jets_kt2>0) return (float)jet_kt2_dR_s.at   (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_isSig",  "if (n_jets_kt2>0) return (float)jet_kt2_isSig.at  (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_flavor", "if (n_jets_kt2>0) return (float)jet_kt2_flavor.at (jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_isG",    "if (n_jets_kt2>0) return (float)recojet_isG_kt2.at(jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_isQ",    "if (n_jets_kt2>0) return (float)recojet_isQ_kt2.at(jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_isS",    "if (n_jets_kt2>0) return (float)recojet_isS_kt2.at(jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_isC",    "if (n_jets_kt2>0) return (float)recojet_isC_kt2.at(jet_kt2_subS_idx); else return float(-99.);")
                  .Define("jet_kt2_subS_isB",    "if (n_jets_kt2>0) return (float)recojet_isB_kt2.at(jet_kt2_subS_idx); else return float(-99.);")

                  .Define("jet_kt2_leadC_idx", "for (int i=0; i<jet_kt2_mass.size();++i) {if (recojet_isC_kt2.at(i) == Max(recojet_isC_kt2)) return i;} return 0;")
                  .Define("jet_kt2_leadC_px",     "if (n_jets_kt2>0) return (float)jet_kt2_px.at     (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_py",     "if (n_jets_kt2>0) return (float)jet_kt2_py.at     (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_pz",     "if (n_jets_kt2>0) return (float)jet_kt2_pz.at     (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_phi",    "if (n_jets_kt2>0) return (float)jet_kt2_phi.at    (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_eta",    "if (n_jets_kt2>0) return (float)jet_kt2_eta.at    (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_energy", "if (n_jets_kt2>0) return (float)jet_kt2_energy.at (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_mass",   "if (n_jets_kt2>0) return (float)jet_kt2_mass.at   (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_dR_b",   "if (n_jets_kt2>0) return (float)jet_kt2_dR_b.at   (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_dR_s",   "if (n_jets_kt2>0) return (float)jet_kt2_dR_s.at   (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_isSig",  "if (n_jets_kt2>0) return (float)jet_kt2_isSig.at  (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_flavor", "if (n_jets_kt2>0) return (float)jet_kt2_flavor.at (jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_isG",    "if (n_jets_kt2>0) return (float)recojet_isG_kt2.at(jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_isQ",    "if (n_jets_kt2>0) return (float)recojet_isQ_kt2.at(jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_isS",    "if (n_jets_kt2>0) return (float)recojet_isS_kt2.at(jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_isC",    "if (n_jets_kt2>0) return (float)recojet_isC_kt2.at(jet_kt2_leadC_idx); else return float(-99.);")
                  .Define("jet_kt2_leadC_isB",    "if (n_jets_kt2>0) return (float)recojet_isB_kt2.at(jet_kt2_leadC_idx); else return float(-99.);")

                  .Define("jet_kt2_subC_idx", "float max_C = 0.0; int idx = 0; for (int i=0; i<jet_kt2_mass.size();++i) {if (recojet_isC_kt2.at(i) > max_C and recojet_isC_kt2.at(i) != Max(recojet_isC_kt2)) {max_C = recojet_isC_kt2.at(i); idx = i;}} return idx;")
                  .Define("jet_kt2_subC_px",     "if (n_jets_kt2>0) return (float)jet_kt2_px.at     (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_py",     "if (n_jets_kt2>0) return (float)jet_kt2_py.at     (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_pz",     "if (n_jets_kt2>0) return (float)jet_kt2_pz.at     (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_phi",    "if (n_jets_kt2>0) return (float)jet_kt2_phi.at    (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_eta",    "if (n_jets_kt2>0) return (float)jet_kt2_eta.at    (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_energy", "if (n_jets_kt2>0) return (float)jet_kt2_energy.at (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_mass",   "if (n_jets_kt2>0) return (float)jet_kt2_mass.at   (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_dR_b",   "if (n_jets_kt2>0) return (float)jet_kt2_dR_b.at   (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_dR_s",   "if (n_jets_kt2>0) return (float)jet_kt2_dR_s.at   (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_isSig",  "if (n_jets_kt2>0) return (float)jet_kt2_isSig.at  (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_flavor", "if (n_jets_kt2>0) return (float)jet_kt2_flavor.at (jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_isG",    "if (n_jets_kt2>0) return (float)recojet_isG_kt2.at(jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_isQ",    "if (n_jets_kt2>0) return (float)recojet_isQ_kt2.at(jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_isS",    "if (n_jets_kt2>0) return (float)recojet_isS_kt2.at(jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_isC",    "if (n_jets_kt2>0) return (float)recojet_isC_kt2.at(jet_kt2_subC_idx); else return float(-99.);")
                  .Define("jet_kt2_subC_isB",    "if (n_jets_kt2>0) return (float)recojet_isB_kt2.at(jet_kt2_subC_idx); else return float(-99.);")
        )

        df3 = (df3.Define("n_btags_kt4", "int(jet_kt4_mass[recojet_isB_kt4>0.5].size())")
                  .Define("n_ctags_kt4", "int(jet_kt4_mass[recojet_isC_kt4>0.5].size())")
                  .Define("n_stags_kt4", "int(jet_kt4_mass[recojet_isS_kt4>0.5].size())")
                  .Define("jet_kt4_leadS_idx", "for (int i=0; i<jet_kt4_mass.size();++i) {if (recojet_isS_kt4.at(i) == Max(recojet_isS_kt4)) return i;} return 0;")
                  .Define("jet_kt4_leadS_px",     "if (n_jets_kt4>0) return (float)jet_kt4_px.at     (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_py",     "if (n_jets_kt4>0) return (float)jet_kt4_py.at     (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_pz",     "if (n_jets_kt4>0) return (float)jet_kt4_pz.at     (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_phi",    "if (n_jets_kt4>0) return (float)jet_kt4_phi.at    (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_eta",    "if (n_jets_kt4>0) return (float)jet_kt4_eta.at    (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_energy", "if (n_jets_kt4>0) return (float)jet_kt4_energy.at (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_mass",   "if (n_jets_kt4>0) return (float)jet_kt4_mass.at   (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_dR_b",   "if (n_jets_kt4>0) return (float)jet_kt4_dR_b.at   (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_dR_s",   "if (n_jets_kt4>0) return (float)jet_kt4_dR_s.at   (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_isSig",  "if (n_jets_kt4>0) return (float)jet_kt4_isSig.at  (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_flavor", "if (n_jets_kt4>0) return (float)jet_kt4_flavor.at (jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_isG",    "if (n_jets_kt4>0) return (float)recojet_isG_kt4.at(jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_isQ",    "if (n_jets_kt4>0) return (float)recojet_isQ_kt4.at(jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_isS",    "if (n_jets_kt4>0) return (float)recojet_isS_kt4.at(jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_isC",    "if (n_jets_kt4>0) return (float)recojet_isC_kt4.at(jet_kt4_leadS_idx); else return float(-99.);")
                  .Define("jet_kt4_leadS_isB",    "if (n_jets_kt4>0) return (float)recojet_isB_kt4.at(jet_kt4_leadS_idx); else return float(-99.);")

                  .Define("jet_kt4_subS_idx", "float max_S = 0.0; int idx = 0; for (int i=0; i<jet_kt4_mass.size();++i) {if (recojet_isS_kt4.at(i) > max_S and recojet_isS_kt4.at(i) != Max(recojet_isS_kt4)) {max_S = recojet_isS_kt4.at(i); idx = i;}} return idx;")
                  .Define("jet_kt4_subS_px",     "if (n_jets_kt4>0) return (float)jet_kt4_px.at     (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_py",     "if (n_jets_kt4>0) return (float)jet_kt4_py.at     (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_pz",     "if (n_jets_kt4>0) return (float)jet_kt4_pz.at     (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_phi",    "if (n_jets_kt4>0) return (float)jet_kt4_phi.at    (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_eta",    "if (n_jets_kt4>0) return (float)jet_kt4_eta.at    (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_energy", "if (n_jets_kt4>0) return (float)jet_kt4_energy.at (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_mass",   "if (n_jets_kt4>0) return (float)jet_kt4_mass.at   (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_dR_b",   "if (n_jets_kt4>0) return (float)jet_kt4_dR_b.at   (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_dR_s",   "if (n_jets_kt4>0) return (float)jet_kt4_dR_s.at   (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_isSig",  "if (n_jets_kt4>0) return (float)jet_kt4_isSig.at  (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_flavor", "if (n_jets_kt4>0) return (float)jet_kt4_flavor.at (jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_isG",    "if (n_jets_kt4>0) return (float)recojet_isG_kt4.at(jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_isQ",    "if (n_jets_kt4>0) return (float)recojet_isQ_kt4.at(jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_isS",    "if (n_jets_kt4>0) return (float)recojet_isS_kt4.at(jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_isC",    "if (n_jets_kt4>0) return (float)recojet_isC_kt4.at(jet_kt4_subS_idx); else return float(-99.);")
                  .Define("jet_kt4_subS_isB",    "if (n_jets_kt4>0) return (float)recojet_isB_kt4.at(jet_kt4_subS_idx); else return float(-99.);")

                  .Define("jet_kt4_leadC_idx", "for (int i=0; i<jet_kt4_mass.size();++i) {if (recojet_isC_kt4.at(i) == Max(recojet_isC_kt4)) return i;} return 0;")
                  .Define("jet_kt4_leadC_px",     "if (n_jets_kt4>0) return (float)jet_kt4_px.at     (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_py",     "if (n_jets_kt4>0) return (float)jet_kt4_py.at     (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_pz",     "if (n_jets_kt4>0) return (float)jet_kt4_pz.at     (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_phi",    "if (n_jets_kt4>0) return (float)jet_kt4_phi.at    (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_eta",    "if (n_jets_kt4>0) return (float)jet_kt4_eta.at    (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_energy", "if (n_jets_kt4>0) return (float)jet_kt4_energy.at (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_mass",   "if (n_jets_kt4>0) return (float)jet_kt4_mass.at   (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_dR_b",   "if (n_jets_kt4>0) return (float)jet_kt4_dR_b.at   (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_dR_s",   "if (n_jets_kt4>0) return (float)jet_kt4_dR_s.at   (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_isSig",  "if (n_jets_kt4>0) return (float)jet_kt4_isSig.at  (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_flavor", "if (n_jets_kt4>0) return (float)jet_kt4_flavor.at (jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_isG",    "if (n_jets_kt4>0) return (float)recojet_isG_kt4.at(jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_isQ",    "if (n_jets_kt4>0) return (float)recojet_isQ_kt4.at(jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_isS",    "if (n_jets_kt4>0) return (float)recojet_isS_kt4.at(jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_isC",    "if (n_jets_kt4>0) return (float)recojet_isC_kt4.at(jet_kt4_leadC_idx); else return float(-99.);")
                  .Define("jet_kt4_leadC_isB",    "if (n_jets_kt4>0) return (float)recojet_isB_kt4.at(jet_kt4_leadC_idx); else return float(-99.);")

                  .Define("jet_kt4_subC_idx", "float max_C = 0.0; int idx = 0; for (int i=0; i<jet_kt4_mass.size();++i) {if (recojet_isC_kt4.at(i) > max_C and recojet_isC_kt4.at(i) != Max(recojet_isC_kt4)) {max_C = recojet_isC_kt4.at(i); idx = i;}} return idx;")
                  .Define("jet_kt4_subC_px",     "if (n_jets_kt4>0) return (float)jet_kt4_px.at     (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_py",     "if (n_jets_kt4>0) return (float)jet_kt4_py.at     (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_pz",     "if (n_jets_kt4>0) return (float)jet_kt4_pz.at     (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_phi",    "if (n_jets_kt4>0) return (float)jet_kt4_phi.at    (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_eta",    "if (n_jets_kt4>0) return (float)jet_kt4_eta.at    (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_energy", "if (n_jets_kt4>0) return (float)jet_kt4_energy.at (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_mass",   "if (n_jets_kt4>0) return (float)jet_kt4_mass.at   (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_dR_b",   "if (n_jets_kt4>0) return (float)jet_kt4_dR_b.at   (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_dR_s",   "if (n_jets_kt4>0) return (float)jet_kt4_dR_s.at   (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_isSig",  "if (n_jets_kt4>0) return (float)jet_kt4_isSig.at  (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_flavor", "if (n_jets_kt4>0) return (float)jet_kt4_flavor.at (jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_isG",    "if (n_jets_kt4>0) return (float)recojet_isG_kt4.at(jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_isQ",    "if (n_jets_kt4>0) return (float)recojet_isQ_kt4.at(jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_isS",    "if (n_jets_kt4>0) return (float)recojet_isS_kt4.at(jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_isC",    "if (n_jets_kt4>0) return (float)recojet_isC_kt4.at(jet_kt4_subC_idx); else return float(-99.);")
                  .Define("jet_kt4_subC_isB",    "if (n_jets_kt4>0) return (float)recojet_isB_kt4.at(jet_kt4_subC_idx); else return float(-99.);")
        )

        df3 = (df3.Define("n_btags_kt6", "int(jet_kt6_mass[recojet_isB_kt6>0.5].size())")
                  .Define("n_ctags_kt6", "int(jet_kt6_mass[recojet_isC_kt6>0.5].size())")
                  .Define("n_stags_kt6", "int(jet_kt6_mass[recojet_isS_kt6>0.5].size())")
                  .Define("jet_kt6_leadS_idx", "for (int i=0; i<jet_kt6_mass.size();++i) {if (recojet_isS_kt6.at(i) == Max(recojet_isS_kt6)) return i;} return 0;")
                  .Define("jet_kt6_leadS_px",     "if (n_jets_kt6>0) return (float)jet_kt6_px.at     (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_py",     "if (n_jets_kt6>0) return (float)jet_kt6_py.at     (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_pz",     "if (n_jets_kt6>0) return (float)jet_kt6_pz.at     (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_phi",    "if (n_jets_kt6>0) return (float)jet_kt6_phi.at    (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_eta",    "if (n_jets_kt6>0) return (float)jet_kt6_eta.at    (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_energy", "if (n_jets_kt6>0) return (float)jet_kt6_energy.at (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_mass",   "if (n_jets_kt6>0) return (float)jet_kt6_mass.at   (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_dR_b",   "if (n_jets_kt6>0) return (float)jet_kt6_dR_b.at   (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_dR_s",   "if (n_jets_kt6>0) return (float)jet_kt6_dR_s.at   (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_isSig",  "if (n_jets_kt6>0) return (float)jet_kt6_isSig.at  (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_flavor", "if (n_jets_kt6>0) return (float)jet_kt6_flavor.at (jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_isG",    "if (n_jets_kt6>0) return (float)recojet_isG_kt6.at(jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_isQ",    "if (n_jets_kt6>0) return (float)recojet_isQ_kt6.at(jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_isS",    "if (n_jets_kt6>0) return (float)recojet_isS_kt6.at(jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_isC",    "if (n_jets_kt6>0) return (float)recojet_isC_kt6.at(jet_kt6_leadS_idx); else return float(-99.);")
                  .Define("jet_kt6_leadS_isB",    "if (n_jets_kt6>0) return (float)recojet_isB_kt6.at(jet_kt6_leadS_idx); else return float(-99.);")

                  .Define("jet_kt6_subS_idx", "float max_S = 0.0; int idx = 0; for (int i=0; i<jet_kt6_mass.size();++i) {if (recojet_isS_kt6.at(i) > max_S and recojet_isS_kt6.at(i) != Max(recojet_isS_kt6)) {max_S = recojet_isS_kt6.at(i); idx = i;}} return idx;")
                  .Define("jet_kt6_subS_px",     "if (n_jets_kt6>0) return (float)jet_kt6_px.at     (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_py",     "if (n_jets_kt6>0) return (float)jet_kt6_py.at     (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_pz",     "if (n_jets_kt6>0) return (float)jet_kt6_pz.at     (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_phi",    "if (n_jets_kt6>0) return (float)jet_kt6_phi.at    (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_eta",    "if (n_jets_kt6>0) return (float)jet_kt6_eta.at    (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_energy", "if (n_jets_kt6>0) return (float)jet_kt6_energy.at (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_mass",   "if (n_jets_kt6>0) return (float)jet_kt6_mass.at   (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_dR_b",   "if (n_jets_kt6>0) return (float)jet_kt6_dR_b.at   (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_dR_s",   "if (n_jets_kt6>0) return (float)jet_kt6_dR_s.at   (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_isSig",  "if (n_jets_kt6>0) return (float)jet_kt6_isSig.at  (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_flavor", "if (n_jets_kt6>0) return (float)jet_kt6_flavor.at (jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_isG",    "if (n_jets_kt6>0) return (float)recojet_isG_kt6.at(jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_isQ",    "if (n_jets_kt6>0) return (float)recojet_isQ_kt6.at(jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_isS",    "if (n_jets_kt6>0) return (float)recojet_isS_kt6.at(jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_isC",    "if (n_jets_kt6>0) return (float)recojet_isC_kt6.at(jet_kt6_subS_idx); else return float(-99.);")
                  .Define("jet_kt6_subS_isB",    "if (n_jets_kt6>0) return (float)recojet_isB_kt6.at(jet_kt6_subS_idx); else return float(-99.);")

                  .Define("jet_kt6_leadC_idx", "for (int i=0; i<jet_kt6_mass.size();++i) {if (recojet_isC_kt6.at(i) == Max(recojet_isC_kt6)) return i;} return 0;")
                  .Define("jet_kt6_leadC_px",     "if (n_jets_kt6>0) return (float)jet_kt6_px.at     (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_py",     "if (n_jets_kt6>0) return (float)jet_kt6_py.at     (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_pz",     "if (n_jets_kt6>0) return (float)jet_kt6_pz.at     (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_phi",    "if (n_jets_kt6>0) return (float)jet_kt6_phi.at    (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_eta",    "if (n_jets_kt6>0) return (float)jet_kt6_eta.at    (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_energy", "if (n_jets_kt6>0) return (float)jet_kt6_energy.at (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_mass",   "if (n_jets_kt6>0) return (float)jet_kt6_mass.at   (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_dR_b",   "if (n_jets_kt6>0) return (float)jet_kt6_dR_b.at   (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_dR_s",   "if (n_jets_kt6>0) return (float)jet_kt6_dR_s.at   (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_isSig",  "if (n_jets_kt6>0) return (float)jet_kt6_isSig.at  (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_flavor", "if (n_jets_kt6>0) return (float)jet_kt6_flavor.at (jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_isG",    "if (n_jets_kt6>0) return (float)recojet_isG_kt6.at(jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_isQ",    "if (n_jets_kt6>0) return (float)recojet_isQ_kt6.at(jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_isS",    "if (n_jets_kt6>0) return (float)recojet_isS_kt6.at(jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_isC",    "if (n_jets_kt6>0) return (float)recojet_isC_kt6.at(jet_kt6_leadC_idx); else return float(-99.);")
                  .Define("jet_kt6_leadC_isB",    "if (n_jets_kt6>0) return (float)recojet_isB_kt6.at(jet_kt6_leadC_idx); else return float(-99.);")

                  .Define("jet_kt6_subC_idx", "float max_C = 0.0; int idx = 0; for (int i=0; i<jet_kt6_mass.size();++i) {if (recojet_isC_kt6.at(i) > max_C and recojet_isC_kt6.at(i) != Max(recojet_isC_kt6)) {max_C = recojet_isC_kt6.at(i); idx = i;}} return idx;")
                  .Define("jet_kt6_subC_px",     "if (n_jets_kt6>0) return (float)jet_kt6_px.at     (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_py",     "if (n_jets_kt6>0) return (float)jet_kt6_py.at     (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_pz",     "if (n_jets_kt6>0) return (float)jet_kt6_pz.at     (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_phi",    "if (n_jets_kt6>0) return (float)jet_kt6_phi.at    (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_eta",    "if (n_jets_kt6>0) return (float)jet_kt6_eta.at    (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_energy", "if (n_jets_kt6>0) return (float)jet_kt6_energy.at (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_mass",   "if (n_jets_kt6>0) return (float)jet_kt6_mass.at   (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_dR_b",   "if (n_jets_kt6>0) return (float)jet_kt6_dR_b.at   (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_dR_s",   "if (n_jets_kt6>0) return (float)jet_kt6_dR_s.at   (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_isSig",  "if (n_jets_kt6>0) return (float)jet_kt6_isSig.at  (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_flavor", "if (n_jets_kt6>0) return (float)jet_kt6_flavor.at (jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_isG",    "if (n_jets_kt6>0) return (float)recojet_isG_kt6.at(jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_isQ",    "if (n_jets_kt6>0) return (float)recojet_isQ_kt6.at(jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_isS",    "if (n_jets_kt6>0) return (float)recojet_isS_kt6.at(jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_isC",    "if (n_jets_kt6>0) return (float)recojet_isC_kt6.at(jet_kt6_subC_idx); else return float(-99.);")
                  .Define("jet_kt6_subC_isB",    "if (n_jets_kt6>0) return (float)recojet_isB_kt6.at(jet_kt6_subC_idx); else return float(-99.);")
        )

        ## event selection

        return df3




    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list
    def output():
        branchList = [
                 "n_genTops", "n_genWs", "n_genBottoms", "n_genStranges", "n_genMuons", "n_genElectrons", 
                 "Wp_elenu", "Wp_munu", "Wp_taunu", "Wp_d", "Wp_s", "Wp_b",
                 "Wm_elenu", "Wm_munu", "Wm_taunu", "Wm_d", "Wm_s", "Wm_b",
                 "genW_px", "genW_py", "genW_pz", "genW_phi", "genW_eta", "genW_energy", "genW_mass", "genW_charge",
                 "n_muons", "n_electrons", "n_photons",
                 "muon_px", "muon_py", "muon_pz", "muon_phi", "muon_eta", "muon_energy", "muon_mass", "muon_charge",
                 "electron_px", "electron_py", "electron_pz", "electron_phi", "electron_eta", "electron_energy", "electron_mass", "electron_charge",
                 "photon_px", "photon_py", "photon_pz", "photon_phi", "photon_eta", "photon_energy", "photon_mass",
                 #"Emiss_energy", "Emiss_p", "Emiss_px", "Emiss_py", "Emiss_pz", "Emiss_phi", "Emiss_eta",
                 "recoEmiss_px", "recoEmiss_py", "recoEmiss_pz", "recoEmiss_e"
                 ]

        branchList += ["n_muons_sel", "n_electrons_sel",
                       "muon_1_px", "muon_1_py", "muon_1_pz", "muon_1_phi", "muon_1_eta", "muon_1_energy", "muon_1_charge",
                       "muon_2_px", "muon_2_py", "muon_2_pz", "muon_2_phi", "muon_2_eta", "muon_2_energy", "muon_2_charge",
                       "electron_1_px", "electron_1_py", "electron_1_pz", "electron_1_phi", "electron_1_eta", "electron_1_energy", "electron_1_charge",
                       "electron_2_px", "electron_2_py", "electron_2_pz", "electron_2_phi", "electron_2_eta", "electron_2_energy", "electron_2_charge"
                       ]

        #branchList += jetFlavourHelper_R5. outputBranches()
        #branchList = [item for item in branchList if item not in ["jet_kt2","jet_R5"]] 
        #branchList += ["jet_R5_px", "jet_R5_py", "jet_R5_pz", "jet_R5_phi", "jet_R5_eta", "jet_R5_energy", "jet_R5_mass", "jet_R5_flavor"]
        branchList += ["jet_pass_px", "jet_pass_py", "jet_pass_pz", "jet_pass_phi", "jet_pass_eta", "jet_pass_energy", "jet_pass_mass", "jet_pass_flavor",
                       "jet_pass_dR_b", "jet_pass_dR_s", "jet_pass_isSig",     
                       "jet_pass_isG", "jet_pass_isQ", "jet_pass_isS", "jet_pass_isC", "jet_pass_isB", "n_jets_pass"]
        branchList += ["jet_kt6_px", "jet_kt6_py", "jet_kt6_pz", "jet_kt6_phi", "jet_kt6_eta", "jet_kt6_energy", "jet_kt6_mass", "jet_kt6_flavor",
                       "jet_kt6_dR_b", "jet_kt6_dR_s", "jet_kt6_isSig",
                       "recojet_isG_kt6", "recojet_isQ_kt6", "recojet_isS_kt6", "recojet_isC_kt6", "recojet_isB_kt6"]
        branchList += ["n_jets_kt2", "n_jets_kt4", "n_jets_kt6"]
        branchList += ["n_btags", "n_btags_kt2", "n_btags_kt4", "n_btags_kt6"]
        branchList += ["n_ctags", "n_ctags_kt2", "n_ctags_kt4", "n_ctags_kt6"]
        branchList += ["n_stags", "n_stags_kt2", "n_stags_kt4", "n_stags_kt6"]
        branchList += ["jet_kt2_Max_mass", "jet_kt2_Min_energy", "jet_kt4_Max_mass", "jet_kt4_Min_energy", "jet_kt6_Max_mass", "jet_kt6_Min_energy"]
        branchList += ["dilep_cat", "semilep_cat", "dihad_cat"]
        branchList += ["jet_leadS_px",   "jet_leadS_py",     "jet_leadS_pz",   "jet_leadS_phi",  "jet_leadS_eta", "jet_leadS_energy", 
                       "jet_leadS_mass", "jet_leadS_flavor", "jet_leadS_dR_b", "jet_leadS_dR_s", "jet_leadS_isSig",
                       "jet_leadS_isG",  "jet_leadS_isQ",    "jet_leadS_isS",  "jet_leadS_isC",  "jet_leadS_isB"]
        branchList += ["jet_subS_px",   "jet_subS_py",     "jet_subS_pz",   "jet_subS_phi",  "jet_subS_eta", "jet_subS_energy",
                       "jet_subS_mass", "jet_subS_flavor", "jet_subS_dR_b", "jet_subS_dR_s", "jet_subS_isSig",
                       "jet_subS_isG",  "jet_subS_isQ",    "jet_subS_isS",  "jet_subS_isC",  "jet_subS_isB"]
        branchList += ["jet_leadC_px",   "jet_leadC_py",     "jet_leadC_pz",   "jet_leadC_phi",  "jet_leadC_eta", "jet_leadC_energy",
                       "jet_leadC_mass", "jet_leadC_flavor", "jet_leadC_dR_b", "jet_leadC_dR_s", "jet_leadC_isSig",
                       "jet_leadC_isG",  "jet_leadC_isQ",    "jet_leadC_isS",  "jet_leadC_isC",  "jet_leadC_isB"]
        branchList += ["jet_subC_px",   "jet_subC_py",     "jet_subC_pz",   "jet_subC_phi",  "jet_subC_eta", "jet_subC_energy",
                       "jet_subC_mass", "jet_subC_flavor", "jet_subC_dR_b", "jet_subC_dR_s", "jet_subC_isSig",
                       "jet_subC_isG",  "jet_subC_isQ",    "jet_subC_isS",  "jet_subC_isC",  "jet_subC_isB"]

        branchList += ["jet_kt2_leadS_px",   "jet_kt2_leadS_py",     "jet_kt2_leadS_pz",   "jet_kt2_leadS_phi",  "jet_kt2_leadS_eta", "jet_kt2_leadS_energy",
                       "jet_kt2_leadS_mass", "jet_kt2_leadS_flavor", "jet_kt2_leadS_dR_b", "jet_kt2_leadS_dR_s", "jet_kt2_leadS_isSig",
                       "jet_kt2_leadS_isG",  "jet_kt2_leadS_isQ",    "jet_kt2_leadS_isS",  "jet_kt2_leadS_isC",  "jet_kt2_leadS_isB"]
        branchList += ["jet_kt2_subS_px",    "jet_kt2_subS_py",      "jet_kt2_subS_pz",    "jet_kt2_subS_phi",   "jet_kt2_subS_eta", "jet_kt2_subS_energy",
                       "jet_kt2_subS_mass",  "jet_kt2_subS_flavor",  "jet_kt2_subS_dR_b",  "jet_kt2_subS_dR_s",  "jet_kt2_subS_isSig",
                       "jet_kt2_subS_isG",   "jet_kt2_subS_isQ",     "jet_kt2_subS_isS",   "jet_kt2_subS_isC",   "jet_kt2_subS_isB"]
        branchList += ["jet_kt2_leadC_px",   "jet_kt2_leadC_py",     "jet_kt2_leadC_pz",   "jet_kt2_leadC_phi",  "jet_kt2_leadC_eta", "jet_kt2_leadC_energy",
                       "jet_kt2_leadC_mass", "jet_kt2_leadC_flavor", "jet_kt2_leadC_dR_b", "jet_kt2_leadC_dR_s", "jet_kt2_leadC_isSig",
                       "jet_kt2_leadC_isG",  "jet_kt2_leadC_isQ",    "jet_kt2_leadC_isS",  "jet_kt2_leadC_isC",  "jet_kt2_leadC_isB"]
        branchList += ["jet_kt2_subC_px",    "jet_kt2_subC_py",      "jet_kt2_subC_pz",    "jet_kt2_subC_phi",   "jet_kt2_subC_eta", "jet_kt2_subC_energy",
                       "jet_kt2_subC_mass",  "jet_kt2_subC_flavor",  "jet_kt2_subC_dR_b",  "jet_kt2_subC_dR_s",  "jet_kt2_subC_isSig",
                       "jet_kt2_subC_isG",   "jet_kt2_subC_isQ",     "jet_kt2_subC_isS",   "jet_kt2_subC_isC",   "jet_kt2_subC_isB"]
        branchList += ["jet_kt4_leadS_px",   "jet_kt4_leadS_py",     "jet_kt4_leadS_pz",   "jet_kt4_leadS_phi",  "jet_kt4_leadS_eta", "jet_kt4_leadS_energy",
                       "jet_kt4_leadS_mass", "jet_kt4_leadS_flavor", "jet_kt4_leadS_dR_b", "jet_kt4_leadS_dR_s", "jet_kt4_leadS_isSig",
                       "jet_kt4_leadS_isG",  "jet_kt4_leadS_isQ",    "jet_kt4_leadS_isS",  "jet_kt4_leadS_isC",  "jet_kt4_leadS_isB"]
        branchList += ["jet_kt4_subS_px",    "jet_kt4_subS_py",      "jet_kt4_subS_pz",    "jet_kt4_subS_phi",   "jet_kt4_subS_eta", "jet_kt4_subS_energy",
                       "jet_kt4_subS_mass",  "jet_kt4_subS_flavor",  "jet_kt4_subS_dR_b",  "jet_kt4_subS_dR_s",  "jet_kt4_subS_isSig",
                       "jet_kt4_subS_isG",   "jet_kt4_subS_isQ",     "jet_kt4_subS_isS",   "jet_kt4_subS_isC",   "jet_kt4_subS_isB"]
        branchList += ["jet_kt4_leadC_px",   "jet_kt4_leadC_py",     "jet_kt4_leadC_pz",   "jet_kt4_leadC_phi",  "jet_kt4_leadC_eta", "jet_kt4_leadC_energy",
                       "jet_kt4_leadC_mass", "jet_kt4_leadC_flavor", "jet_kt4_leadC_dR_b", "jet_kt4_leadC_dR_s", "jet_kt4_leadC_isSig",
                       "jet_kt4_leadC_isG",  "jet_kt4_leadC_isQ",    "jet_kt4_leadC_isS",  "jet_kt4_leadC_isC",  "jet_kt4_leadC_isB"]
        branchList += ["jet_kt4_subC_px",    "jet_kt4_subC_py",      "jet_kt4_subC_pz",    "jet_kt4_subC_phi",   "jet_kt4_subC_eta", "jet_kt4_subC_energy",
                       "jet_kt4_subC_mass",  "jet_kt4_subC_flavor",  "jet_kt4_subC_dR_b",  "jet_kt4_subC_dR_s",  "jet_kt4_subC_isSig",
                       "jet_kt4_subC_isG",   "jet_kt4_subC_isQ",     "jet_kt4_subC_isS",   "jet_kt4_subC_isC",   "jet_kt4_subC_isB"]
        branchList += ["jet_kt6_leadS_px",   "jet_kt6_leadS_py",     "jet_kt6_leadS_pz",   "jet_kt6_leadS_phi",  "jet_kt6_leadS_eta", "jet_kt6_leadS_energy", 
                       "jet_kt6_leadS_mass", "jet_kt6_leadS_flavor", "jet_kt6_leadS_dR_b", "jet_kt6_leadS_dR_s", "jet_kt6_leadS_isSig",
                       "jet_kt6_leadS_isG",  "jet_kt6_leadS_isQ",    "jet_kt6_leadS_isS",  "jet_kt6_leadS_isC",  "jet_kt6_leadS_isB"]
        branchList += ["jet_kt6_subS_px",    "jet_kt6_subS_py",      "jet_kt6_subS_pz",    "jet_kt6_subS_phi",   "jet_kt6_subS_eta", "jet_kt6_subS_energy",
                       "jet_kt6_subS_mass",  "jet_kt6_subS_flavor",  "jet_kt6_subS_dR_b",  "jet_kt6_subS_dR_s",  "jet_kt6_subS_isSig",
                       "jet_kt6_subS_isG",   "jet_kt6_subS_isQ",     "jet_kt6_subS_isS",   "jet_kt6_subS_isC",   "jet_kt6_subS_isB"]
        branchList += ["jet_kt6_leadC_px",   "jet_kt6_leadC_py",     "jet_kt6_leadC_pz",   "jet_kt6_leadC_phi",  "jet_kt6_leadC_eta", "jet_kt6_leadC_energy",
                       "jet_kt6_leadC_mass", "jet_kt6_leadC_flavor", "jet_kt6_leadC_dR_b", "jet_kt6_leadC_dR_s", "jet_kt6_leadC_isSig",
                       "jet_kt6_leadC_isG",  "jet_kt6_leadC_isQ",    "jet_kt6_leadC_isS",  "jet_kt6_leadC_isC",  "jet_kt6_leadC_isB"]
        branchList += ["jet_kt6_subC_px",    "jet_kt6_subC_py",      "jet_kt6_subC_pz",    "jet_kt6_subC_phi",   "jet_kt6_subC_eta", "jet_kt6_subC_energy",
                       "jet_kt6_subC_mass",  "jet_kt6_subC_flavor",  "jet_kt6_subC_dR_b",  "jet_kt6_subC_dR_s",  "jet_kt6_subC_isSig",
                       "jet_kt6_subC_isG",   "jet_kt6_subC_isQ",     "jet_kt6_subC_isS",   "jet_kt6_subC_isC",   "jet_kt6_subC_isB"]

        return branchList