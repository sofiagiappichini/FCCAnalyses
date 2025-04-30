#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_gaga_ee_60_ecm240/chunk_6.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_204.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_126.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_182.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_120.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_32.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_214.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_49.root 

