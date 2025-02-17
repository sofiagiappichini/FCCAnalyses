#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-explicit/stage2_280125/QQ/LH/wzp6_ee_mumu_ecm365/chunk_6.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_18.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_45.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_9.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_15.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_19.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_25.root 

