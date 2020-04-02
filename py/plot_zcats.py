import glob
import numpy             as np
import pylab             as pl
import astropy.io.fits   as fits
import matplotlib.pyplot as plt

from   astropy.table     import Table, join, vstack


colors    = plt.rcParams['axes.prop_cycle'].by_key()['color']
fig, axes = plt.subplots(1, 3, figsize=(10,15))

mtl       = Table(fits.open('../run/quicksurvey/{}/mtl.fits'.format(9))[1].data)
zcat      = Table(fits.open('../run/quicksurvey/{}/zcat.fits'.format(9))[1].data)

tokeep    = ['BGS_TARGET','MWS_TARGET','SUBPRIORITY','OBSCONDITIONS','PRIORITY_INIT','NUMOBS_INIT','HPXPIXEL','NUMOBS_MORE','PRIORITY','RA', 'DEC', 'TARGETID', 'DESI_TARGET'] 
zcat      = join(zcat, mtl[tokeep], join_type='left', keys='TARGETID')
  
zcat['RA'][zcat['RA'] > 180.] -= 360. 

axes.set_xlim(0., 30.)
axes.set_ylim(0., 7.5)

axes.scatter(zcat['RA'], zcat['DEC'], marker='.', s=.1)
axes.legend(frameon=False)

pl.show()
