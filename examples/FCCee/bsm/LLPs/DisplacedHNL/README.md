# Instruction for HNL analysis

The instructions mainly follow the LLP tutorial [https://github.com/jalimena/LLPFCCTutorial/blob/main/README.md](https://github.com/jalimena/LLPFCCTutorial/blob/main/README.md)

- [Instruction for HNL analysis](#instruction-for-hnl-analysis)
  - [FCCAnalyses setup](#fccanalyses-setup)
  - [Generating your own samples](#generating-your-own-samples)
    - [LHE files](#lhe-files)
    - [Pythia+Delphes](#pythiadelphes)
  - [Running the analysis](#running-the-analysis)
    - [How to add new functions to call in the stage1](#how-to-add-new-functions-to-call-in-the-stage1)
    - [Changes made to the general code](#changes-made-to-the-general-code)
  - [Additional codes](#additional-codes)
    - [Access LHE files](#access-lhe-files)
    - [LHE conversion to ROOT](#lhe-conversion-to-root)
    - [Access histograms](#access-histograms)
    - [Rebinning](#rebinning)
    - [Plots](#plots)
    - [Combine](#combine)

## FCCAnalyses setup 

1. Following instructions given in [https://github.com/HEP-FCC/FCCAnalyses](https://github.com/HEP-FCC/FCCAnalyses), fork the FCC-LLP version [FCC-LLP/FCCAnalyses](https://github.com/FCC-LLP/FCCAnalyses) to set up the working environment in lxplus.

    **Note:** FCC-LLP/FCCAnalyses hasn't been kept up to date with main repository so it's best to fork the [official version](https://github.com/HEP-FCC/FCCAnalyses).

    ```
    bash
    git clone git@github.com:HEP-FCC/FCCAnalyses.git
    cd FCCAnlyses
    source ./setup.sh
    mkdir build install
    cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=../install
    make install
    ```

2. When beginning a new session do:

    ```
    cd FCCAnlyses
    source ./setup.sh
    ```

3. Move to the HNL directory to find the analysis files:

    ```
    cd FCCAnalyses/examples/FCCee/bsm/LLPs/DisplacedHNL
    ```

## Generating your own samples

Instructions adapted from [https://github.com/zuoxunwu/FCCeePhysicsPerformance/blob/BuBc_dev/case-studies/BSM/LLP/DisplacedHNL/HNL_sample_creation/Readme.txt](https://github.com/zuoxunwu/FCCeePhysicsPerformance/blob/BuBc_dev/case-studies/BSM/LLP/DisplacedHNL/HNL_sample_creation/Readme.txt). 

Winter 23 samples have been created with Pythia8 and Delphes 3.5.1pre05 as stated [here](https://github.com/HEP-FCC/FCCeePhysicsPerformance/blob/master/General/README.md#common-event-samples).

### LHE files

1. First of all, install Madgraph on lxplus by downloading the latest version and copying it in lxplus:

    ```
    scp MG5_aMC_version.tar.gz user@lxplus.cern.ch:/path/
    ```

    Or simply do from lxplus:

    ```
    wget https://launchpad.net/mg5amcnlo/3.0/3.5.x/+download/MG5_aMC_v3.5.3.tar.gz
    ```

    Then in lxplus unzip the file (tar -xf) and proceed with the installation:

    ```
    cd MG5_aMC_version
    ./bin/mg5_aMC
    ```

    For HNL signal samples, the HeavyN model needs to be added in the models directory if it's not already in the model list (MG5_aMC>display modellist): dowload the file `​SM_HeavyN_CKM_AllMasses_LO.tgz` from [https://feynrules.irmp.ucl.ac.be/wiki/HeavyN](https://feynrules.irmp.ucl.ac.be/wiki/HeavyN) and unzip it (tar -xf).

2. Then you can start generating LHE files by passing the appropriate card to Madgraph:

    ```
    ./bin/mg5_aMC mg5_proc_card.dat
    ```

    The LHE file is in the corresponding directory.

### Pythia+Delphes

To create a root file of the event after the detector reconstruction in the EDM4Hep format you need to source the key3hep stack version used in the winter 2023 campaign or the output will not be compatible:

```
source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2022-12-23/x86_64-centos7-gcc11.2.0-opt/ll3gi/setup.sh
```

More information on the version used can be found [here](https://github.com/HEP-FCC/EventProducer/blob/master/config/param_FCCee.py#L46).

The command to produce root files in Delphes with Pythia hadronization and EDM4Hep format is this:

```
DelphesPythia8_EDM4HEP DelphesPythia8config_file output_config_file pythia_card output_file
```

The `DelphesPythia8config_file` is the detector card, it can be found [here](https://github.com/HEP-FCC/FCC-config/blob/winter2023/FCCee/Delphes/card_IDEA.tcl) for the IDEA detector for winter 2023 production. The `output_config_file` is found [here](https://github.com/HEP-FCC/FCC-config/blob/winter2023/FCCee/Delphes/edm4hep_IDEA.tcl). Both can be obtained by cloning the winter 2023 branch of [HEP-FCC/FCC-config](https://github.com/HEP-FCC/FCC-config/tree/winter2023).

In the Pythia card `pythia_card` the path to the unzipped LHE file must be given correctly, alongside the other commands.

The `output_file` is the EDM4Hep root file containing the sample that needs to be analyzed.

**Note:** all the cards for Madgraph (one example with multiple runs where the masses change), Pythia and Delphes (edm4hep) can be easily found at [https://github.com/sofiagiappichini/FCCAnalyses/tree/master/examples/FCCee/bsm/LLPs/DisplacedHNL/2HNL_sample_creation](https://github.com/sofiagiappichini/FCCAnalyses/tree/master/examples/FCCee/bsm/LLPs/DisplacedHNL/2HNL_sample_creation).

Instructions to validate in the EDM4Hep format root files created in standalone MG+Pythia+Delphes can be found [here](https://github.com/zuoxunwu/FCCeePhysicsPerformance/tree/BuBc_dev/case-studies/BSM/LLP/DisplacedHNL) (not necessary, it does not produce an edm4hep file, just some histograms).


## Running the analysis

**Always check that the input/output directories for each stage are the correct ones, change them in the first few lines of each file.**

My comments on the general code begin and end with three #.

The stack had changed since the beginning of the analysis. To keep things consistent (mostly root version) from the FCCAnalyses directory do:

```
source /cvmfs/sw.hsf.org/key4hep/releases/2023-11-23/x86_64-almalinux9-gcc11.3.1-opt/key4hep-stack/2023-11-30-gyuooo/setup.sh
source ./setup.sh
```

1. Run the first stage to create trees for the events from the HNL directory:

    ```
    cd FCCAnalyses/examples/FCCee/bsm/LLPs/DisplacedHNL
    fccanalysis run analysis_stage1.py
    ```

    This is the stage where you can add or modify the variables that you want to save in the trees, remember to update the other stages as well to get the plots.

2. Then run the chosen selections on top of that:

    ```
    fccanalysis final analysis_final.py
    ```

    The selections are based on the objects stored in the trees in the first stage. The step will also create a latex table with the number of events after each selection and the efficiency.

3. To create the plots do:

    ```
    fccanalysis plots analysis_plots.py
    ```

    Open the file to make changes to how the plots look.


### How to add new functions to call in the stage1

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

### Changes made to the general code

I've made a few changes to the analyzers. 

First of all in [`FCCAnalyses/python/do_plots.py`](https://github.com/sofiagiappichini/FCCAnalyses/blob/master/python/do_plots.py) I changed the dimensions of the legends and how the yields are saved.

In [`FCCAnalyses/python/run_final_analysis.py`](https://github.com/sofiagiappichini/FCCAnalyses/blob/master/python/run_final_analysis.py) I changed how the efficiencies are written in the table in scientific notation and with the same format as the number of events, the scaling applied now includes the luminosity (`luminosity * cross section * k factor * matching efficiency * efficiency`). 

Because of that, the plotting code is modified to not scale to the luminosity anymore but simply takes the argument to print it onto the plots. In this way, the histograms are correctly scaled in the `final` step and can be used as input into CMS Combine with the correct number of expected events.

Note: the uncertainty on the number of events that is saved in the tables is the square root of the efficiency multiplied by the rest of the factors.

## Additional codes

Some additional python codes have been made to automate certain tasks. They can be found [here](https://github.com/sofiagiappichini/FCCAnalyses/blob/master/examples/FCCee/bsm/LLPs/DisplacedHNL/codes).

### Access LHE files

`get_decay_length_lhe.py` accesses .lhe files to retrieve information about each event and computes the decay length. This one is also evaluated from the computed width of the particle.

`get_weight_lhe.py` and `get_weight_banner.py` extract the cross section values from the .lhe files. The first one writes them in the format used in `analysis_final.py`(remember to change the square brackets to curly afterwards). The second needs to be called inside the directory where the runs are stored and it's just for preliminary checking all the values at a glance.

### LHE conversion to ROOT

`replace_input_delphes.py` automatically converts all the .lhe files given in the list to .root files with the process described in the previous section. It needs to be run in the directory where the cards are stored.

### Access histograms

`get_decay_length.py` looks through histograms (.root files) to get the maximum value of a variable. It can loop over multiple variables and files. It also returns the total number of entries.

### Rebinning

`rebinning.py` rebins one variable (histogram stored in .root file) given a generic array of lower edges (they need to be a subgroup of the original edges). It loops over multiple cuts and files, the output is one .root file with all the histograms rebinned with names `$PROCESS_$CHANNEL`.

### Plots

`replot.py` is heavily inspired by `do_plots.py`. It allows to plot log scale x axis and it's made to be more adaptable. The current version stacks backgrounds and not signals. Plots for only one group can be done.

### Combine

`replace_input_combine.py` automates getting the significance of the events. It loops over signal files so the datacard can be updated properly and the significance is written on a file. It assumes that all signal events have the same uncertainty. The backgrounds are manually listed in the datacard. It needs to be run from the Combine directory after installation of CMSSW.