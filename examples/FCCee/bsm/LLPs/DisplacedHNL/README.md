# Instruction for HNL analysis

The instructions mainly follow the LLP tutorial [https://github.com/jalimena/LLPFCCTutorial/blob/main/README.md](https://github.com/jalimena/LLPFCCTutorial/blob/main/README.md)

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

1. First of all, install Madgraph on lxplus by downloading the latest version and send the file to lxplus:

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

To create a root file of the event after the detector reconstruction in the EDM4Hep format you need to source either FCCAnalyses setup or 

```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

or the equivalent (newer for FCCSW sourcing):

```
source /cvmfs/sw.hsf.org/key4hep/setup.sh
```

The command to produce root files in Delphes with Pythia hadronization and EDM4Hep format is this:

```
DelphesPythia8_EDM4HEP DelphesPythia8config_file output_config_file pythia_card output_file
```

The `DelphesPythia8config_file` is the detector card, it can be foun [here](https://github.com/HEP-FCC/FCC-config/blob/winter2023/FCCee/Delphes/card_IDEA.tcl) for the IDEA detector for winter 2023 production. The `output_config_file` is found [here](https://github.com/HEP-FCC/FCC-config/blob/winter2023/FCCee/Delphes/edm4hep_IDEA.tcl). Both can be obtained by cloning the winter 2023 branch of [HEP-FCC/FCC-config](https://github.com/HEP-FCC/FCC-config/tree/winter2023).

In the Pythia card `pythia_card` the path to the unzipped LHE file must be given correctly, alongside the other commands.

The `output_file` is the EDM4Hep root file cointaning the sample that needs to be analysed.

**Note:** all the cards for Madgraph (one example with multiple run where the masses change), Pythia and Delphes (edm4hep) can be easily found at (https://github.com/sofiagiappichini/FCCAnalyses/tree/master/examples/FCCee/bsm/LLPs/DisplacedHNL/2HNL_sample_creation)[https://github.com/sofiagiappichini/FCCAnalyses/tree/master/examples/FCCee/bsm/LLPs/DisplacedHNL/2HNL_sample_creation].

Instructions to validate in the EDM4Hep format root files created in standalone MG+Pythia+Delphes can be found [here](https://github.com/zuoxunwu/FCCeePhysicsPerformance/tree/BuBc_dev/case-studies/BSM/LLP/DisplacedHNL) (not necessary, it does not produce an edm4hep file, just some histograms).


## Running the analysis

**Always check that the input/output directories for each stage are the correct ones, change them in the first few lines of each file.**

My comments to the general code begin and end with three #.

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
