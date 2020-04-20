import fitsio
import desimodel
import numpy as np
import astropy.io.fits as fits

from   astropy.table import Table, unique
from   desisurvey.utils import get_date
from   desimodel.footprint import is_point_in_desi

##
tfiles  = '/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020e-onepercent/run/survey/tiles/des.fits'
tiles   = desimodel.io.load_tiles(tilesfile=tfiles)

# ids   = complete['TILEID']
# isin  = np.isin(tiles['TILEID'], ids)

skies   = fitsio.read('/global/cfs/cdirs/desi/target/catalogs/dr8/0.32.0/skies/skies-dr8-0.32.0.fits')

# Cut to observed tiles.                                                                                                                                                                                                       
isin    = is_point_in_desi(tiles, skies['RA'], skies['DEC'])

skies   = skies[isin]

fitsio.write('/global/cscratch1/sd/mjwilson/svdc-spring2020e-onepercent/targets/skies.fits', skies)
