#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/NuNu/

fccanalysis run analysis_stage2_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/NuNu/LH/wzp6_ee_tautau_ecm365/chunk_7.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_111.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_87.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_67.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_48.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_33.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_84.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_55.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautau_ecm365/chunk_59.root 

