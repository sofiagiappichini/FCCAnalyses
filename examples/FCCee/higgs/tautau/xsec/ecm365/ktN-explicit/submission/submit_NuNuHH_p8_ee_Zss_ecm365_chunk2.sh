#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit/NuNu/

fccanalysis run analysis_stage2_NuNuHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-explicit/stage2_280125/NuNu/HH/p8_ee_Zss_ecm365/chunk_2.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_32.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_49.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_29.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_57.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zss_ecm365/chunk_3.root 

