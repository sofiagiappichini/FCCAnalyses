#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-explicit/stage2_280125/QQ/HH/p8_ee_Zqq_ecm365/chunk_3.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_30.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_23.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_11.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_48.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_33.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_55.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zqq_ecm365/chunk_59.root 

