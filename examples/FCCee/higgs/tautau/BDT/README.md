# Instruction for usage of BDT 

- [Instruction for usage of BDT](#instruction-for-usage-of-bdt)
  - [Setup](#setup)
  - [BDT training](#bdt-training)
  - [BDT use](#bdt-use)

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

The training is handeled by the script `train_bdt_qqhh.py`. Lists of variables, signal and background processes are defined in the beginning. The variables used for training are exactly the same ones required for later application. It takes stage2 (or alternatevely stage1) files as input.

A weight column is added in the DataFrames for all processes to be later used as weight of events in the BDT fit, according to corss section, luminosity and raw number of events.

## BDT use

We apply the trained BDT to stage2 by plugging it in as in [this example](https://github.com/zuoxunwu/FCCAnalyses/blob/3d872a8bd6098bb8935fa41c0202b6a7886b06d7/examples/FCCee/flavour/BuBc2TauNu/analysis_stage2.py#L104-L111). The initialization of the BDT requires you to specify the exact number of variables used for trining that will also have to be passed to the function in the code. The BDT output is a vector of float so you need to take the first element