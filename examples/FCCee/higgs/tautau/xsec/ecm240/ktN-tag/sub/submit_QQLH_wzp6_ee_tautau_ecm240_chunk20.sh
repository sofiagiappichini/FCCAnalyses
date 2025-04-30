#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_ee_tautau_ecm240/chunk_20.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_145.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_451.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_228.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_344.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_262.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_502.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_514.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_296.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_467.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_57.root 

