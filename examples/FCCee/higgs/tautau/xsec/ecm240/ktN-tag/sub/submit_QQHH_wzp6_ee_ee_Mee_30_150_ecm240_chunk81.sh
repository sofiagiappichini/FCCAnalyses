#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_81.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_759.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_802.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_260.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_130.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_566.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_340.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_529.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_138.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_655.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ee_Mee_30_150_ecm240/chunk_706.root 

