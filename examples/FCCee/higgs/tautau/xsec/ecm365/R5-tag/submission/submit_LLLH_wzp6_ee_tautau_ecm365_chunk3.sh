#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-tag/LL/

fccanalysis run analysis_stage2_LLLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-tag/stage2_280125/LL/LH/wzp6_ee_tautau_ecm365/chunk_3.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_104.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_61.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_71.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_50.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_127.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_90.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_37.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_126.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_12.root 

