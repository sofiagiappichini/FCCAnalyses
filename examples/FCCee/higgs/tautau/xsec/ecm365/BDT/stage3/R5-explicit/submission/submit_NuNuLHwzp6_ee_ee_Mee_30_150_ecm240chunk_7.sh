#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_7.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_69.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_18.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_78.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_45.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_9.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_15.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_19.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_25.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_70.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_ee_Mee_30_150_ecm240/chunk_74.root 

