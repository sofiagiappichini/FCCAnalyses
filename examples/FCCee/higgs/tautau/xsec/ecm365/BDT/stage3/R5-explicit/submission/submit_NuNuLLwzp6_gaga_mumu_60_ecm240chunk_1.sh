#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLL.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_1.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_1.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_3.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_23.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_11.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_4.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_6.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_16.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_17.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_27.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LL/wzp6_gaga_mumu_60_ecm240/chunk_8.root 

