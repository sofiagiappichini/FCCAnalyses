#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-tag/LL/

fccanalysis run analysis_stage2_LLLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-tag/stage2_280125/LL/LH/p8_ee_ZZ_ecm365/chunk_4.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_94.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_29.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_110.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_68.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_57.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_95.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_82.root 

