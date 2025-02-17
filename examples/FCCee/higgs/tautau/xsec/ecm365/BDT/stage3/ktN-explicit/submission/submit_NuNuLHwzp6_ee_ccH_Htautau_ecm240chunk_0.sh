#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/ktN-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage3_241202/NuNu/LH/wzp6_ee_ccH_Htautau_ecm240/chunk_0.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ccH_Htautau_ecm240/chunk_0.root 

