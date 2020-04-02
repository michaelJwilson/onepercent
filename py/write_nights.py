import fitsio
import numpy           as np
import astropy.io.fits as fits

from   astropy.table   import Table


nights    = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc-spring2020b-onepercent/survey/assign_dates_surveysim.fits')[1].data)
nights, _ = np.unique(nights['ASSIGNDATE'], return_counts=True)

np.savetxt('../nights.txt', nights, fmt='%s')
