#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/p8_ee_Zqq_ecm240/chunk_87.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_432.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_446.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_209.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_538.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_489.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_337.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_188.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_359.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_578.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_85.root 

