#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/ktN-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage3_241202/NuNu/LH/p8_ee_ZZ_ecm240/chunk_4.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_41.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_46.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_21.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_18.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_45.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_9.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_15.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_19.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_ZZ_ecm240/chunk_25.root 

