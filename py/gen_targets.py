import os
import fitsio
import numpy           as np
import astropy.io.fits as fits


info    = fits.open('/global/cscratch1/sd/mjwilson/svdc-spring2020a-onepercent/targets/targets.fits').info()

rows    = list(range(100))

# rows=rows
targets = fitsio.read('/global/cscratch1/sd/mjwilson/svdc-spring2020a-onepercent/targets/targets.fits')
truth   = fitsio.read('/global/cscratch1/sd/mjwilson/svdc-spring2020a-onepercent/targets/truth.fits')  

assert  np.all(targets['TARGETID'] == truth['TARGETID'])

ngc     = (targets['RA'] > 100.) & (targets['RA'] < 275.)
sgc     = ~ngc

targets = targets[sgc]
truth   =   truth[sgc]

fitsio.write('/global/cscratch1/sd/mjwilson/svdc-spring2020a-onepercent/targets/targets-sgc.fits', targets)
fitsio.write('/global/cscratch1/sd/mjwilson/svdc-spring2020a-onepercent/targets/truth-sgc.fits', truth)
