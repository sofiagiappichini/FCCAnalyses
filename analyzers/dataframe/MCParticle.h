
#ifndef  MCPARTICLE_ANALYZERS_H
#define  MCPARTICLE_ANALYZERS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/Vector3f.h"
#include "edm4hep/Vector3d.h"
#include "edm4hep/Vector2i.h"


/// select MCParticles with transverse momentum greater than a minimum value [GeV]
struct selMC_pT {
  selMC_pT(float arg_min_pt);
  float m_min_pt = 20; //> transverse momentum threshold [GeV]
  std::vector<edm4hep::MCParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
};

/// return the time of the input MCParticles
std::vector<float> getMC_time(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the PDG of the input MCParticles
std::vector<float> getMC_pdg(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the generator status of the input MCParticles
std::vector<float> getMC_genStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the simulation status of the input MCParticles
std::vector<float> getMC_simStatus(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the production vertex of the input MCParticles
std::vector<edm4hep::Vector3d> getMC_vertex(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the production vertex x of the input MCParticles
std::vector<float> getMC_vertex_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the production vertex y of the input MCParticles
std::vector<float> getMC_vertex_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the production vertex z of the input MCParticles
std::vector<float> getMC_vertex_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the end point of the input MCParticles
std::vector<edm4hep::Vector3d> getMC_endPoint(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the end point x of the input MCParticles
std::vector<float> getMC_endPoint_x(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the end point y of the input MCParticles
std::vector<float> getMC_endPoint_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the z of the input MCParticles
std::vector<float> getMC_endPoint_z(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the transverse momenta of the input MCParticles
std::vector<float> getMC_pt(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the momenta of the input MCParticles
std::vector<float> getMC_p(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the momenta of the input MCParticles
std::vector<float> getMC_px(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the momenta of the input MCParticles
std::vector<float> getMC_py(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the momenta of the input MCParticles
std::vector<float> getMC_pz(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the pseudo-rapidity of the input MCParticles
std::vector<float> getMC_eta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the rapidity of the input MCParticles
std::vector<float> getMC_y(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the theta of the input MCParticles
std::vector<float> getMC_theta(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the phi of the input MCParticles
std::vector<float> getMC_phi(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the energy of the input MCParticles
std::vector<float> getMC_e(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// return the masses of the input MCParticles
std::vector<float> getMC_mass(ROOT::VecOps::RVec<edm4hep::MCParticleData> in); 

/// return the charges of the input MCParticles
std::vector<float> getMC_charge(ROOT::VecOps::RVec<edm4hep::MCParticleData> in); 

/// return the TlorentzVector of the input MCParticles
std::vector<TLorentzVector> getMC_tlv(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);

/// concatenate both input vectors and return the resulting vector
ROOT::VecOps::RVec<edm4hep::MCParticleData> mergeParticles(ROOT::VecOps::RVec<edm4hep::MCParticleData> x, ROOT::VecOps::RVec<edm4hep::MCParticleData> y);

/// return the size of the input collection
int getMC_n(ROOT::VecOps::RVec<edm4hep::MCParticleData> in);


#endif
