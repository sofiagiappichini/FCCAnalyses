#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/wzp6_ee_tautau_ecm240/chunk_43.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_416.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_458.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_307.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_62.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_46.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_259.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_21.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_496.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_192.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_318.root 

