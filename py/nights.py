import numpy           as     np
import astropy.io.fits as     fits

from   astropy.table   import Table 

dat          = np.loadtxt('/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020a-onepercent/nights.txt')
dat          = np.c_[dat]

tab          = Table()
tab['NIGHT'] = dat

print(tab.columns)

tab.write('/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020a-onepercent/nights.fits', format='fits', overwrite=True)

print(tab)
