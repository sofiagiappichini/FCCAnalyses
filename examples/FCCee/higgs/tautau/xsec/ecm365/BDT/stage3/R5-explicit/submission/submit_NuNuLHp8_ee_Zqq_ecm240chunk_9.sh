#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LH/p8_ee_Zqq_ecm240/chunk_9.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_78.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_45.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_9.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_98.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_15.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_19.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_25.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_70.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_96.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_Zqq_ecm240/chunk_74.root 

