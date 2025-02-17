#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/ktN-tag/NuNu/

fccanalysis run analysis_stage2_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/ktN-tag/stage2_280125/NuNu/LL/p8_ee_ZZ_ecm365/chunk_8.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_81.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_7.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_44.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_53.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_112.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_77.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_83.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_60.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_43.root /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_ZZ_ecm365/chunk_20.root 

