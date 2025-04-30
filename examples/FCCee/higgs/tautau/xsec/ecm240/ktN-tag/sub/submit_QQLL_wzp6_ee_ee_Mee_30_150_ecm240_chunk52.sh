#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_52.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_640.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_166.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_459.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_719.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_441.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_403.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_852.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_84.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_834.root 

