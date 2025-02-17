#!/bin/bash

source /work/awiedl/FCCAnalyses/setup.sh

cd /work/awiedl/FCCAnalyses/examples/FCCee/higgs/tautau/xsec/ecm365/

fccanalysis run analysis_stage1.py --batch  --output  /ceph/awiedl/FCCee/HiggsCP/ecm365/stage1_280125/p8_ee_WW_ecm365/chunk_80.root --files-list  /ceph/xzuo/FCC_samples_EMD4HEP/Htautau_365GeV/p8_ee_WW_ecm365/events_114994428.root 

