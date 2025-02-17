#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit/NuNu/

fccanalysis run analysis_stage2_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-explicit/stage2_280125/NuNu/LH/wzp6_ee_ssH_HZZ_ecm365/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HZZ_ecm365/chunk_9.root 

