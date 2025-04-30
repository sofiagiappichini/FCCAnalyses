#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_28.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_823.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_282.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_405.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_463.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_225.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_530.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_470.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_660.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_153.root 

