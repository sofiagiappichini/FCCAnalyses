#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/QQ/HH/p8_ee_Zbb_ecm365/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_26.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_24.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_40.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_39.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_35.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_36.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_50.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_37.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_Zbb_ecm365/chunk_22.root 

