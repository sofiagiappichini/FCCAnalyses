#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_ee_tautau_ecm240/chunk_16.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_282.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_405.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_463.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_225.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_470.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_153.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_497.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_tautau_ecm240/chunk_475.root 

