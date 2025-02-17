#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/NuNu/

fccanalysis run analysis_stage2_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/NuNu/LL/wzp6_ee_mumu_ecm365/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_56.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_26.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_24.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_40.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_39.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_35.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_65.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_36.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_61.root 

