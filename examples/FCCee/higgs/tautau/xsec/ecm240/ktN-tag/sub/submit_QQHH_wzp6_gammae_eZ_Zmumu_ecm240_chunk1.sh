#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQHH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/HH/wzp6_gammae_eZ_Zmumu_ecm240/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_40.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_39.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_35.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_36.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_50.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_37.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_5.root 

