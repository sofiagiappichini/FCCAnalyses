#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_4.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_17.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_42.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_27.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_7.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_44.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_53.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_43.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_20.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_28.root 

