#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/p8_ee_ZZ_ecm240/chunk_32.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_354.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_313.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_532.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_236.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_166.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_459.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_441.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_403.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_84.root 

