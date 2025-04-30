#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/p8_ee_ZZ_ecm240/chunk_44.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_270.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_86.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_382.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_158.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_347.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_41.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_558.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_196.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_272.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_ZZ_ecm240/chunk_437.root 

