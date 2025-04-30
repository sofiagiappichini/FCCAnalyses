#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/p8_ee_WW_ecm240/chunk_274.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3271.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_954.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2183.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1540.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3163.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3046.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_360.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2057.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1802.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2991.root 

