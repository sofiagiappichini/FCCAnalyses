#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/LL/

fccanalysis run analysis_stage2_LLLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/LL/LL/wzp6_ee_tautau_ecm365/chunk_12.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_19.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_105.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_25.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_70.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_96.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_124.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_74.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_109.root 

