#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"
#include "FCCAnalyses/JetConstituentsUtils.h"
#include "FCCAnalyses/ReconstructedParticle.h"
#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "edm4hep/Track.h"
#include "edm4hep/TrackerHitData.h"
#include "edm4hep/TrackData.h"
#include "edm4hep/Cluster.h"
#include "edm4hep/ClusterData.h"
#include "edm4hep/CalorimeterHitData.h"
#include "FCCAnalyses/JetClusteringUtils.h"
// #include "FCCAnalyses/ExternalRecombiner.h"
#include "fastjet/JetDefinition.hh"
#include "fastjet/PseudoJet.hh"
#include "fastjet/Selector.hh"


namespace FCCAnalyses { namespace ZHfunctions {


// returns missing energy vector, based on reco particles
Vec_rp missingEnergy(float ecm, Vec_rp in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += -p.momentum.x;
        py += -p.momentum.y;
        pz += -p.momentum.z;
        e += p.energy;
    }
    
    Vec_rp ret;
    rp res;
    res.momentum.x = px;
    res.momentum.y = py;
    res.momentum.z = pz;
    res.energy = ecm-e;
    ret.emplace_back(res);
    return ret;
}

  // --- functions Helper
float deltaEta(float eta1, float eta2) {
    return std::abs(eta1 - eta2);
  }

float deltaPhi(float phi1, float phi2){
    float PHI = std::abs(phi1-phi2);
    if (PHI<=3.14159265)
      return PHI;
    else
      return 2*3.14159265-PHI;
  }

float deltaR(float phi1, float phi2, float eta1, float eta2) {
    return sqrt(deltaEta(eta1,eta2)*deltaEta(eta1,eta2) + deltaPhi(phi1,phi2)*deltaPhi(phi1,phi2));
  }
}

ROOT::VecOps::RVec<TLorentzVector> build_p4(ROOT::VecOps::RVec<float> px, ROOT::VecOps::RVec<float> py, ROOT::VecOps::RVec<float> pz, ROOT::VecOps::RVec<float> e) {
    ROOT::VecOps::RVec<TLorentzVector> p4;
    for (size_t i = 0; i < px.size(); ++i) {  
        TLorentzVector tlv;
        tlv.SetPxPyPzE(px[i], py[i], pz[i], e[i]);
        p4.push_back(tlv);
    }
    return p4;
}

TLorentzVector build_p4_single(float px, float py, float pz, float e) {
    TLorentzVector tlv;
    tlv.SetPxPyPzE(px, py, pz, e);
    return tlv;
}

ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> findTauInJet (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets){

    // Identify taus by starting from a jet. An alternative is starting directly from reconstructed particles (to be tested more deeply in the future). 
    // This algorithm requires first building a jet (base example is clustering_ee_kt(2, 4, 1, 0) , we have tested with several configurations) from con 
    // Then loop over the constituents: identify a seed, and count pions (neutral and charged) and photons to a) build a tau candidate b) be able to identify it

    ROOT::VecOps::RVec< edm4hep::ReconstructedParticleData> out;

    // Loop over jets:

    for (int i = 0; i < jets.size(); ++i) {

        TLorentzVector sum_tau; // initialized by (0., 0., 0., 0.)
        edm4hep::ReconstructedParticleData partMod;
        FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);
        int tauID=-1;
        int count_piP=0, count_piM=0, count_nu=0, count_pho=0;

        // Find Lead (This needs to change to first sort the jcs by p or pt, it is very messy right now)

        TLorentzVector lead;
        lead.SetPxPyPzE(0,0,0,0);
        int chargeLead=0;

        // Eventually the FCC sw should have better ID for the particles, based on the detector. 
        // For the moment I compare the reconstructed  masses and charges to known values
        // (since that is what the PID module as references does). This is something to be improved in the future! 
        // Too truth-based.


        // First loop just to find the lead (not very efficient). 
        for (const auto& jc : jcs) {

            // No electrons or muons
            if (fabs(jc.mass -  0.105658) < 1.e-03) {
                tauID=-13;
                continue; 
                }
            if (fabs(jc.mass-0.000510999)<  1.e-05 ) {
                tauID=-11;
                continue; //stops the loop on jet constituents as soon as it finds a lepton
            }

            // Anything else lets: find the highest pt one, charged particle as lead only
            if ((jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
                lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
                chargeLead=jc.charge;
            }
        }

        // Clean and start counting
        if (lead.Pt()<2) {
            tauID=-1;
            partMod.type = tauID;
            out.push_back(partMod); //make sure to keep this iteration saved as non tau jets
            continue;
        } // Too low pt 

        if (tauID==-13 || tauID==-11) {
            partMod.type = tauID;
            out.push_back(partMod); //make sure to keep this iteration saved as non tau jets
            continue;
        }//jets with electrons or muon, cannot be tau jets

        if (chargeLead==1) count_piP++;

        else if (chargeLead==-1) count_piM++;

        else {continue;} // This cannot happen 

        sum_tau+=lead;

        // Now I loop to build the tau adding candidates to the lead
        // Only if they satisfy some conditions: distance, charge, etc 
        for (const auto& jc : jcs) {

            TLorentzVector tlv;  
            tlv.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);

            if (tlv==lead) continue;

            // Distance (in terms of Theta)
            double dTheta= fabs(sum_tau.Theta()-tlv.Theta());   

            // The Pt cut and Distance are parameters to tune in the future
            if (tlv.Pt()<1 || dTheta>0.20) continue;

            // Now count! 
            if (jc.charge>0) count_piP++;   

            else if (jc.charge<0) count_piM++;  

            else  count_pho++;

            sum_tau += tlv;  // This is the 4 momenta of only the particles we have selected

        }

        // Now we have a tau candidate and its momentum (sum_tau).
        // Lets build the ID : count the charged pions and the neutrals. 
        // The charge of the tau must be +1 or -1. 
        // Considering the decays of the tau: we want candidates with one or three charged candidates (one or three prongs) 
        //std::cout<<" Count? "<<count_piP<<"   "<<count_piM<<"  "<<count_pho<<"   "<<count_pho<<std::endl;
        // The ID number assigned is a bit dummy, helps to keep track of the kind of candidate we have (and see if we can be more restrictive)

        if (tauID!=-13 && tauID!=-11 && abs(count_piP-count_piM)==1 && ( (count_piP+count_piM)==1 || (count_piP+count_piM)==3) ){    

            if( (count_piP+count_piM)==1 && count_pho==0) tauID=0;
            if( (count_piP+count_piM)==1 && count_pho==1) tauID=1;
            if( (count_piP+count_piM)==1 && count_pho==2) tauID=2;
            if( (count_piP+count_piM)==1 && count_pho==3) tauID=3;
            if( (count_piP+count_piM)==1 && count_pho==4) tauID=4;
            if( (count_piP+count_piM)==1 && count_pho==5) tauID=5;
            if( (count_piP+count_piM)==1 && count_pho>=6) tauID=6;

            if( (count_piP+count_piM)==3 && count_pho==0)  tauID=10;
            if( (count_piP+count_piM)==3 && count_pho==1)  tauID=11;
            if( (count_piP+count_piM)==3 && count_pho==2)  tauID=12;
            if( (count_piP+count_piM)==3 && count_pho==3)  tauID=13;
            if( (count_piP+count_piM)==3 && count_pho==4)  tauID=14;
            if( (count_piP+count_piM)==3 && count_pho==5)  tauID=15;
            if( (count_piP+count_piM)==3 && count_pho>=6)  tauID=16;

            partMod.momentum.x=sum_tau.Px();
            partMod.momentum.y=sum_tau.Py();
            partMod.momentum.z=sum_tau.Pz();
            partMod.mass= sum_tau.M();
            partMod.energy= sum_tau.E();
            partMod.charge= (count_piP-count_piM);
            partMod.type = tauID;

            if (tauID!=-1 && partMod.mass<3)  out.push_back(partMod);
            else {
                partMod.momentum.x = 0;
                partMod.momentum.y = 0;
                partMod.momentum.z = 0;
                partMod.mass = 0;
                partMod.energy= 0;
                partMod.charge = 0; //reset particle so it aligs with other non tau particles saved, we only care about the type in these cases
                tauID = -2;
                partMod.type = tauID;
                out.push_back(partMod);
            }
        }

        else {
            tauID=-3;
            partMod.type = tauID;
            out.push_back(partMod);
        }
    }
    return out;

}
}

#endif
