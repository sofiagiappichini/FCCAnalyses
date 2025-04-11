# Instruction for usage of BDT 

- [Instruction for usage of BDT](#instruction-for-usage-of-bdt)
  - [Setup](#setup)
  - [BDT training](#bdt-training)
  - [BDT use](#bdt-use)
  - [Combine on the BDT output](#combine-on-the-bdt-output)

## Setup

This instructions assume you already setup FCCAnalyses as written [here](https://github.com/sofiagiappichini/FCCAnalyses/blob/higgs/examples/FCCee/higgs/tautau/xsec/README.md).

To run the BDT script, you need to have a local installation of Python (version > 3.10 to work with all the dependencies):

```
wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
tar -zxvf Python-3.10.13.tgz
cd Python-3.10.13
mkdir ~/.localpython
./configure --prefix=/PATH_TO_INSTALLATION/.localpython
make
make install
```

Then you need to copy [this file](https://github.com/zuoxunwu/FCCeePhysicsPerformance/blob/BuBc_dev/case-studies/flavour/tools/install.sh) and [this one](https://github.com/zuoxunwu/FCCeePhysicsPerformance/blob/BuBc_dev/case-studies/flavour/tools/localSetup.sh) and source them both in succession passing the path to your local python istallation (`/work/user/Python`).

Every time you log into a new shell, you nedd to source the second file with the absolute path given:

```
source ./localSetup.sh /ceph/sgiappic/Python-3.10.13
```

## BDT training

The training is handeled by the script `/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/training/train_bdt_{}.py`. Lists of variables, signal and background processes are defined in the beginning. The variables used for training are exactly the same ones required for later application. It takes stage2 (or alternatevely stage1) files as input.

A weight column is added in the DataFrames for all processes to be later used as weight of events in the BDT fit, according to corss section, luminosity and raw number of events.

**Note:** The samples that the training and application should be applied to can be found at `/ceph/awiedl/FCCee/HiggsCP/stage2_241025_cut`. For the NuNu catgeories a cut was applied on `RecoEmiss_e>100`, while for QQ it's `100<Collinear_mass<150`, this helps steer the traingin in the right direction. This samples have tau defined from the jet tagger.

## BDT use

We apply the trained BDT to stage2 by plugging it in as in [this example](https://github.com/zuoxunwu/FCCAnalyses/blob/3d872a8bd6098bb8935fa41c0202b6a7886b06d7/examples/FCCee/flavour/BuBc2TauNu/analysis_stage2.py#L104-L111) in a stage3 script (`/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3`). 

The initialization of the BDT requires you to specify the exact number of variables used for trining that will also have to be passed to the function in the code. The BDT output is a vector of float so you need to take the first element to get the score value: 0 corresponding to background-like events, 1 for signal-like.

After having processed stage3 and final with the BDT score (`/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/final`), some processes need to be merged into one sample for easier visualisation and to have less statistica fluctuations in combine. This is done with the script `/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/merge_histos.py`, the variables to be merged need to be specified.

## Combine on the BDT output

First of all, you need to set uo the right enviornment. Either install [Combine](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/) or do these steps from ETP machines:

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /work/xzuo/combine_test/CMSSW_14_1_0_pre4/src/
cmsenv
```

Technically these commands are done in the scripts used but they don't really work so better do it automatically and from a fresh terminal based on Alma9.

**Note:** to use python after the source of cmssw you need to use `python3` or it doesn't work.

Then, the code `/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/combine/make_datacards.py` makes the datacards for combine by only saving the samples that have events so combine doesn't complain. To actually run combine, use `/ceph/sgiappic/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/combine/replace_input_combine.py`.