#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/QQ/LH/p8_ee_WW_ecm365/chunk_10.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_46.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_21.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_69.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_85.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_114.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_99.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_18.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_78.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_45.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_9.root 

