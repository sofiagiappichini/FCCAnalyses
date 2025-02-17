#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit/LL/

fccanalysis run analysis_stage2_LLLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-explicit/stage2_280125/LL/LL/p8_ee_Zss_ecm365/chunk_0.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_54.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_51.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_34.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_13.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_47.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_31.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_58.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_38.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_10.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_56.root 

