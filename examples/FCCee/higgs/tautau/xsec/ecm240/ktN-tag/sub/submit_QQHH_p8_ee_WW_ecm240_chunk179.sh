#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/p8_ee_WW_ecm240/chunk_179.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_465.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2883.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2563.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1862.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3587.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2585.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_415.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1107.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2986.root 

