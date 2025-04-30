#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/p8_ee_WW_ecm240/chunk_218.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2187.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_570.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_990.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3393.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3002.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2718.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2806.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3093.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1730.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3396.root 

