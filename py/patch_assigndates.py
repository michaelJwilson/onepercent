import astropy.io.fits as fits

from astropy.table import Table, join

tiles   = Table(fits.open('../run/survey/tiles/des.fits')[1].data)
dat     = Table(fits.open('../run/survey/assign_dates_surveysim.fits')[1].data)

tiles   = join(tiles, dat, join_type='left', keys='TILEID')

topatch = (tiles['ASSIGNDATE'] == '2020-09-15') & (tiles['COVERED'] == -1) 

tiles['ASSIGNDATE'][topatch] = '9999-99-99'

tiles   = tiles['TILEID', 'ASSIGNDATE']

tiles.pprint()

tiles.write('../run/survey/assign_dates_surveysim.fits', format='fits', overwrite=True)
