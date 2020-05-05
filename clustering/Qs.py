import sys
import pickle
import numpy                       as      np
import fitsio
import astropy.units               as      u
import pylab                       as      pl

from   scipy.special               import  eval_legendre
from   astropy.cosmology           import  Planck13
from   astropy.cosmology           import  FlatLambdaCDM
from   astropy                     import  constants as const
from   Corrfunc.mocks.DDrppi_mocks import  DDrppi_mocks
from   Corrfunc.mocks.DDsmu_mocks  import  DDsmu_mocks
from   astropy.table               import  Table, join
from   desitarget.targets          import  desi_mask, bgs_mask, mws_mask


weighted   = True

truth      = Table.read('../run/targets/truth-dark.fits')
targets    = Table.read('../run/targets/targets-dark.fits')

# Force native endian-ness.
targets    = Table(join(targets, truth, join_type='left', keys='TARGETID').as_array())
# targets.write('../run/targets/targets-truth-dark.fits', format='fits', overwrite=True)

lrgs       = (targets['DESI_TARGET'] & desi_mask["LRG"]) != 0
lrgs       = targets[lrgs]

# zs       = lrgs['TRUEZ']

rand       = Table(Table.read('../run/catalogs/dark/LRG_oneper_clus.ran.fits').as_array())

if not weighted:
  rand['WEIGHT'] = np.ones_like(rand['Z'])
  
zs         = rand['Z']
  
np.random.seed(seed=314)

# zs       = np.random.choice(zs, replace=True, size=len(rand)).astype(np.float64)

# rand['Z']  = zs

# rand.write('../run/randoms/dark/randoms_oneper_darktime_jmtl_truez.fits', format='fits', overwrite=True)

# Number of threads to use
nthreads  = 32

# Specify cosmology (1->LasDamas, 2->Planck)
cosmology = 1

# Create the bins array
rmin      = 0.1
rmax      = 1.e3
nbins     = 50
rbins     = np.logspace(np.log(rmin), np.log(rmax), nbins + 1, base=np.exp(1))

# Specify the max. of the cosine of the angle to the LOS
# for DD(s, mu)
mu_max    = 1.0

# Specify the number of linear bins in `mu`
nmu_bins  = 100

dmu       = mu_max / nmu_bins

# Specify that an autocorrelation is wanted
autocorr    = 1

sampling    = 25

ras         = np.array(rand['RA'])[::sampling]
decs        = np.array(rand['DEC'])[::sampling]
ws          = np.array(rand['WEIGHT'])[::sampling]
zs          = zs[::sampling]
czs         = const.c.to('km/s').value * zs

# Mpch/h
czs         = Planck13.comoving_distance(zs).value * Planck13.h

# https://corrfunc.readthedocs.io/en/master/modules/weighted_correlations.html#weighted-correlations
result      = DDsmu_mocks(autocorr, cosmology, nthreads, mu_max, nmu_bins, rbins, ras, decs, czs, is_comoving_dist=True, weights1=ws, output_savg=True, weight_type='pair_product')

with open(r'QS_weighted_{}_corrfunc.pkl'.format(np.int(weighted)), 'wb') as out:
    pickle.dump(result, out)

# ('smin', 'smax', 'savg', 'mumax', 'npairs', 'weightavg')
ss          = (result['smin'] + result['smax']) / 2.
mus         = result['mumax'] - dmu / 2.
ns          = result['npairs']

#    if not weighted:
#        assert  np.allclose(result['weightavg'], result['npairs'])

us          = np.unique(ss)

result      = [us.tolist()]

for ell in [0, 2, 4, 6]:
  Qs        = []

  for u in us:
    isin    = (ss == u)
    
    _       = mus[isin]
    
    indx    = np.argsort(_)
    
    assert  np.all(np.diff(mus[isin][indx]) > 0.0)
    
    Qs.append(0.5 * (2. * ell + 1) * np.trapz(ns[isin][indx] * eval_legendre(ell, mus[isin][indx]) / u**3., mus[isin][indx]))

  result.append(Qs)
    
  Qs        = np.array(Qs)
  Qs        = np.abs(Qs)
  
  # pl.semilogx(us, Qs, label=r'$\ell={}$'.format(ell), marker='^')

# pl.xlim(0.1, 500.)
# pl.ylim(0.0,  1.2)

# pl.legend()
# pl.show()

#
result = np.array(result).T

np.savetxt('Qs_onepercent_weighted_{}.txt'.format(np.int(weighted)), result)

print('\n\nDone.\n\n')
