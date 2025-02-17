#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/

fccanalysis run analysis_stage1.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/wzp6_ee_tautauH_Htautau_ecm365/chunk_8.root --files-list  /ceph/xzuo/FCC_samples_EMD4HEP/Htautau_365GeV/wzp6_ee_tautauH_Htautau_ecm365/events_095907086.root 

