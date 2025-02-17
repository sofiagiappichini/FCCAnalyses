#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-tag/NuNu/

fccanalysis run analysis_stage2_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-tag/stage2_280125/NuNu/LL/wzp6_ee_ssH_HWW_ecm365/chunk_0.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_3.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_7.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ssH_HWW_ecm365/chunk_9.root 

