import os
import shutil

DIR_PLOTS = '/eos/user/s/sgiappic/www/paper/august/' 

CUTS = [
    "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35_DF",
    "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35_10gev_DF",
    "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35_20gev_DF",
    "selReco_gen_notracks_2eh_M80_10MET_0cos_45ME_e35_30gev_DF",
 ] 

# Loop through each replacement word
for cut in CUTS:
    dir_name =  DIR_PLOTS+cut+"/"
    os.system("cp /eos/user/s/sgiappic/www/index.php {}".format(dir_name))
    print("{} processed".format(dir_name))