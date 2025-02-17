#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-tag/stage2_280125/QQ/LH/wzp6_gaga_tautau_60_ecm365/chunk_20.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_138.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_25.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_70.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_96.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_124.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_202.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_74.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_109.root 

