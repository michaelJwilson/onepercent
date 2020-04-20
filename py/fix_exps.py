import fitsio
import desimodel
import numpy as np
import astropy.io.fits as fits

from   astropy.table import Table, unique
from   desisurvey.utils import get_date
from   desimodel.footprint import is_point_in_desi


dat          = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc-spring2020e-onepercent/survey/exposures_surveysim.fits')[1].data)
dat['NIGHT'] = ['               '] * len(dat)

for i, mjd in enumerate(dat['MJD']):
  dat['NIGHT'][i] = get_date(mjd)
  dat['NIGHT'][i] = dat['NIGHT'][i].replace('-', '')

# dat.pprint(max_width=-1)

# dat.write('/global/cscratch1/sd/mjwilson/svdc-spring2020b-onepercent/survey/exposures_surveysim_fix.fits', format='fits', overwrite=True)

complete = dat[dat['SNR2FRAC'] >= 1.0]
complete.sort('TILEID')

# complete = unique(complete, keys='TILEID')

complete.pprint(max_lines=-1)

# complete.write('/global/cscratch1/sd/mjwilson/svdc-spring2020b-onepercent/survey/complete_exposures_surveysim_fix.fits', format='fits', overwrite=True)

