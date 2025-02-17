#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/ktN-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage3_241202/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_3.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_49.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_29.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_68.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_57.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_72.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_3.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_30.root 

