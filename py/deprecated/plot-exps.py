import astropy.io.fits as fits
import numpy           as np
import pylab           as pl

from astropy.table import Table, join
from astropy.time  import Time


print('\n\nWelcome.\n\n')

dat        = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc2019c2/survey/exposures_surveysim.fits')[1].data)

##  Calculate ISO time. 
times      = dat['MJD']
t          = Time(times, format='mjd', scale='utc')
dat['ISO'] = t.iso


nights       = np.array([x.split(' ')[0].replace('-', '') for x in dat['ISO'] if x != '--'])
dat['NIGHT'] = nights

##  Join with tiles file. 
tiles      = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc2019c2/survey/tiles/schlafly/opall.fits')[1].data)

dat        = join(dat, tiles, keys=['TILEID'], join_type='outer', table_names=['', '~'], uniq_col_name='{col_name}{table_name}')
dat.sort('ISO')
 
dat.remove_column('AIRMASS~')
dat.remove_column('BRIGHTRA')
dat.remove_column('BRIGHTDEC')
dat.remove_column('BRIGHTVTMAG')

dat.write('/global/cscratch1/sd/mjwilson/svdc2019c2/survey/exposures_surveysim_vadd.fits', format='fits', overwrite=True)

##  Write dates file.
written = set()
dates   = np.array([x.split(' ')[0] for x in dat['ISO'] if x != '--'])
dates   = [x.replace('-', '') for x in dates if x not in written and (written.add(x) or True)]

np.savetxt('nights.txt', dates, fmt='%s')
'''
dates = dates.reshape(1, len(dates))
dates = Table(dates.T, names=['ISO'])

dates.write('nights.fits', format='fits', overwrite=True)
'''
print(dat)

for _pass in np.arange(0, 11, 1):
  pl.clf()
  
  pl.scatter(tiles[tiles['PASS'] == _pass]['RA'], tiles[tiles['PASS'] == _pass]['DEC'], marker='.', c='k', alpha=0.3, rasterized=True)
  pl.scatter(dat[dat['PASS'] == _pass]['RA'], dat[dat['PASS'] == _pass]['DEC'], marker='.', c=dat[dat['PASS'] == _pass]['EXPTIME'], rasterized=True)
  pl.colorbar(label='EXPTIME [s]')
  pl.title('Pass: {}'.format(_pass))
  pl.savefig('plots/exposures/pass_{}.pdf'.format(_pass))
  
print('\n\nDone.\n\n')
