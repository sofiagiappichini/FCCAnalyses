#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/wzp6_ee_tautau_ecm240/chunk_39.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_509.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_297.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_506.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_429.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_271.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_257.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_181.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_43.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_301.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_342.root 

