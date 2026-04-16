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


namespace FCCAnalyses { namespace ZHfunctions {
    
struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    Vec_rp operator() (Vec_rp in, Vec_f iso);
  };

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (Vec_rp in, Vec_f iso) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if (iso[i] < m_max_iso) {
            result.emplace_back(p);
        }
    }
    return result;
}

 
// compute the cone isolation for reco particles
struct coneIsolation {

    coneIsolation(float arg_dr_min, float arg_dr_max);
    double deltaR(double eta1, double phi1, double eta2, double phi2) { return TMath::Sqrt(TMath::Power(eta1-eta2, 2) + (TMath::Power(phi1-phi2, 2))); };

    float dr_min = 0;
    float dr_max = 0.4;
    Vec_f operator() (Vec_rp in, Vec_rp rps) ;
};

coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max( arg_dr_max ) { };
Vec_f coneIsolation::coneIsolation::operator() (Vec_rp in, Vec_rp rps) {
  
    Vec_f result;
    result.reserve(in.size());

    std::vector<ROOT::Math::PxPyPzEVector> lv_reco;
    std::vector<ROOT::Math::PxPyPzEVector> lv_charged;
    std::vector<ROOT::Math::PxPyPzEVector> lv_neutral;

    for(size_t i = 0; i < rps.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(rps.at(i).momentum.x, rps.at(i).momentum.y, rps.at(i).momentum.z, rps.at(i).energy);
        
        if(rps.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }
    
    for(size_t i = 0; i < in.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z, in.at(i).energy);
        lv_reco.push_back(tlv);
    }

    
    // compute the isolation (see https://github.com/delphes/delphes/blob/master/modules/Isolation.cc#L154) 
    for (auto & lv_reco_ : lv_reco) {
    
        double sumNeutral = 0.0;
        double sumCharged = 0.0;
    
        // charged
        for (auto & lv_charged_ : lv_charged) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_charged_.Eta(), lv_charged_.Phi());
            if(dr > dr_min && dr < dr_max) sumCharged += lv_charged_.P();
        }
        
        // neutral
        for (auto & lv_neutral_ : lv_neutral) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_neutral_.Eta(), lv_neutral_.Phi());
            if(dr > dr_min && dr < dr_max) sumNeutral += lv_neutral_.P();
        }
        
        double sum = sumCharged + sumNeutral;
        double ratio= sum / lv_reco_.P();
        result.emplace_back(ratio);
    }
    return result;
}
 
 
 
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
    return eta1 - eta2;
  }

float deltaPhi(float phi1, float phi2){
    float PHI = 3.14159265;
    return PHI - std::abs(std::abs(phi1-phi2) - PHI);
  }

float deltaR(float phi1, float phi2, float eta1, float eta2) {
    return sqrt(deltaEta(eta1,eta2)*deltaEta(eta1,eta2) + deltaPhi(phi1,phi2)*deltaPhi(phi1,phi2));
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

ROOT::VecOps::RVec<TLorentzVector> build_p4_class(TLorentzVector v1, TLorentzVector v2) {
    ROOT::VecOps::RVec<TLorentzVector> result;
    result.push_back(v1);
    result.push_back(v2);
    return result;
}

ROOT::VecOps::RVec<TLorentzVector> boosted_p4(TLorentzVector boost, ROOT::VecOps::RVec<TLorentzVector> vec) {
    ROOT::VecOps::RVec<TLorentzVector> result;
    for (size_t i = 0; i < vec.size(); ++i) {
        TLorentzVector boosted=vec[i];
        boosted.Boost( - boost.BoostVector());
        result.push_back(boosted);
    }
    return result;
}

TLorentzVector boosted_p4_single(TLorentzVector boost, TLorentzVector vec) {
    vec.Boost( - boost.BoostVector());
    return vec;
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
        float tauID=-1;
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
            if (sqrt(jc.momentum.x*jc.momentum.x+jc.momentum.y*jc.momentum.y)>lead.Pt() && jc.charge!=0){
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
}}

#endif
