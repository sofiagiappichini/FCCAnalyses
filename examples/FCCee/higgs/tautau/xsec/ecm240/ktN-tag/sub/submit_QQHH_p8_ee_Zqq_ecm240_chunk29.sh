#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/p8_ee_Zqq_ecm240/chunk_29.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_321.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_204.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_749.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_972.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_126.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_716.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_182.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_521.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_Zqq_ecm240/chunk_814.root 

