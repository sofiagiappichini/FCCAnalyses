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
    - new calculation for FWHM: 1. GaussFit between -2*sigma to 2*sigma
                                2. 1000 bins, scan in 5 bin steps for the integral within 2*sigma around the maximum, for half maximum
    - MC-Electrons are reconstructed as Photons for IDEA -> solution: read in RecoElectrons