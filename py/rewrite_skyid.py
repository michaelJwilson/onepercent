import numpy              as     np
import healpy             as     hp

from   astropy.table      import Table
from   desitarget.targets import encode_targetid
from   desitarget.geomask import is_in_hp


# objid    = np.arange(nobj + nsky)

nside      = 64

dat        = Table.read('../run/targets/skies.fits')
dec        = dat['DEC']
ra         = dat['RA']

bid        = np.unique(dat['TARGETID'])

# ADM check whether ra, dec are in the pixel list
theta, phi = np.radians(90-dec), np.radians(ra)
pixnums    = hp.ang2pix(nside, theta, phi, nest=True)

dat['HEALPIXEL'] = pixnums

upix       = np.unique(pixnums)

for u in upix:
  inpix    = dat['HEALPIXEL'] == u 

  nsky     = np.count_nonzero(inpix) 

  objid    = np.arange(nsky)
  
  dat['TARGETID'][inpix] = encode_targetid(objid=objid, brickid=u, mock=1, sky=1)

# Check on copy. 
fid        = np.unique(dat['TARGETID'])

fixed      = np.count_nonzero(fid != bid)

assert  fixed == len(dat)

print(dat)
  
dat.write('../run/targets/skies_fixedid.fits', format='fits', overwrite=True)
