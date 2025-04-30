#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_gammae_eZ_Zmumu_ecm240/chunk_2.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_32.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_49.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_29.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_3.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_30.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_23.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_gammae_eZ_Zmumu_ecm240/chunk_11.root 

