#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LL/wzp6_ee_ssH_HWW_ecm240/chunk_0.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_10.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_3.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_11.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_ee_ssH_HWW_ecm240/chunk_7.root 

