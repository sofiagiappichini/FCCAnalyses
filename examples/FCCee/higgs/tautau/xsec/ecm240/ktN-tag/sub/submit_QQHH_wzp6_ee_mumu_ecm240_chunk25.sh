#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_ee_mumu_ecm240/chunk_25.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_116.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_338.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_164.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_107.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_378.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_289.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_3.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_154.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_396.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_mumu_ecm240/chunk_30.root 

