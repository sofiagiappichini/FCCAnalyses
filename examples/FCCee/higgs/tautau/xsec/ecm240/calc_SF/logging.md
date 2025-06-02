# Week 05.05.2025-11.05.2025
- new function for matching reco and gen particles by index for electron, photon, muon
- matching for quarks and jets based on charge does not work well
    - plan to replace it with matching for charged and neutral hadrons by index
- GaussFit for IDEA works great for CMS1 and CMS2, but does not suit IDEA
    - shift to FWHM
- first test of smearing for electrons with smearfactors around 20 
    - is not sufficient and FWHM stays the same (suspicious)
    - check on electron mass -> is super sharp, should not cause problems
    - check on mismatching -> does not happen
    - check on negative smeared_p values -> happens in around 30% of all cases
        - select only electrons with Z as parent
            - no were found
            - check for tau as parent: increases the smearfactor to 67 (CMS2) and 78 (CMS1), but still not sufficient; FWHM stays still the same, also problems with low event yields
                - found another peak around -1 in IDEA momentum resolution plot, when asked for tau as parent

# Week 12.05.2025-18.05.2025
- check on electron parents: all electrons come from muons or taus
- check on muon parents: all muons come from muons???
- smearing for muons: much better, but based on FWHM overshoots https://etpwww.etp.kit.edu/~awiedl/detector_res/mumu/Muon_p_res_total.png
- Monday-Meeting with Xunwu:
    - new calculation for FWHM: 1. GaussFit between -2sigma to 2sigma
                                2. 1000 bins, scan in 5 bin steps for the integral within 2*sigma around the maximum, for half maximum
    - MC-Electrons are reconstructed as Photons for IDEA -> solution: read in RecoElectrons
- fitting resolution for e, mu and gamma works quite solid now, only small deviations
- for IDEA many neural hadrons are mismatched, also small shift for CMS1 + 2
- charged hadrons work ok for CMS2, but also small shift for CMS1 and not enough smearing  

# Week 19.05.2025-25.05.2025
- more reconstructed neutral hadrons than MC neutral hadrons -> missmatching
- for CMS1 lowest number of neutral hadrons per event
- ckecks on eta and dR: nothing unexpected
- created 2 subsets with dR < 0.01 and dR > 0.06: 
    - checks on MC-PDG: dR > 0.06 mainly charged Pions and Kaons, dR < 0.01 still contains protons 
- fitting only neutral hadron dR<0.01:
    - CMS2: SF 2.24087
    - CMS1: SF 5.93010
    - not enough smearing, understandable since many mismatched charged hadrons do not get proper smearing
- fitting jet reso -> poor fit -> change to scan for FWHM
    - CMS2: SF 2.49057
    - CMS1: SF 3.00629
    - not enough

# Week 26.05.2025-01.06.2025
- FWHM scan for low dR neutral hadrons:
    - CMS2: SF 2.5
    - CMS1: SF 2.53125
    - not enough
- Meeting: smearing based on dijet mass
    - sigma = sqrt(sigma_cms^2-sigma_idea^2)
    - p_jet_idea rn gauss smearing with sigma
- Dijet mass shape is off
- function for jets smearing build -- not tested 

# Week 02.06.2025-08.06.2025
