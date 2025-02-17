#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/LL/

fccanalysis run analysis_stage2_LLLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/LL/LH/p8_ee_Zqq_ecm365/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_26.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_24.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_40.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_39.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_35.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_36.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_50.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_37.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_22.root 

