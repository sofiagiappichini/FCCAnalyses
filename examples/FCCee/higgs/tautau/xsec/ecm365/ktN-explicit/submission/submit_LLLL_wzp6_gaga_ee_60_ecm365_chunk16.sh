#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit/LL/

fccanalysis run analysis_stage2_LLLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-explicit/stage2_280125/LL/LL/wzp6_gaga_ee_60_ecm365/chunk_16.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_158.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_41.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_196.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_62.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_46.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_21.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_192.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_195.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_143.root 

