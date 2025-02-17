#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/R5-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage3_241202/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_0.root --files-list  /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_34.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_13.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_47.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_31.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_38.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_10.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_26.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_24.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_40.root /ceph/awiedl/FCCee/HiggsCP/R5-explicit/stage2_241202_cut/NuNu/LH/wzp6_ee_mumu_ecm240/chunk_2.root 

