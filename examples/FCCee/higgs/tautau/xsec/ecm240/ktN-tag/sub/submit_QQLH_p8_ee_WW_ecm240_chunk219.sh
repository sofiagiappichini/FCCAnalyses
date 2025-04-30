#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/p8_ee_WW_ecm240/chunk_219.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_821.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_931.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3325.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2447.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3556.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_741.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_293.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2989.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2874.root 

