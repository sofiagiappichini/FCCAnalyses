#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LL/p8_ee_Zqq_ecm240/chunk_5.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_80.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_89.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_87.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_67.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_48.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_33.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_84.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/p8_ee_Zqq_ecm240/chunk_16.root 

