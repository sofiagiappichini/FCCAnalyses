#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LH/p8_ee_Zqq_ecm240/chunk_3.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_22.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_12.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_5.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_32.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_49.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_14.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_52.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_94.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_29.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_68.root 

