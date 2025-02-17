#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_6.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_60.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_43.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_20.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_75.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_28.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_41.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_0.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_62.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_46.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_21.root 

