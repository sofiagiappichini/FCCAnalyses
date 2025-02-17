#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/LL/

fccanalysis run analysis_stage2_LLLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/LL/LH/wzp6_gaga_ee_60_ecm365/chunk_14.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_44.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_121.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_53.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_128.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_112.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_191.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_201.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_129.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_117.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_gaga_ee_60_ecm365/chunk_77.root 

