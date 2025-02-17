#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-explicit/stage2_280125/QQ/LL/p8_ee_WW_ecm365/chunk_11.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_98.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_15.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_19.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_105.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_25.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_70.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_96.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_74.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_109.root 

