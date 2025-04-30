#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_ee_qqH_Htautau_ecm240/chunk_0.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_qqH_Htautau_ecm240/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_qqH_Htautau_ecm240/chunk_0.root 

