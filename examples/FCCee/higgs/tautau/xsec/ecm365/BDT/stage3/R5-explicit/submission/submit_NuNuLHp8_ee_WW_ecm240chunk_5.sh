#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LH/p8_ee_WW_ecm240/chunk_5.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_219.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_299.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_184.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_40.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_174.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_93.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_176.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_2.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_39.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_163.root 

