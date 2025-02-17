#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/QQ/HH/wzp6_gaga_tautau_60_ecm365/chunk_9.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_135.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_162.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_82.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_92.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_72.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_200.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_136.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_100.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_116.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_tautau_60_ecm365/chunk_164.root 

