#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_egamma_eZ_Zee_ecm240/chunk_2.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_32.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_49.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_29.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_57.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zee_ecm240/chunk_3.root 

