#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/LL/

fccanalysis run analysis_stage2_LLHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/LL/HH/wzp6_ee_ccH_Htautau_ecm365/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ccH_Htautau_ecm365/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ccH_Htautau_ecm365/chunk_9.root 

