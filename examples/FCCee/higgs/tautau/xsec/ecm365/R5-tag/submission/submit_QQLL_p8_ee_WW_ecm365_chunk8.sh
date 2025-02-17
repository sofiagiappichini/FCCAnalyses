#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-tag/stage2_280125/QQ/LL/p8_ee_WW_ecm365/chunk_8.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_113.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_81.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_7.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_44.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_53.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_112.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_117.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_77.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_83.root 

