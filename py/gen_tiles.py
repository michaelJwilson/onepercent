import os
import desimodel
import fitsio
import astropy.io.fits as fits

from   astropy.table   import Table
from   desimodel.io    import findfile


tiles_file = findfile('footprint/desi-tiles.fits')

print(tiles_file)

tiles      = Table(fits.open(tiles_file)[1].data)

print(tiles)

# In DESI
tiles      = tiles[tiles['IN_DESI'] > 0]

# NGC
ngc        = (tiles['RA'] > 100.) & (tiles['RA'] < 275.)

# SGC.
tiles      = tiles[~ngc]

# DARK
tiles      = tiles[(tiles['PROGRAM'] == 'DARK') | (tiles['PROGRAM'] == 'GREY') | (tiles['PROGRAM'] == 'GRAY')]

# dec cut.
tiles      = tiles[(tiles['DEC'] > 15.0) & (tiles['DEC'] < 25.0)] 

tiles.sort('TILEID')

# max_width=-1
tiles.pprint(max_width=-1)

##  tiles.write('/global/cscratch1/sd/mjwilson/svdc-spring2020a-onepercent/survey/tiles/test.fits', format='fits', overwrite=True)
