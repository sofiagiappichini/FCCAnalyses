#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/ktN-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage3_241202/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_5.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_17.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_64.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_42.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_66.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_27.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_8.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_7.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_44.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_53.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_77.root 

