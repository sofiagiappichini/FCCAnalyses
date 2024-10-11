# Instruction for Higgs CP analysis

- [Instruction for Higgs CP analysis](#instruction-for-higgs-cp-analysis)
  - [FCCAnalyses setup](#fccanalyses-setup)
  - [How to run an analysis (generic)](#how-to-run-an-analysis-generic)
    - [How to add new functions](#how-to-add-new-functions)
    - [Changes made to the general code](#changes-made-to-the-general-code)
  - [How to run the CP analysis (specific)](#how-to-run-the-cp-analysis-specific)
    - [Delphes samples](#delphes-samples)
    - [Stage 1 ntuples](#stage-1-ntuples)
    - [Stage2](#stage2)
    - [Final stage](#final-stage)
    - [Plotting](#plotting)
    - [Combine (not yet implemented)](#combine-not-yet-implemented)
    - [Maria Cepeda code](#maria-cepeda-code)

## FCCAnalyses setup 

1. Fork Sofia's version  of [FCCAnalyses](https://github.com/sofiagiappichini/FCCAnalyses/tree/higgs) (official version is moving to EDM4Hep 1.0 which makes things more complicated to run on the Winter 23 samples) to set up the working environment in lxplus (or other space).

    ```
    bash
    git clone git@github.com:HEP-FCC/FCCAnalyses.git
    cd FCCAnalyses
    source ./setup.sh
    mkdir build install
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=../install
    make install
    ```

2. When beginning a new session do:

    ```
    cd FCCAnalyses
    source ./setup.sh
    ```

    The `setup.sh` script has been modified to always get the correct version of the stack instead of the latest, `source /cvmfs/sw.hsf.org/key4hep/releases/2023-11-23/x86_64-almalinux9-gcc11.3.1-opt/key4hep-stack/2023-11-30-gyuooo/setup.sh`.

3. Move to the Higgs CP directory to find the analysis files:

    ```
    cd FCCAnalyses/examples/FCCee/higgs/tautau/CP
    ```

## How to run an analysis (generic)

**Always check that the input/output directories for each stage are the correct ones, change them in the first few lines of each file.**

1. Run the first/second stage to create trees for the events from the Higgs CP directory:

    ```
    fccanalysis run analysis_stage1.py
    fccanalysis run analysis_stage2.py
    ```

    This is the stage where you can add or modify the variables that you want to save in the trees, remember to update the other stages as well to get the plots.

    In the first stage simple variables are builkt for truth and reconstructed particles. In the second stage, complex variables are built from the information from the stage1. In stage 2 you can also filter events by requiring or not to have certain particles present, i.e. differentiate decay channels.

2. Then run the chosen selections on top of that:

    ```
    fccanalysis final analysis_final.py
    ```

    The selections are based on the objects stored in the trees in the first stages. The step will also create a latex table with the number of events after each selection and the efficiency. If you want the historgams and number of events in the table to be scaled to the respective luminosity and cross section, turn on the corresponding option.

### How to add new functions

To add new functions that take any argument and that will be useful to either select or build new variables in analysis_stage1.py these are the steps (assuming the function is written in cpp):

1. Open the file where new functions get written and add the new function, specifying the type, arguments, actions and return:

    ```
    FCCAnalyses/analyzers/dataframe/src/myUtils.cc
    ```

2. Only add the type of function, name and arguments to:

    ```
    FCCAnalyses/analyzers/dataframe/FCCAnalyses/myUtils.h
    ```

3. Go back to the main directory, source the setup and do a clean build (use this step also when modifying any code in  `FCCAnalyses/python` to update it):

    ```
    fccanalysis build --clean-build
    ```

4. Now you can use your function by calling it:

    ```
    .Define("variable", "myUtils::myFunction(arguments)")
    ```

Added custom functions: `myUtils::deltaR`, `myUtils::deltaEta`, `myUtils::deltaPhi`, `myUtils::build_p4`, `myUtils::boosted_p4`, `myUtils::get_scalar`, `myUtils::get_gamma`, `myUtils::get_ptvl`, ... , `MCParticle::sel_parentID`, `MCParticle::sel_daughterID`.

More functions have been introduced to work with the tau tagging algorithm at [/afs/cern.ch/user/s/sgiappic/FCCAnalyses/install/python/addons/FastJet/jetClusteringHelper.py](/afs/cern.ch/user/s/sgiappic/FCCAnalyses/install/python/addons/FastJet/jetClusteringHelper.py) and (/afs/cern.ch/user/s/sgiappic/FCCAnalyses/addons/FastJet/python/jetClusteringHelper.py)[/afs/cern.ch/user/s/sgiappic/FCCAnalyses/addons/FastJet/python/jetClusteringHelper.py].

One another way of adding custom function is to write them in the file `functions.h`. In this case there is no need to build the workspace again. The file needs to be uploaded in each stages were it is used in the preamble:

```
includePaths = ["functions.h"]
```

### Changes made to the general code

I've made a few changes to the analyzers. 

In [`FCCAnalyses/python/run_final_analysis.py`](https://github.com/sofiagiappichini/FCCAnalyses/blob/master/python/run_final_analysis.py) I changed how the efficiencies are written in the table in scientific notation and with the same format as the number of events. The scaling applied to the number of events and histograms now includes the luminosity and considers the number of events stated in the `procDictAdd` instead of the number of events in the trees. In this way the events are correctly scaled with the global cross section even when filtering out events in stage1. If the scaling is not applied then the number of events is the one in the trees.

Because of that, the plotting code is modified to not scale to the luminosity anymore but simply takes the argument to print it onto the plots. In this way, the histograms are correctly scaled in the `final` step and can be used as input into CMS Combine with the correct number of expected events.

Note: the uncertainty on the number of events that is saved in the tables is the square root of the number of events (scaled or not).

## How to run the CP analysis (specific)

### Delphes samples

The SM LO samples come from the [central winter 23 production](https://fcc-physics-events.web.cern.ch/FCCee/winter2023/Delphesevents_IDEA.php). For ZH at $\sqrt{s}=$240 GeV the samples are produced in [Wizard v. 3.0.3](https://github.com/HEP-FCC/FCC-config/tree/winter2023/FCCee/Generator/Whizard/v3.0.3) and showered with Pythia 6. The file names indicates the other particles besides the H (s channel Z -> ZH or if possible with the same final state WW -> H is also included) and also the decay of the H. The Delphes root files can be also found at ETP under `/ceph/sgiappic/HiggsCP/winter23`.

The EFT signal samples are stored under `/ceph/mpresill/FCCee/ZH_SMEFT_LO_noISR_noCuts_prod/'. More information [here](https://codimd.web.cern.ch/VIIxHnFJTAqRiUWzyDtOQw).


### Stage 1 ntuples

The ntuples contain information about the thruth level variables for final state electrons and muons, number of Z, final state neutrinos (all flavors together), and final state photons. For the thruth level tau variables there is one class with all taus (AllGenTau) and one for only after FSR or in case of no FSR at all taus (FSRGenTau), there is also `noFSRGenTau` which refers to the tau produced in the decay of the boson/quark. 

For the reconstructed particles there are:
- final state electrons, muons, leptons (electrons+muons)
- final state electrons, muon, leptons that have p>20 GeV, and are isolated (0.25) (`_sel`)
- final state photons, missing energy, primary and secondary tracks
- two jets classes, one with R5 removing the isolated letons and one with exclusive gen kt with 4 jets on all final state particles
- two reconstructed hadronic tau classes based respectively on the two jet classes 
- one jet class based on R5 with jets that are not being considered as tau jets (`_sel`)

### Stage2

After porcessing stage1 on all the available samples, in stage2 we define separate categories based on the decay products of the Z (LL, QQ, NuNu) and H bosons (LL, LH, HH, H means hadronic tau here). The selection to define the catagories is on the number of particles (leptons, hadronic taus, jets), on the charges (and flavor) of the lepton pairs from the Z, on the charges of the reconstructed taus. The gen-labeled stage2 containes CP sensitive variables for generated particles, while the unlabeled ones are for reconstructed particles. 

Two functions are available to determine the origin of two pairs of leptons when the final state has four, checking that the pair is neutral and same flavor, and one to determine the pair of leptons form the Z if there are three leptons, again checking that the pair is neutral and same flavor. The flavor check is done by considering the mass of the leptons. These can be found in `functions.h`, along with all the other functions used in stage2.

**Note**: the output should be in separate directories named after the final states so there is no confusion between the files.

### Final stage

Here we keep the same categories as stage2 and apply the respective cuts on kinematical variables. 

**Note**: the output should be in separate directories named after the final states so there is no confusion between the files.

### Plotting

`FCCAnalyses/examples/FCCee/higgs/tautau/CP/replot.py` is inspired by `do_plots.py`. It allows to plot log scale y axis and it's made to be more adaptable. The current version stacks backgrounds and not signals. Plots for only one group can be done. The histograms are organised by Z decay and H($ \tau\tau $) decay: processes for each type are merged into one histogram, common backgrounds are kept separate. For efficiency, the final stage root files need to be organised in corresponding directories based on Z decay with subdirectories on H decays.

Similarly, `FCCAnalyses/examples/FCCee/higgs/tautau/CP/replot_ratio.py` plots the variables alongside the ratios with the first sample, with uncertanty bands.

### Combine (not yet implemented)

To get the relative uncertainty on the $ H \to \tau \tau $ cross section, we can use [CMS Combine](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) to get the value from analyzing the signal and background histograms after final selection (shape based analysis).

To do this, we need to make datacards that combine uses as input. They can be created with `FCCAnalyses/examples/FCCee/higgs/tautau/CP/combine/make_datacards.py` for each respective category and for the combined ones. The code `FCCAnalyses/examples/FCCee/higgs/tautau/CP/combine/replace_input_combine.py` automatically sources the environment and computes the uncertainty, storing the output in a text file.

### Maria Cepeda code

The tau reco function is [here](https://github.com/mcepeda/FCCAnalyses/blob/master/analyzers/dataframe/src/myUtils.cc#L2559).
The stage1 Htautau script is [here](https://github.com/mcepeda/FCCAnalyses/blob/master/examples/FCCee/higgs/tautau/test/analysis_stage1_fromjets_win23.py).
And then [these files](https://github.com/mcepeda/ExamplesFCCee/tree/main/ZHTauTau) are for making plots.
