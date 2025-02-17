#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/QQ/HH/p8_ee_Zcc_ecm365/chunk_4.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_17.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_42.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_27.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_7.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_44.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_53.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_43.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_20.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zcc_ecm365/chunk_28.root 

