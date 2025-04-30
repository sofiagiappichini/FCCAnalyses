#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_ee_mumu_ecm240/chunk_14.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_321.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_204.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_126.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_182.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_521.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_295.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_481.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_457.root 

