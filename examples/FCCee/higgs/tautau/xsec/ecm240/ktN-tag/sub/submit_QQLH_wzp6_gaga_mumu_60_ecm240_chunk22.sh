#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_gaga_mumu_60_ecm240/chunk_22.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_113.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_189.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_81.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_172.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_7.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_203.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_190.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_44.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_mumu_60_ecm240/chunk_121.root 

