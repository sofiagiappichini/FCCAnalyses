#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-tag/NuNu/

fccanalysis run analysis_stage2_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-tag/stage2_280125/NuNu/LL/wzp6_gaga_tautau_60_ecm365/chunk_12.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_166.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_84.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_179.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_55.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_59.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_146.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_88.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_17.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_198.root 

