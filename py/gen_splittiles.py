import os
import desimodel
import fitsio
import numpy                as     np
import pylab                as     pl
import astropy.io.fits      as     fits
import matplotlib.pyplot    as     plt

from   astropy.table        import Table, vstack
from   desimodel.io         import findfile
from   desitarget.geomask   import circles
from   desimodel.focalplane import get_tile_radius_deg


tiles_file   = findfile('footprint/desi-tiles.fits')

print(tiles_file)

tiles        = Table(fits.open(tiles_file)[1].data)
tiles.pprint(max_width=-1)

extra_gray   = Table(tiles[tiles['PASS'] == 8], copy=True)
extra_dark   = Table(tiles[tiles['PASS'] == 9], copy=True)
extra_brt    = Table(tiles[tiles['PASS'] == 8], copy=True)

example_gray = Table(tiles[tiles['PASS'] == 0], copy=True)
example_dark = Table(tiles[tiles['PASS'] == 1], copy=True)
example_brt  = Table(tiles[tiles['PASS'] == 5], copy=True)

extra_gray['PASS']          = 8
extra_gray['PROGRAM']       = example_gray['PROGRAM'][0]
extra_gray['OBSCONDITIONS'] = example_gray['OBSCONDITIONS'][0]

extra_dark['PASS']          = 9
extra_dark['PROGRAM']       = example_dark['PROGRAM'][0]
extra_dark['OBSCONDITIONS'] = example_dark['OBSCONDITIONS'][0]

extra_brt['PASS']           = 10 
extra_brt['PROGRAM']        = example_brt['PROGRAM'][0]
extra_brt['OBSCONDITIONS']  = example_brt['OBSCONDITIONS'][0]

tiles                       = vstack((tiles[tiles['PASS'] < 8], extra_gray, extra_dark, extra_brt))
tiles['TILEID']             = np.arange(len(tiles))

tiles.pprint(max_width=-1)

# In DESI
tiles      = tiles[tiles['IN_DESI'] > 0]

# DES
opone      = (tiles['RA'] > 0.)  & (tiles['RA'] <  15.) & (tiles['DEC'] < 6.)  & (tiles['DEC'] > 1.5)
optwo      = (tiles['RA'] > 100.) & (tiles['RA'] < 120.) & (tiles['DEC'] < 36.) & (tiles['DEC'] > 28.5)

#
tiles      = tiles[opone | optwo]

tiles.sort('TILEID')

# max_width=-1
# tiles.pprint(max_width=-1)

# tiles.write('/global/cscratch1/sd/mjwilson/svdc-spring2020g-onepercent/survey/tiles/onepercent.fits', format='fits', overwrite=True)

opone        = (tiles['RA'] > 0.)  & (tiles['RA'] <  15.) & (tiles['DEC'] < 6.)  & (tiles['DEC'] > 1.5)
optwo        = (tiles['RA'] > 100.) & (tiles['RA'] < 120.) & (tiles['DEC'] < 36.) & (tiles['DEC'] > 28.5)

fig, axes    = plt.subplots(1, 2, figsize=(10, 5))

for i, field in enumerate([opone, optwo]):
  plt.sca(axes[i])

  inpass     = (tiles['PASS'] != -1)
  
  circles(tiles['RA'][field & inpass], tiles['DEC'][field & inpass], s= get_tile_radius_deg() * np.ones_like(tiles['DEC'][field & inpass]), ec='b', facecolor='None', lw=1, alpha=0.1)

pl.show()

