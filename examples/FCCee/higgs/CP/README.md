# Instruction for Higgs CP analysis

The instructions mainly follow the LLP tutorial [https://github.com/jalimena/LLPFCCTutorial/blob/main/README.md](https://github.com/jalimena/LLPFCCTutorial/blob/main/README.md)

- [Instruction for Higgs CP analysis](#instruction-for-higgs-cp-analysis)
  - [FCCAnalyses setup](#fccanalyses-setup)
  - [Running the analysis](#running-the-analysis)
    - [How to add new functions to call in the stage1](#how-to-add-new-functions-to-call-in-the-stage1)
    - [Changes made to the general code](#changes-made-to-the-general-code)
  - [Additional codes](#additional-codes)
    - [Access LHE files](#access-lhe-files)
    - [LHE conversion to ROOT](#lhe-conversion-to-root)
    - [Access histograms](#access-histograms)
    - [Rebinning](#rebinning)
    - [Cut optimizer](#cut-optimizer)
    - [Plots](#plots)
    - [Combine](#combine)
    - [Other](#other)

## FCCAnalyses setup 

1. Fork Sofia's version  of [FCCAnalyses](https://github.com/sofiagiappichini/FCCAnalyses) (official version is moving to EDM4Hep 1.0 which makes things more complicated to run on the Winter 23 samples) to set up the working environment in lxplus (or other space).

    **Note:** FCC-LLP/FCCAnalyses hasn't been kept up to date with the main repository so it's best to fork the [official version](https://github.com/HEP-FCC/FCCAnalyses).

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
    source /cvmfs/sw.hsf.org/key4hep/releases/2023-11-23/x86_64-almalinux9-gcc11.3.1-opt/key4hep-stack/2023-11-30-gyuooo/setup.sh
    source ./setup.sh
    ```

3. Move to the Higgs CP directory to find the analysis files:

    ```
    cd FCCAnalyses/examples/FCCee/higgs/CP
    ```

## Running the analysis

**Always check that the input/output directories for each stage are the correct ones, change them in the first few lines of each file.**

1. Run the first/second stage to create trees for the events from the Higgs CP directory:

    ```
    cd FCCAnalyses/examples/FCCee/higgs/CP
    fccanalysis run analysis_stage1.py
    fccanalysis run analysis_stage2.py
    ```

    This is the stage where you can add or modify the variables that you want to save in the trees, remember to update the other stages as well to get the plots.

    In the first stage simple variables are builkt for thrut and reconstructed particles. In the second stage, complex variables are built from the information from the stage1. In stage 2 you can also filter events by requiring or not to have certain particles present, i.e. differentiate decay channels.

2. Then run the chosen selections on top of that:

    ```
    fccanalysis final analysis_final.py
    ```

    The selections are based on the objects stored in the trees in the first stages. The step will also create a latex table with the number of events after each selection and the efficiency. If you want the historgams and number of events in the table to be scaled to the respective luminosity and cross section, turn on the corresponding option.

3. `replot.py` is inspired by `do_plots.py`. It allows to plot log scale x axis and it's made to be more adaptable. The current version stacks backgrounds and not signals. Plots for only one group can be done. Also, there is the possibility of having a logarithmic scale for y or x.

    ```
    python replot.py
    ```

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

In [`FCCAnalyses/python/run_final_analysis.py`](https://github.com/sofiagiappichini/FCCAnalyses/blob/master/python/run_final_analysis.py) I changed how the efficiencies are written in the table in scientific notation and with the same format as the number of events, the scaling applied now includes the luminosity (`luminosity * cross section * k factor * matching efficiency * efficiency`). 

Because of that, the plotting code is modified to not scale to the luminosity anymore but simply takes the argument to print it onto the plots. In this way, the histograms are correctly scaled in the `final` step and can be used as input into CMS Combine with the correct number of expected events.

Note: the uncertainty on the number of events that is saved in the tables is the square root of the efficiency multiplied by the rest of the factors.

More functions have been introduced to work with the tau tagging algorithm at [/afs/cern.ch/user/s/sgiappic/FCCAnalyses/install/python/addons/FastJet/jetClusteringHelper.py](/afs/cern.ch/user/s/sgiappic/FCCAnalyses/install/python/addons/FastJet/jetClusteringHelper.py) and (/afs/cern.ch/user/s/sgiappic/FCCAnalyses/addons/FastJet/python/jetClusteringHelper.py)[/afs/cern.ch/user/s/sgiappic/FCCAnalyses/addons/FastJet/python/jetClusteringHelper.py].

## Additional codes

Some additional python codes have been made to automate certain tasks. They can be found [here](https://github.com/sofiagiappichini/FCCAnalyses/blob/master/examples/FCCee/bsm/LLPs/DisplacedHNL/codes).

### Access LHE files

`cpy_lhe.py` copies the .lhe files form the Madgraph directories into a different directory changing the name of each to to reflect the coupling and mass values.

`get_decay_length_lhe.py` accesses .lhe files to retrieve information about each event and compute the decay length. This one is also evaluated from the computed width of the particle.

`get_weight_lhe.py` and `get_weight_banner.py` extract the cross section values from the .lhe files. The first one writes them in the format used in `analysis_final.py`(remember to change the square brackets to curly afterward). The second needs to be called inside the directory where the runs are stored and it's just for preliminary checking all the values at a glance.

`mass_scan.py` accesses the basic .lhe info (cross section and error) and plots them. The values are put into global arrays that are then split according to the input files and runs of each sample.

### LHE conversion to ROOT

`replace_input_delphes.py` automatically converts all the .lhe files given in the list to .root files with the process described in the previous section. It needs to be run in the directory where the cards are stored.

### Access histograms

`get_decay_length.py` looks through histograms (.root files) to get the mean value of a variable. It can loop over multiple variables and files. It also returns the total number of entries.

`get_PID.py` looks through histograms (.root files) to get the values of a variable. It can loop over multiple variables and files. It also returns the total number of entries.

### Rebinning

`rebinning.py` rebins one variable (histogram stored in .root file) given a generic array of lower edges (they need to be a subgroup of the original edges). It loops over multiple cuts and files, the output is one .root file with all the histograms rebinned with names `$PROCESS_$CHANNEL`. It can also then plot the rebinned variable, grouping some backgrounds together and adding the same and different flavor events.

### Cut optimizer

`cut_optimizer.py` looks at one variable at a time to see what cut would result in higher significance from $\frac{S}{\sqrt{S+B}}$. It loops over all the backgrounds to get the cumulative number and also multiple signals to check different options. Cuts can be either up to or from a value. It's not possible to check multiple cuts at once as there is no information in the histograms on how the events are related across different variables, successive cuts need to be implemented on the full selection coming from the final stage analysis.

### Plots

`replot.py` is inspired by `do_plots.py`. It allows to plot log scale x axis and it's made to be more adaptable. The current version stacks backgrounds and not signals. Plots for only one group can be done.

### Combine

`replace_input_combine.py` automates getting the significance of the events. It loops over signal files so the datacard can be updated properly and the significance is written on a file. It assumes that all signal events have the same uncertainty. The backgrounds are manually listed in the datacard. It needs to be run from the Combine directory after installation of CMSSW.

`significance_plots.py` plots the values of the significance obtained from Combine with and without log scale for the coupling. First of all the input files are divided so that two different sets of data can be extracted and plotted separetely. Then there is the distinction between the scales and methods used for the creation of the grid. `nevents_plots.py` does the same thing.

### Other

`tertiary_plot.py` makes a tertiary plot from some data file and points for the HNLs couplings.

`future_constraint.py` makes an exclusion and significance plot for the HNL scenario, with data from other experiments and private analyses. The x and y values of each set of data are in logaritmic scale but converted back to agree with the private plots.