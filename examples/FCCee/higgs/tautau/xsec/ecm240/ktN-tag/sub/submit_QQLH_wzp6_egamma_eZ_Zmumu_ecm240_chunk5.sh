#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm240/ktN-tag/QQ/

fccanalysis run analysis_stage2_QQLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm240/ktN-tag/stage2/QQ/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_5.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_41.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_46.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_21.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_18.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_45.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_9.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_15.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_19.root /ceph/awiedl/FCCee/HiggsCP/ecm240/stage1_241202/wzp6_egamma_eZ_Zmumu_ecm240/chunk_25.root 

