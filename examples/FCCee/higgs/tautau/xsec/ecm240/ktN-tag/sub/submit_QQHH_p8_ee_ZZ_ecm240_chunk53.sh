#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/p8_ee_ZZ_ecm240/chunk_53.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_231.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_132.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_161.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_260.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_130.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_340.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_529.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_138.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_213.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_25.root 

