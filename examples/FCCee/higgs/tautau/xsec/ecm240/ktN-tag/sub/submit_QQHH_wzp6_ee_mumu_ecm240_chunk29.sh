#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_ee_mumu_ecm240/chunk_29.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_320.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_87.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_440.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_510.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_157.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_391.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_67.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_474.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_385.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_275.root 

