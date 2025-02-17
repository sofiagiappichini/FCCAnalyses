#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/LL/

fccanalysis run analysis_stage2_LLLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/LL/LL/wzp6_ee_ee_Mee_30_150_ecm365/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_3.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_23.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_11.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_17.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_27.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_ee_Mee_30_150_ecm365/chunk_8.root 

