# Instruction for $H\to\tau\tau$ cross-section analysis

- [Instruction for $H\\to\\tau\\tau$ cross-section analysis](#instruction-for-htotautau-cross-section-analysis)
  - [Generating your own events](#generating-your-own-events)
    - [LHE files](#lhe-files)
    - [Pythia+Delphes](#pythiadelphes)
  - [Analysis](#analysis)
    - [FCCAnalyses setup](#fccanalyses-setup)
    - [Running the analysis](#running-the-analysis)
    - [How to add new functions to call in the stage1](#how-to-add-new-functions-to-call-in-the-stage1)
  - [Visualization](#visualization)
  - [Statystical analysis with Combine](#statystical-analysis-with-combine)

## Generating your own events

Instructions adapted from [https://github.com/zuoxunwu/FCCeePhysicsPerformance/blob/BuBc_dev/case-studies/BSM/LLP/DisplacedHNL/HNL_sample_creation/Readme.txt](https://github.com/zuoxunwu/FCCeePhysicsPerformance/blob/BuBc_dev/case-studies/BSM/LLP/DisplacedHNL/HNL_sample_creation/Readme.txt). 

FCC official winter 23 samples have been created with Pythia8 and Delphes 3.5.1pre05 as stated [here](https://github.com/HEP-FCC/FCCeePhysicsPerformance/blob/master/General/README.md#common-event-samples). You can have access to them if you are working in lxplus (and have a computing CERN account) or if you have access to the KIT machines (`root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA`). To get the list of centrally produced samples there is [this website](https://fcc-physics-events.web.cern.ch/FCCee/winter2023/Delphesevents_IDEA.php) and the JSON file (you need a CERN account to view it):

```
/afs/cern.ch/work/f/fccsw/public/FCCDicts/FCCee_procDict_winter2023_IDEA.json
```

If you want to use a sample that is not there, i.e. your favourite BSM model, you will need to generate it yourself, making sure that the format of the hadronisation and detector simulation agrees with the winte 23 campaign. The following paragraph will guide on how to do this.

### LHE files

These are the instructions to generate samples starting from Madgraph. More information can be found in [this set of slides](https://indico.jlab.org/event/413/contributions/7694/attachments/6580/8909/Hands-onStartToMG.pdf). If you want to use Pythia, skip ahead.

1. First of all, install [Madgraph](http://madgraph.phys.ucl.ac.be) by downloading the latest version (check it on the website):

    ```
    wget https://launchpad.net/mg5amcnlo/3.0/3.6.x/+download/MG5_aMC_v3.5.7.tar.gz
    tar -xfz MG5_aMC_v3.5.7.tar.gz
    cd MG5_aMC_v3.5.7
    ```

    Now you can run Madgraph by calling:
    ```
    ./bin/mg5_aMC
    ```
    You can follow the official tutorial by typing `tutorial` inside the Madgraph shell.

    For HNL signal samples, the HeavyN model needs to be added in the `models` directory if it's not already in the model list (MG5_aMC>display modellist): download the file `​SM_HeavyN_CKM_AllMasses_LO.tgz` from [https://feynrules.irmp.ucl.ac.be/wiki/HeavyN](https://feynrules.irmp.ucl.ac.be/wiki/HeavyN) and unzip it (tar -xf). Similar with your favourite UFO model (this is the format used by many generators to understand what are the particles and interactions in the model which expands the SM).

2. Then you can start generating LHE files. You can do this efficiently by writing all of your commands in a .txt file (see `mg_ee_eeH_Htautau.txt` for example) and passing the appropriate card to Madgraph:

    ```
    ./bin/mg5_aMC mg_ee_eeH_Htautau.txt
    ```

    The LHE file is in the directory you have indicated (`MG5_aMC_v3.5.7/eeH_Htautau/Events/run_01`) and is always name `unweighted_events.lhe.gz` (note: this is a zip file, to look into it unzip with `gzip -d unweighted_events.lhe.gz`). There is also the banner `run_01_tag_1_banner.txt` which is the initial part of the Madgraph .lhe file where all the details of the enration, cross section and number of events are listed. This is not part of the .lhe standard file per se but something specific to Madgraph. 

    Otherwise, you can get some info from the header:
    ```
    <init>
    -11 11 4.559400e+01 4.559400e+01 0 0 0 0 -4 1
    1.093647e-02 4.421059e-06 1.094628e-02 1
    <generator name='MadGraph5_aMC@NLO' version='3.5.4'>please cite 1405.0301 </generator>
    </init>
    ```
    which tells you the particles you collide (-11 11-> e+ e-), the energy of the respective beams in GeV (4.559400e+01 4.559400e+01), the cross section in pb in the second row, first element (1.093647e-02).
    
    If you scroll down the .lhe file you will see it beginngs with `<event>`. Each block is one event:
    ```
        <event>
    6      1 +1.0946278e-02 4.81214300e+01 7.54677100e-03 1.30620000e-01
        -11 -1    0    0    0    0 +0.0000000000e+00 +0.0000000000e+00 +4.5593999997e+01 4.5594000000e+01 5.1100000000e-04 0.0000e+00 -1.0000e+00
        11 -1    0    0    0    0 -0.0000000000e+00 -0.0000000000e+00 -4.5593999997e+01 4.5594000000e+01 5.1100000000e-04 0.0000e+00 1.0000e+00
        -11  1    1    2    0    0 +1.8218980787e+00 +5.7512719916e+00 -1.2382217277e+00 6.1587040389e+00 5.1100000000e-04 0.0000e+00 -1.0000e+00
        11  1    1    2    0    0 +3.0535394536e+00 +9.6634542572e+00 -2.0831119998e+00 1.0346294372e+01 5.1100000000e-04 0.0000e+00 1.0000e+00
        12  1    1    2    0    0 +1.8791933610e+01 +1.7026292112e+01 +1.8882992851e+01 3.1616432608e+01 0.0000000000e+00 0.0000e+00 -1.0000e+00
        -12  1    1    2    0    0 -2.3667371142e+01 -3.2441018361e+01 -1.5561659124e+01 4.3066568980e+01 0.0000000000e+00 0.0000e+00 1.0000e+00
    </event>
    ```
    (Ignoring the first line) The first column is the [PID of the particle](https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf). The second is the generator status: it is specific for each generator but in general it's -1 for initial state particles, 2 for intermediate state, 1 for final state. The third and fourth column tells you the decay chain, who is the mother, who is the daughter. The fifth and sixth columns are for colored particles. Then comes px, py, pz, e, mass and spin.

### Pythia+Delphes

There are now two ways of doing this step. You can install [Pythia8](https://pythia.org/documentation/) and [Delphes](https://cp3.irmp.ucl.ac.be/projects/delphes/wiki/WorkBook) inside Madgraph (`install pythia8` etc.) or use the key4hep stack where the software is distributed without you having to download it. 

For the first way, you can have a look into the Madgraph card that we used before and see that we have turned on both software and indicated the full path to the respective cards (`card_IDEA.tcl` for Delphes and `pythia.cmd` for Pythia). The output is standard Delpehs and you can access the classes by looking into the .root file created with ROOT TBrowser (install root from [here](https://root.cern/install/)):

```
root output_delphes.root
TBrowser t
```

To create a root file of the event after the detector reconstruction in the EDM4Hep format (common for future colliders studies) instead, you need to source the key4hep stack version used in the winter 2023 campaign or the output will not be compatible:

```
source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2022-12-23/x86_64-centos7-gcc11.2.0-opt/ll3gi/setup.sh
```

More information on the version used can be found [here](https://github.com/HEP-FCC/EventProducer/blob/master/config/param_FCCee.py#L46).

The command to produce root files in Delphes with Pythia hadronization and EDM4Hep format is this:

```
DelphesPythia8_EDM4HEP config_file output_config_file pythia_card output_file
```

The `config_file` is the detector card, it can be found [here](https://github.com/HEP-FCC/FCC-config/blob/winter2023/FCCee/Delphes/card_IDEA.tcl) for the IDEA detector for winter 2023 production. The `output_config_file` is found [here](https://github.com/HEP-FCC/FCC-config/blob/winter2023/FCCee/Delphes/edm4hep_IDEA.tcl). Both can be obtained by cloning the winter 2023 branch of [HEP-FCC/FCC-config](https://github.com/HEP-FCC/FCC-config/tree/winter2023).

In the Pythia card `pythia_card` the path to the unzipped LHE file must be given correctly, alongside the other commands. You can find a standard Pythia card at `pythia.cmd`.

The `output_file` is the EDM4Hep root file you want to produce.

**Note**: you need to pass the full path to the cards if they are not in the same directory where you are running the command from.

**Bonus**: if you want to generate events with Pythia, effectively skipping Madgraph (only easy when it' a SM process or something that does not require a UFO), then you can modify the Pythia card in a similar way as `pythia_gen.cmd`. Here we generate e+ e- > Z(ee/mumu)H(tautau) where both taus decay only to pi nu. For more commands, go through the Pythia [documentation](https://pythia.org//latest-manual/Welcome.html).

## Analysis

### FCCAnalyses setup 

1. First of all you need to clone or fork this FCCAnalyses repository to set up the working environment in lxplus/kit machines/linux environment. Go to the directory in your file system where you want to have FCCAnalyses and the do:

    ```
    git clone git@github.com:sofiagiappichini/FCCAnalyses.git
    git checkout higgs
    cd FCCAnalyses
    source ./setup.sh
    fccanalysis build
    ```

    **Note**: this particular branch for tutorials lives in the higgs branch of the repository so we need to move there.

2. When beginning a new session do:

    ```
    cd FCCAnalyses
    source ./setup.sh
    ```

3. Move to the analysis directory to find the analysis files:

    ```
    cd FCCAnalyses/examples/FCCee/higgs/tautau/xsec/tutorial
    ```

### Running the analysis

There are three (fundamental, maybe more depending on the analysis) steps for each analysis. FCCAnalyses is based on RDataFrame. You could use your own python script using uproot or ROOT, or even coffea (more info on this will follow in the future). At this stage, the use of FCCAnalyses is highly encouraged since most things you will need have already been developed by somebody else.

**Always check that the input/output directories for each stage are the correct ones, change them in the first few lines of each file.**

1. First of all, we want to creat n-tuples out of the Delphes output which is organised in ROOT trees. You can look into .root files with ROOT interactive web interface:

    ```
    root --web=off
    TBrowser t
    ```

    This is achieved in what we call stage1. The python script is called `analysis_stage1.py` and you can see some comments in it that will guide you in expanding it and saving all the variables that you want. There we use functions that are defined in `FCCAnalyses/analyzers/dataframe/src` but we can add costum C++ function in the file `functions.h`. To run this stage do: 

    ```
    fccanalysis run analysis_stage1.py
    ```

    Remember to update the other stages as well to get the plots of the variables you added.

    **Addendum**: you can have a second stage (stage2) and third and so on where you add iteratevely more variables. You will have access to the variables already saved in the previous step and if you want to have them all in the end you need to add them to the `branchList` of each stage. To run these stages you use the same command as stage1.

2. Now, we still have a tree structure of our files and we want to convert to histograms (ROOT TH1 or TH2) and apply some kinematic selection to our events.
   
    **Note**: you can add a selection in stage1/2/.. with the `.Filter()` method. Choose the best method that works for your analysis but remember that if you select events in final then you have the possibility of doing so iteratevely without having to run stage1 (which is slower than final) multiple times.

    In `analysis_final.py` you can add your chosen selection, using the variables defined in the previous stage and add the histograms, specifying the name, title, number of bins and range. The step will also create a latex table with the number of events after each selection and the efficiency. You can choose if you want to scale your events to the appropriate luminosity and cross-section or not.
    
    To run the stage do:

    ```
    fccanalysis final analysis_final.py
    ```

3. To create the plots for the histograms you just made, one easy way is to look into `analysis_plots.py`. There you can add the list of variables you want to plot, the list of signal and backgorund processes (at least one backgorund is required), choose the colors, legend labels and other stylistic parameters. You cna plot multiple selections at the same time. To run this do:

    ```
    fccanalysis plots analysis_plots.py
    ```
    Alternatively, you can develop your own python script to plot TH1 histograms. If you do so, make them look as close as the ones from this script for official pubblications.

**Note**: if you want to know why those commands work the way they do, have a look at `FCCAnalyses/python`.

### How to add new functions to call in the stage1

To add new functions that take any argument and that will be useful to either select or build new variables in analysis_stage1.py these are the steps (assuming the function is written in C++):

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

5. As said before, you can also add the functions in `functions.h` and you will not have to build again and do any of the other steps. Be aware that sometimes you will not be able to do this because of the type of objects you want.

## Visualization

You can visiualize single events in an event display fashion via the website [https://fccsw.web.cern.ch/fccsw/phoenix/](https://fccsw.web.cern.ch/fccsw/phoenix/), selecting the IDEA detector geometry (so you don't have to load this too). You will now see the detctor layers (can be modified or removed via the menu) and now you need to load your events. To do this, you first need to have simulated edm4hep files including the detcetor simulation (i.e. files from Delphes or GEANT). After sourcing the usual key4hep stack, run the command 

```
edm4hep2json $PATH_TO_YOUR_EVENTS.root
```

which will result in a json file containing the event info. Some options:

- `-n 10` to only keep 10 events,
- `-l ReconstructedParticles,Particle,DCH,...` to list the classes you want the file to have in the end. These can be seen in the ROOT TTree structure (names without a #, as these are reference classes).

Then upload this json file to the website and from the menu again you can change the color and which classes to visualize. You can now save the visualization and play with it.

**Note**: this works for both fast and full simulation. For fast simulation you can only see tracks, jets, and missing energy and for full simulation you can see the individual hits in the detector layers and the reconstructed tracks or jets only if this is implemented in your workflow (try with different stages and see what is available).

## Statystical analysis with Combine

You now have all the elements you need to obtain the measurement. This is done with [Combine](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/). This is a tool developed for the CMS Higgs searches and it applies all the statistical concepts so you don't have to do it by hand. But you will need to make a datacard, i.e. a .txt file telling Combine what are your processes and how the histograms look like or how many events you have. The instructions on how to do that can be found [here](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/part2/settinguptheanalysis/?h=data). You have an example of one at `datacard.txt`. The format is pretty rigid, please follow it to ensure the least ammount of trouble with Combine.

You can either follow the direction to install Combine standalone or in a CMSSW distribution (if you are a CMS member) or use the version already installed at KIT. To load this last option you need to do from an ETP machine and a **new shell** (otherwise there will be conflicts in python versions and so on):

```
cd /work/sgiappic/CMSSW_14_1_0_pre4/
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
cd /path/to/your/datacard/
```

Then you also need to know what statistical variable you want to compute and the corresponding command to do this. For the cross-section relative uncertainty we will use:

```
text2workspace.py datacard.txt -o ws.root
combine -M FitDiagnostics -t -1 --expectSignal=1 ws.root --rMin -10  --cminDefaultMinimizerStrategy 0 --robustFit 1 >output.txt
```

This will print the result of the fit into `output.txt`. You can remove `>output.txt` from the previous line if you only want the reuslt to be visualised on your screen.

To get the significance:
```
combine -M Significance datacard.txt -t -1 --expectSignal=1
```
