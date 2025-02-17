#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-explicit/LL/

fccanalysis run analysis_stage2_LLLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-explicit/stage2_280125/LL/LH/wzp6_ee_numunumuH_HZZ_ecm365/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_numunumuH_HZZ_ecm365/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_numunumuH_HZZ_ecm365/chunk_9.root 

