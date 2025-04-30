#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/p8_ee_ZZ_ecm240/chunk_40.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_266.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_220.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_408.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_77.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_377.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_83.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_356.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_352.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_445.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_523.root 

