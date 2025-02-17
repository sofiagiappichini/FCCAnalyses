#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/LL/

fccanalysis run analysis_stage2_LLLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/LL/LL/wzp6_gaga_ee_60_ecm365/chunk_5.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_71.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_50.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_127.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_90.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_37.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_126.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_182.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_5.root 

