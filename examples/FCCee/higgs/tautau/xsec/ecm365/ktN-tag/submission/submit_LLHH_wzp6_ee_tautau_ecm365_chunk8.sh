#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/LL/

fccanalysis run analysis_stage2_LLHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/LL/HH/wzp6_ee_tautau_ecm365/chunk_8.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_88.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_17.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_64.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_42.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_66.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_27.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_113.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_81.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_7.root 

