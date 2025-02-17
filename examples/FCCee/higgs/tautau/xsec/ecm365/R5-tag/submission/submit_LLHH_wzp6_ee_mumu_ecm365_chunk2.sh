#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-tag/LL/

fccanalysis run analysis_stage2_LLHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-tag/stage2_280125/LL/HH/wzp6_ee_mumu_ecm365/chunk_2.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_50.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_37.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_32.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_49.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_29.root 

