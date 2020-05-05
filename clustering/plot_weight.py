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


truth      = Table.read('../run/targets/truth-dark.fits')
targets    = Table.read('../run/targets/targets-dark.fits')

# Force native endian-ness.
targets    = Table(join(targets, truth, join_type='left', keys='TARGETID').as_array())
# targets.write('../run/targets/targets-truth-dark.fits', format='fits', overwrite=True)

lrgs       = (targets['DESI_TARGET'] & desi_mask["LRG"]) != 0
lrgs       = targets[lrgs]

# zs       = lrgs['TRUEZ']

rand       = Table(Table.read('../run/catalogs/dark/LRG_oneper_clus.ran.fits').as_array())
rand       = rand[::100]

rand['RA'][rand['RA'] > 180.] -= 360.
  
zs         = rand['Z']

pl.scatter(rand['RA'], rand['DEC'], c=rand['WEIGHT'], cmap='jet', vmin=0.0, vmax=1.0, s=0.2)
pl.colorbar(label='Random weight')

pl.xlabel('Right ascension [deg.]')
pl.ylabel('Declination [deg.]')

pl.xlim(22.5, -2.5)

pl.show()

print('\n\nDone.\n\n')
