# Calculate number of expected heavy neutrinos 
# assuming a total of 6e12 produced Z bosons, based on formulas
# by M. Drewes
def nobs(mn,U2):
  mz=91.18
  NZ=6e12
  cprod=2 # for two neutrinos
  BR=1/15. # Z BR into one neutrino species
  pn=(mz/2)*(1-(mn/mz)**2)
  phsp=((2*pn/mz)**2)*(1+((mn/mz)**2)/2)
  NHN=2*U2*cprod*NZ*BR*phsp 
  return NHN

def n_scale(sigma):
    return sigma*205e6 #in pb

def n_scale_eff(sigma):
    return sigma*137.5e6 #in pb


print(f"HNL mass = 40, u^2 = 1.33e-7, cross-section(MG) = 0.000179 pb")
print(f"Drewes formula:{nobs(40,1.33e-7)}")
print(f"Lumi scale: {n_scale(0.000179)}")
print(f"ratio with formula: {nobs(40,1.33e-7)/ n_scale(0.000179)}")
print(f"With eff. lumi: {n_scale_eff(0.000179)}")
print(f"ratio with formula: {nobs(40,1.33e-7)/ n_scale_eff(0.000179)}")
print(f"ratio with eff. lumi: {n_scale(0.000179)/ n_scale_eff(0.000179)}\n\n")


print(f"HNL mass = 70, u^2 = 2.86e-9, cross-section(MG) = 1.2319764975593676e-06 pb")
print(f"Drewes formula:{nobs(70,2.86e-9)}")
print(f"Lumi scale: {n_scale(1.2319764975593676e-06)}")
print(f"ratio with formula: {nobs(70,2.86e-9)/ n_scale(1.2319764975593676e-06)}")
print(f"With eff. lumi: {n_scale_eff(1.2319764975593676e-06)}")
print(f"ratio with formula: {nobs(70,2.86e-9)/ n_scale_eff(1.2319764975593676e-06)}")
print(f"ratio with eff. lumi: {n_scale(1.2319764975593676e-06)/ n_scale_eff(1.2319764975593676e-06)}\n\n")

print(f"ONE HNL mass = 40, u^2 = 1, cross-section(MG) = 5.69e3 pb")
#factor 1/2 for cprod
print(f"Drewes formula:{nobs(40,1)/2}")
print(f"Lumi scale: {n_scale(5.69e3)}")
print(f"ratio with formula: {nobs(40,1)/ (2*n_scale(5.69e3))}")
print(f"With eff. lumi: {n_scale_eff(5.69e3)}")
print(f"ratio with formula: {nobs(40,1)/ (2*n_scale_eff(5.69e3))}")
print(f"ratio with eff. lumi: {n_scale(5.69e3)/ n_scale_eff(5.69e3)}")