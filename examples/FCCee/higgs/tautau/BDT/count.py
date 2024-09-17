import uproot
import os
process = [ 'wzp6_ee_eeH_Htautau_ecm240/chunk_0.root',
            'wzp6_ee_mumuH_Htautau_ecm240/chunk_0.root',
            'wzp6_ee_tautauH_Htautau_ecm240/chunk_0.root',
            'wzp6_ee_nunuH_Htautau_ecm240/chunk_1.root',
            'wzp6_ee_bbH_Htautau_ecm240/chunk_0.root',
            'wzp6_ee_ccH_Htautau_ecm240/chunk_0.root',
            'wzp6_ee_ssH_Htautau_ecm240/chunk_0.root',
            'wzp6_ee_qqH_Htautau_ecm240/chunk_0.root']


path = '/ceph/awiedl/FCCee/HiggsCP/stage2/NuNu/LL/'
for i in process:
    file = uproot.open(path+i)
    if file.keys()==['eventsProcessed;1']:
        print('fehlt')
        continue
    else:
        for events in uproot.iterate(path+i+':events',expressions='n_FSGenElectron',library='pd'):
            print(i)
            print(len(events))
