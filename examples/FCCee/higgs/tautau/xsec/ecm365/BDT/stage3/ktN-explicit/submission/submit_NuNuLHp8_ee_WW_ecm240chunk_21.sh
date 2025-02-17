#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/BDT/stage3/ktN-explicit/

fccanalysis run analysis_stage3_NuNuLH.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage3_241202/NuNu/LH/p8_ee_WW_ecm240/chunk_21.root --files-list  /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_117.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_266.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_220.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_77.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_83.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_60.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_297.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_271.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_257.root /ceph/awiedl/FCCee/HiggsCP/ktN-explicit/stage2_241202_cut/NuNu/LH/p8_ee_WW_ecm240/chunk_181.root 

