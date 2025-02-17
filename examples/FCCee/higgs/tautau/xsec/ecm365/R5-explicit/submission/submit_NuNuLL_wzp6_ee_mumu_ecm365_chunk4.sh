#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/NuNu/

fccanalysis run analysis_stage2_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/NuNu/LL/wzp6_ee_mumu_ecm365/chunk_4.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_55.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_59.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_17.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_64.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_42.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_27.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_7.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_mumu_ecm365/chunk_44.root 

