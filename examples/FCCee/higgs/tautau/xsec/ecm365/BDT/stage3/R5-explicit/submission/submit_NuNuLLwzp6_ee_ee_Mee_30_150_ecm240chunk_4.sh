#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_4.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_23.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_11.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_67.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_48.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_33.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_55.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_ee_ee_Mee_30_150_ecm240/chunk_59.root 

