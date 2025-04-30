#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/p8_ee_Zqq_ecm240/chunk_67.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_832.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_771.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_319.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_795.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_583.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_353.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_494.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_64.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_193.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_364.root 

