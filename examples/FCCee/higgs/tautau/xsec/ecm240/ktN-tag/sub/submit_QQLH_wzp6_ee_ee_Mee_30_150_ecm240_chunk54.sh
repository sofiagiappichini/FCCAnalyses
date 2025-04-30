#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_54.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_281.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_486.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_661.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_621.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_146.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_659.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_554.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_314.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_325.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_276.root 

