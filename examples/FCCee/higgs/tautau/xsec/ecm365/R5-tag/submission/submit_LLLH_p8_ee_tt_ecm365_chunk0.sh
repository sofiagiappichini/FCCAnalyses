#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-tag/LL/

fccanalysis run analysis_stage2_LLLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-tag/stage2_280125/LL/LH/p8_ee_tt_ecm365/chunk_0.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_13.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_10.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_26.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_24.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_tt_ecm365/chunk_1.root 

