#cmod +x merge_root.sh
#./merge_root.sh

#!/bin/bash
#First run this line and check you have 100 files per bkg
#for i in "NJL_BG_DYJetsTocc" "NJL_BG_tt123j_noMadspin" "NJL_BG_WJets" "NJL_BG_st_tWcc" "NJL_BG_WWToLNuQQ" "NJL_BG_WZToLNuQQ" "NJL_BG_ZZToAcc"; do ls $i*.root | wc -l; done

#then merge the files for each background
for i in "p8_ee_bbH_Htautau_CPmix_0" "p8_ee_bbH_Htautau_CPmix_1" "p8_ee_bbH_Htautau_CPmix_2";
do 
hadd -a p8_ee_bbH_Htautau_CPmix.root "$i".root 
# rm "$i".root
done