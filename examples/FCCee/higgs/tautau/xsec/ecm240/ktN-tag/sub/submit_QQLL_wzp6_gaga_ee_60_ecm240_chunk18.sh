#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/wzp6_gaga_ee_60_ecm240/chunk_18.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_222.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_62.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_46.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_21.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_192.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_195.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_143.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_69.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gaga_ee_60_ecm240/chunk_169.root 

