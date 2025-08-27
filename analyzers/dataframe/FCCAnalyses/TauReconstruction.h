
#ifndef  TAURECONSTRUCTION_ANALYZERS_H
#define  TAURECONSTRUCTION_ANALYZERS_H

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "FCCAnalyses/JetConstituentsUtils.h"
#include "FCCAnalyses/ReconstructedParticle.h"
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/ReconstructedParticle2MC.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/Track.h"
#include "edm4hep/TrackerHitData.h"
#include "edm4hep/TrackData.h"
#include "edm4hep/Cluster.h"
#include "edm4hep/ClusterData.h"
#include "edm4hep/CalorimeterHitData.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "FCCAnalyses/JetClusteringUtils.h"


namespace FCCAnalyses { namespace TauReconstruction {

// Identify taus. This algorithm requires to first build a jet (for example clustering_ee_kt(2, 4, 1, 0)).
// Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it with specific decay modes.
// The taus will have charge +-1, mass below 3 GeV, no leptons.

// "request" parameter, should be >0 only if needing specific consituents of the tau: 
    // 0 for full visible tau, 
    // 1 for charged pion (the one with same charge as the tau if from the rho resonance (3 prong)), 
    // 2 for opposite charged pion in rho resonance (3 prong) or sum of neutral particles (1 prong), 
    // 3 for sum of charged pions, 
    // 4 or else for neutral system only (only different from 1 and 2 in case of 3 prong).

// The outpiut is a ReconstructedParticle type, all the variables are then accessible through the usual methods.
// Every jet will return one entry so the vector can then be filtered by the tau ID for specific tau modes or quark jets.
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets, int request);

// Same function but with pi0 reconstruction
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet_pi0 (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets, int request);

// Function to get the impact parameter vector from the track, defined in the origin frame pointing to the point on the track that is closest to the IP
ROOT::VecOps::RVec<TLorentzVector> ImpactVector(ROOT::VecOps::RVec<TLorentzVector> Track, ROOT::VecOps::RVec<float> D0, ROOT::VecOps::RVec<float> Z0);

// find the intersection between two tracks defined by one point and one vector (both TVector3)
TVector3 findIntersection(const TVector3& P1, const TVector3& d1, const TVector3& P2, const TVector3& d2);

// Function to find the closest point on the line defined by d0 and direction of the track (track momentum) to the point IP
TLorentzVector ImpactFromIP(const TLorentzVector& d0, const TLorentzVector& pi, const TLorentzVector& IP);

// Return parallel component of a vector v that lies in the plane defined by a and b
TVector3 ProjectOntoPlane(const TVector3& v, const TVector3& a, const TVector3& b);

// Minimizer function to reconstruct the full tau momenta in di-tau events following reference https://arxiv.org/pdf/1507.01700
// Returns tau neutrinos in lab frame, for hadronic decays only
ROOT::VecOps::RVec<TLorentzVector> TauNuReco_Impact(const TLorentzVector& Recoil, // recoil system or centre of mass
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Charged_p4, // sum of charged daughters of the taus
                                                 const ROOT::VecOps::RVec<TLorentzVector>& Neutral_p4, // sum of neutral daughters of taus (if non then empty)
                                                 const ROOT::VecOps::RVec<float>& D0_p4, // d0 of leading prong
                                                 const ROOT::VecOps::RVec<float>& Z0_p4, //z0 of leading prong
                                                 const TLorentzVector& IP, // interaction point (e=0)
                                                 ROOT::VecOps::RVec<float> charge); // charge of taus, same indices as Charged_p4, Neutral_p4, D0_p4 and Z0_p4
                                            
// Following kinematic reconstrcution of di-tau system in its rest frame in https://arxiv.org/pdf/1310.8503
// Returns the taus in the lab frame, for hadronic decays only
// Recoil vector can be recoiling system or center of mass
// Tau_vis and charge need to have the same indices to properly assign the charge to the taus
ROOT::VecOps::RVec<TLorentzVector> TauReco_Kin (TLorentzVector Recoil, ROOT::VecOps::RVec<TLorentzVector> Tau_vis, ROOT::VecOps::RVec<float> charge);

}}

#endif
