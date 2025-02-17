#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/QQ/LH/wzp6_ee_tautau_ecm365/chunk_10.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_20.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_75.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_28.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_86.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_41.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_62.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_46.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_21.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_69.root 

