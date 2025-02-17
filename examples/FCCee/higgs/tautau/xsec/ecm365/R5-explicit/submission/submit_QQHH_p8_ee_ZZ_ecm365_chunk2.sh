#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/R5-explicit/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/R5-explicit/stage2_280125/QQ/HH/p8_ee_ZZ_ecm365/chunk_2.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_24.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_40.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_93.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_39.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_35.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_65.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_36.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_104.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_61.root 

