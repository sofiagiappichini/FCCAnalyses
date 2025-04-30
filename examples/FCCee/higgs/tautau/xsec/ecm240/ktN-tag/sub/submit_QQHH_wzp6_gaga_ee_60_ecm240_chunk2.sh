#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_gaga_ee_60_ecm240/chunk_2.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_97.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_31.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_58.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_149.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_38.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_10.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_125.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_79.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_56.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_134.root 

