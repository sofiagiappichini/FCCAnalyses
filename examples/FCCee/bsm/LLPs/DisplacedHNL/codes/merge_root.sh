#cmod +x merge_root.sh
#./merge_root.sh

#!/bin/bash
#First run this line and check you have 100 files per bkg
#for i in "NJL_BG_DYJetsTocc" "NJL_BG_tt123j_noMadspin" "NJL_BG_WJets" "NJL_BG_st_tWcc" "NJL_BG_WWToLNuQQ" "NJL_BG_WZToLNuQQ" "NJL_BG_ZZToAcc"; do ls $i*.root | wc -l; done

#then merge the files for each background
for i in "llnunu_1" "llnunu_2" "llnunu_3" "llnunu_4" "llnunu_5" "llnunu_6" "llnunu_7" "llnunu_8" "llnunu_9" "llnunu_10" ;  
do 
hadd -a llnunu.root "$i".root 
# rm "$i".root
done