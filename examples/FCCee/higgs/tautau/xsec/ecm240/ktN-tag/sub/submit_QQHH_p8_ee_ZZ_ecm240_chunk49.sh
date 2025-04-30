#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/p8_ee_ZZ_ecm240/chunk_49.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_194.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_99.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_336.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_18.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_78.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_478.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_303.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_45.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_9.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_118.root 

