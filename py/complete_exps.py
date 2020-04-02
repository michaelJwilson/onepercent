import pylab                as     pl
import numpy                as     np
import astropy.io.fits      as     fits
import matplotlib.pyplot    as     plt

from   astropy.table        import Table, join
from   desisurvey.utils     import get_date
from   desitarget.geomask   import circles
from   desimodel.focalplane import get_tile_radius_deg


tiles        = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc-spring2020b-onepercent/survey/tiles/des.fits')[1].data)
dat          = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc-spring2020b-onepercent/survey/exposures_surveysim_fix.fits')[1].data)

complete     = dat[dat['SNR2FRAC'] >= 1.0]
complete     = join(complete, tiles['RA', 'DEC', 'PROGRAM', 'PASS', 'TILEID'], keys='TILEID', join_type='left')
complete.pprint(max_width=-1, max_lines=-1)

exit(0)

complete     = tiles[np.isin(tiles['TILEID'],      dat['TILEID'])]

s            = get_tile_radius_deg() * np.ones_like(complete['DEC'])

fig, axes    = plt.subplots(5, 1, figsize=(10, 30))

for i, c in enumerate(['k', 'b', 'g', 'r', 'gold']):
  inpass     = complete['PASS'] == i

  plt.sca(axes[i])
  
  circles(complete['RA'][inpass], complete['DEC'][inpass], s=s[inpass], c=c, alpha=0.2)

  axes[i].set_ylim(-5., 7.5)
  
pl.show()

