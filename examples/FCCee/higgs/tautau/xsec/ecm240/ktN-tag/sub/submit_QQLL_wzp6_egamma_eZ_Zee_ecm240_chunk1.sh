#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/wzp6_egamma_eZ_Zee_ecm240/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_26.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_24.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_40.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_39.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_35.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_36.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_50.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_37.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_22.root 

