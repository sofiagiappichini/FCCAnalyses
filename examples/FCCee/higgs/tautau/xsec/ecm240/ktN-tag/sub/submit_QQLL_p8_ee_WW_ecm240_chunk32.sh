#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/p8_ee_WW_ecm240/chunk_32.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3208.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_3454.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1897.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_819.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1939.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2479.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1639.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1150.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_1779.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/p8_ee_WW_ecm240/chunk_2051.root 

