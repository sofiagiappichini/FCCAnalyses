#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_ee_mumu_ecm240/chunk_45.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_345.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_69.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_169.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_432.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_446.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_209.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_489.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_337.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_188.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_359.root 

