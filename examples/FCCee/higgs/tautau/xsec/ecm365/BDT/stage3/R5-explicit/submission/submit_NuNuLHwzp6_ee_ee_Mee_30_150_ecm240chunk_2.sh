#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_2.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_65.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_36.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_61.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_71.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_50.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_37.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_32.root 

