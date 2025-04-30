#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_ee_mumu_ecm240/chunk_22.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_311.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_122.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_399.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_187.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_95.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_374.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_185.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_160.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_142.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_479.root 

