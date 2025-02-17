#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/ktN-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage3_241202/NuNu/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_0.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_3.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_egamma_eZ_Zmumu_ecm240/chunk_0.root 

