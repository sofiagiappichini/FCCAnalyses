#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_3.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_30.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_23.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_11.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_48.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_33.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_55.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_59.root 

