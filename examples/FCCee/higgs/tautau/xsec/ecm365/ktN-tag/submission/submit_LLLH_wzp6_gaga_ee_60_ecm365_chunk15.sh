#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/LL/

fccanalysis run analysis_stage2_LLLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/LL/LH/wzp6_gaga_ee_60_ecm365/chunk_15.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_83.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_60.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_181.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_43.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_115.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_183.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_20.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_75.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_28.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_86.root 

