import os, copy # tagging
import ROOT
import urllib.request

#Mandatory: List of processes
processList_ = {
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

#Mandatory: Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics
#prodTag     = "FCCee/winter2023/IDEA/"

#inputDir = "/ceph/sgiappic/HiggsCP/winter23"
#inputDir = "root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"
inputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/MCgenCP/DelphesPythia8_EDM4HEP/test/"

#Optional: output directory, default is local running directory
#outputDir   = "/ceph/sgiappic/HiggsCP/stage1_241105/" 
outputDir = "/eos/experiment/fcc/ee/analyses_storage/Higgs_and_TOP/HiggsTauTau/ecm240/CP/gen_stage1_ele/"

# additional/costom C++ functions, defined in header files (optional)
includePaths = ["functions.h"]

### necessary to run on HTCondor ###
eosType = "eosuser"

#Optional running on HTCondor, default is False
runBatch = False

nCPUS = 6

#Optional batch queue name when running on HTCondor, default is workday
batchQueue = "workday"

#Optional computing account when running on HTCondor, default is group_u_FCC.local_gen
compGroup = "group_u_CMS.u_zh.users"

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
                .Define("GenHiggs_p4",      "TLorentzVector(GenHiggs_px.at(0), GenHiggs_py.at(0), GenHiggs_pz.at(0), GenHiggs_e.at(0))")
                
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
                .Define("HiggsGenTau_p4",     "FCCAnalyses::ZHfunctions::build_p4(HiggsGenTau_px, HiggsGenTau_py, HiggsGenTau_pz, HiggsGenTau_e)")

                .Define("GenTauP_p4",     "if (HiggsGenTau_charge.at(0)==1) return HiggsGenTau_p4.at(0); else return HiggsGenTau_p4.at(1);")
                .Define("GenTauP_px",    "GenTauP_p4.Px()")
                .Define("GenTauP_py",    "GenTauP_p4.Py()")
                .Define("GenTauP_pz",    "GenTauP_p4.Pz()")
                .Define("GenTauP_p",    "GenTauP_p4.P()")
                .Define("GenTauP_pt",    "GenTauP_p4.Pt()")
                .Define("GenTauP_e",     "GenTauP_p4.E()")
                .Define("GenTauP_eta",    "GenTauP_p4.Eta()")
                .Define("GenTauP_phi",    "GenTauP_p4.Phi()")
                .Define("GenTauP_theta",    "GenTauP_p4.Theta()")
                .Define("GenTauP_y",     "GenTauP_p4.Rapidity()")
                .Define("GenTauP_mass",    "GenTauP_p4.M()")
                
                .Define("GenTauM_p4",     "if (HiggsGenTau_charge.at(0)==1) return HiggsGenTau_p4.at(1); else return HiggsGenTau_p4.at(0);")
                .Define("GenTauM_px",    "GenTauM_p4.Px()")
                .Define("GenTauM_py",    "GenTauM_p4.Py()")
                .Define("GenTauM_pz",    "GenTauM_p4.Pz()")
                .Define("GenTauM_p",    "GenTauM_p4.P()")
                .Define("GenTauM_pt",    "GenTauM_p4.Pt()")
                .Define("GenTauM_e",     "GenTauM_p4.E()")
                .Define("GenTauM_eta",    "GenTauM_p4.Eta()")
                .Define("GenTauM_phi",    "GenTauM_p4.Phi()")
                .Define("GenTauM_theta",    "GenTauM_p4.Theta()")
                .Define("GenTauM_y",     "GenTauM_p4.Rapidity()")
                .Define("GenTauM_mass",    "GenTauM_p4.M()")

                #rho nu decay (pi pi0 nu)
                .Define("TauPtoRhoNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 22, 22, -16},  true, false, false, false)  ( Particle, Particle1)" ) #size is the size of the vector (mother+daughters) because it only saves the first matching decay in the event, not all the decays
                .Define("TauMtoRhoNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 22, 22, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #pi nu decay
                .Define("TauPtoPiNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, -16},  true, false, false, false)  ( Particle, Particle1)" ) #size is the size of the vector (mother+daughters) because it only saves the first matching decay in the event, not all the decays
                .Define("TauMtoPiNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #ele nu decay
                .Define("TauPtoENuNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {-11, 12, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMtoENuNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {11, -12, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #mu nu decay
                .Define("TauPtoMuNuNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {-13, 14, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMtoMuNuNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {13, -14, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #a1 nu decay (pi pi0 pi0 nu)
                .Define("TauPto2Pi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 22, 22, 22, 22, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMto2Pi0Nu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, 22, 22, 22, 22, 16},  true, false, false, false)  ( Particle, Particle1)" )
                #a1 nu decay - three prongs (pi pi pi nu)
                .Define("TauPto3PiNu_idx",  "FCCAnalyses::MCParticle::get_indices( -15, {211, 211, -211, -16},  true, false, false, false)  ( Particle, Particle1)" )
                .Define("TauMto3PiNu_idx",  "FCCAnalyses::MCParticle::get_indices( 15, {-211, -211, 211, 16},  true, false, false, false)  ( Particle, Particle1)" )

                .Define("GenTauP_DM",      "if (TauPtoPiNu_idx.size()>0) return 0; else if (TauPtoRhoNu_idx.size()>0) return 1; else if (TauPto2Pi0Nu_idx.size()>0) return 2;\
                                        else if (TauPto3PiNu_idx.size()>0) return 3; else if (TauPtoENuNu_idx.size()>0) return 4; else if (TauPtoMuNuNu_idx.size()>0) return 5; else return 10;")
                .Define("GenTauM_DM",      "if (TauMtoPiNu_idx.size()>0) return 0; else if (TauMtoRhoNu_idx.size()>0) return 1; else if (TauMto2Pi0Nu_idx.size()>0) return 2;\
                                        else if (TauMto3PiNu_idx.size()>0) return 3; else if (TauMtoENuNu_idx.size()>0) return 4; else if (TauMtoMuNuNu_idx.size()>0) return 5; else return 10;")

                #select the right decay for both taus

                ###############################

                .Filter("n_HiggsGenTau==2 && (HiggsGenTau_charge.at(0) + HiggsGenTau_charge.at(1))==0") #select only events with oppositely charged tau pair from Higgs and with known decay mode
                #.Filter("(TauPtoENuNu_idx.size()>0)")
                #.Filter("(TauMtoENuNu_idx.size()>0)")

                #.Filter("n_FSGenElectron==4 && n_FSGenMuon==0")

                .Define("FSGenLeptons",           "FCCAnalyses::MCParticle::mergeParticles(FSGenElectron, FSGenMuon)")
                .Define("n_FSGenLeptons", "FCCAnalyses::MCParticle::get_n(FSGenLeptons)")
                .Define("FSGenLepton_e", "FCCAnalyses::MCParticle::get_e(FSGenLeptons)")
                .Define("FSGenLepton_p", "FCCAnalyses::MCParticle::get_p(FSGenLeptons)")
                .Define("FSGenLepton_pt", "FCCAnalyses::MCParticle::get_pt(FSGenLeptons)")
                .Define("FSGenLepton_px", "FCCAnalyses::MCParticle::get_px(FSGenLeptons)")
                .Define("FSGenLepton_py", "FCCAnalyses::MCParticle::get_py(FSGenLeptons)")
                .Define("FSGenLepton_pz", "FCCAnalyses::MCParticle::get_pz(FSGenLeptons)")
                .Define("FSGenLepton_y", "FCCAnalyses::MCParticle::get_y(FSGenLeptons)")
                .Define("FSGenLepton_eta", "FCCAnalyses::MCParticle::get_eta(FSGenLeptons)")
                .Define("FSGenLepton_theta", "FCCAnalyses::MCParticle::get_theta(FSGenLeptons)")
                .Define("FSGenLepton_phi", "FCCAnalyses::MCParticle::get_phi(FSGenLeptons)")
                .Define("FSGenLepton_charge", "FCCAnalyses::MCParticle::get_charge(FSGenLeptons)")
                .Define("FSGenLepton_mass",   "FCCAnalyses::MCParticle::get_mass(FSGenLeptons)")

                .Filter("FSGenLeptons.size()==4") #select only events with 4 leptons (e or mu) in the final state

                .Define("RecoLepton_p4",  "FCCAnalyses::ZHfunctions::build_p4(FSGenLepton_px, FSGenLepton_py, FSGenLepton_pz, FSGenLepton_e)")

                .Define("RecoZH_idx",        "FCCAnalyses::ZHfunctions::FindBest_4(RecoLepton_p4, FSGenLepton_charge, FSGenLepton_mass, 91.188, 125.25)")

                .Define("GenPiP_p4",      "if (FSGenLepton_charge.at(RecoZH_idx[2])==1) return RecoLepton_p4.at(RecoZH_idx[2]); else return RecoLepton_p4.at(RecoZH_idx[3]);")
                .Define("GenPiM_p4",        "if (FSGenLepton_charge.at(RecoZH_idx[3])==-1) return RecoLepton_p4.at(RecoZH_idx[3]); else return RecoLepton_p4.at(RecoZH_idx[2]);")

                #.Define("GenPiP_e", "TauPtoENuNu_idx.size() > 1 ? FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoENuNu_idx[1])}) : ROOT::VecOps::RVec<float>{-99}")
                #.Define("GenPiP_px", "TauPtoENuNu_idx.size() > 1 ? FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoENuNu_idx[1])}) : ROOT::VecOps::RVec<float>{-99}")
                #.Define("GenPiP_py", "TauPtoENuNu_idx.size() > 1 ? FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoENuNu_idx[1])}) : ROOT::VecOps::RVec<float>{-99}")
                #.Define("GenPiP_pz", "TauPtoENuNu_idx.size() > 1 ? FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauPtoENuNu_idx[1])}) : ROOT::VecOps::RVec<float>{-99}")
                #.Define("GenPiP_p4", "(GenPiP_px.size() > 0 && GenPiP_py.size() > 0 && GenPiP_pz.size() > 0 && GenPiP_e.size() > 0) ? TLorentzVector(GenPiP_px.at(0), GenPiP_py.at(0), GenPiP_pz.at(0), GenPiP_e.at(0)) : TLorentzVector(-99, -99, -99, -99)")

                #.Define("GenPiM_e", "TauMtoENuNu_idx.size() > 1 ? FCCAnalyses::MCParticle::get_e(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoENuNu_idx[1])}) : ROOT::VecOps::RVec<float>{-99}")
                #.Define("GenPiM_px", "TauMtoENuNu_idx.size() > 1 ? FCCAnalyses::MCParticle::get_px(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoENuNu_idx[1])}) : ROOT::VecOps::RVec<float>{-99}")
                #.Define("GenPiM_py", "TauMtoENuNu_idx.size() > 1 ? FCCAnalyses::MCParticle::get_py(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoENuNu_idx[1])}) : ROOT::VecOps::RVec<float>{-99}")
                #.Define("GenPiM_pz", "TauMtoENuNu_idx.size() > 1 ? FCCAnalyses::MCParticle::get_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData>{Particle.at(TauMtoENuNu_idx[1])}) : ROOT::VecOps::RVec<float>{-99}")
                #.Define("GenPiM_p4", "(GenPiM_px.size() > 0 && GenPiM_py.size() > 0 && GenPiM_pz.size() > 0 && GenPiM_e.size() > 0) ? TLorentzVector(GenPiM_px.at(0), GenPiM_py.at(0), GenPiM_pz.at(0), GenPiM_e.at(0)) : TLorentzVector(-99, -99, -99, -99)") 

                .Define("ZMF_p4",       "GenPiP_p4+GenPiM_p4")
                .Define("ZMF_GenTau_p4",    "FCCAnalyses::ZHfunctions::boosted_p4(- ZMF_p4, HiggsGenTau_p4)")
                .Define("ZMF_GenTauP_p4",     "if (HiggsGenTau_charge.at(0)==1) return ZMF_GenTau_p4.at(0); else return ZMF_GenTau_p4.at(1);")
                .Define("ZMF_GenTauM_p4",     "if (HiggsGenTau_charge.at(0)==1) return ZMF_GenTau_p4.at(1); else return ZMF_GenTau_p4.at(0);")

                .Define("ZMF_GenPiP_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, GenPiP_p4)")
                .Define("ZMF_GenPiM_p4",    "FCCAnalyses::ZHfunctions::boosted_p4_single(- ZMF_p4, GenPiM_p4)")

                .Define("ZMF_GenTauP_par",       "((ZMF_GenTauP_p4.Vect()).Dot((ZMF_GenPiP_p4.Vect())))/((ZMF_GenPiP_p4.Vect()).Mag2())*ZMF_GenPiP_p4.Vect()")
                .Define("ZMF_GenTauP_perp",      "(ZMF_GenTauP_p4.Vect() - ZMF_GenTauP_par).Unit()")  
                .Define("ZMF_GenTauM_par",       "((ZMF_GenTauM_p4.Vect()).Dot((ZMF_GenPiM_p4.Vect())))/((ZMF_GenPiM_p4.Vect()).Mag2())*ZMF_GenPiM_p4.Vect()")
                .Define("ZMF_GenTauM_perp",      "(ZMF_GenTauM_p4.Vect() - ZMF_GenTauM_par).Unit()")  

                .Define("Phi_ZMF",       "acos(ZMF_GenTauP_perp.Dot(ZMF_GenTauM_perp))")
                .Define("y_plus",       "1.")
                .Define("y_min",       "1.")
                .Define("y_tau",        "(y_plus*y_min)") 
                .Define("O_ZMF",         "((ZMF_GenPiM_p4.Vect()).Unit()).Dot(ZMF_GenTauP_perp.Cross(ZMF_GenTauM_perp))")

                ## y=1 if both pi0 are not there so it doesn't matter, if one is there then it's the single y, if both are present then it's still what i want
                .Define("PhiCP_y",        "if (y_tau>=0) return Phi_ZMF; else return (-3.1415 + Phi_ZMF);")
                ## if the selection prceeded with the y then it will not have an effect but jsut mirroring an already symmetric function, otherwise the phi_recoil is correclty separated when there is no pi0
                .Define("GenPhi_CP",        "if (O_ZMF>=0) return PhiCP_y; else return (-PhiCP_y);")


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

            "GenTauP_px",    
            "GenTauP_py",   
            "GenTauP_pz",   
            "GenTauP_p",   
            "GenTauP_pt",   
            "GenTauP_e",    
            "GenTauP_eta",    
            "GenTauP_phi",    
            "GenTauP_theta",    
            "GenTauP_y",    
            "GenTauP_mass",

            "GenTauM_px",    
            "GenTauM_py",   
            "GenTauM_pz",   
            "GenTauM_p",   
            "GenTauM_pt",   
            "GenTauM_e",    
            "GenTauM_eta",    
            "GenTauM_phi",    
            "GenTauM_theta",    
            "GenTauM_y",    
            "GenTauM_mass",

            "ZMF_GenTauP_p4",
            "ZMF_GenTauM_p4", 
            "GenPhi_CP",
            "Phi_ZMF",
            "O_ZMF",
            "y_tau",

            "GenTauP_DM",
            "GenTauM_DM",


        ]

        return branchList
