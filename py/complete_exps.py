import pylab                as     pl
import numpy                as     np
import astropy.io.fits      as     fits
import matplotlib.pyplot    as     plt

from   astropy.table        import Table, join
from   desisurvey.utils     import get_date
from   desitarget.geomask   import circles
from   desimodel.focalplane import get_tile_radius_deg


tiles        = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc-spring2020g-onepercent/survey/tiles/onepercent.fits')[1].data)
dat          = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc-spring2020g-onepercent/survey/exposures_surveysim_fix.fits')[1].data)

tiles        = tiles[np.isin(tiles['TILEID'], dat['TILEID'])]

complete     = dat[dat['SNR2FRAC'] >= 1.0]
complete     = join(complete, tiles['RA', 'DEC', 'PROGRAM', 'PASS', 'TILEID'], keys='TILEID', join_type='left')

assert  len(np.unique(complete['TILEID'])) == len(complete['TILEID'])

complete.pprint(max_width=-1, max_lines=-1)

complete.write('/global/cscratch1/sd/mjwilson/svdc-spring2020g-onepercent/survey/complete_exposures_surveysim_fix.fits', format='fits', overwrite=True)

exit(0)

tiles        = complete

opone        = (tiles['RA'] > 0.)  & (tiles['RA'] <  15.) & (tiles['DEC'] < 6.)  & (tiles['DEC'] > 1.5)
optwo        = (tiles['RA'] > 100.) & (tiles['RA'] < 120.) & (tiles['DEC'] < 36.) & (tiles['DEC'] > 28.5)

fig, axes    = plt.subplots(1, 2, figsize=(10, 5))

for i, field in enumerate([opone, optwo]):
  plt.sca(axes[i])

  circles(tiles['RA'][field], tiles['DEC'][field], s= get_tile_radius_deg() * np.ones_like(tiles['DEC'][field]), ec='b', facecolor='None', lw=1, alpha=0.1)

pl.show()
