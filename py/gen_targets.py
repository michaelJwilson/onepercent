import os
import fitsio
import numpy           as np
import astropy.io.fits as fits

release = 'e'
light   = 'dark'

info    = fits.open('/global/cscratch1/sd/mjwilson/svdc-spring2020{}-onepercent/targets/_targets-{}.fits'.format(release, light)).info()

# rows  = list(range(100))
# rows=rows
targets = fitsio.read('/global/cscratch1/sd/mjwilson/svdc-spring2020{}-onepercent/targets/_targets-{}.fits'.format(release, light))
truth   = fitsio.read('/global/cscratch1/sd/mjwilson/svdc-spring2020{}-onepercent/targets/_truth-{}.fits'.format(release, light))  

assert  np.all(targets['TARGETID'] == truth['TARGETID'])

ngc     = (targets['RA'] > 100.) & (targets['RA'] < 275.)
sgc     = ~ngc

targets = targets[sgc]
truth   =   truth[sgc]

fitsio.write('/global/cscratch1/sd/mjwilson/svdc-spring2020{}-onepercent/targets/targets-{}-sgc.fits'.format(release, light), targets)
fitsio.write('/global/cscratch1/sd/mjwilson/svdc-spring2020{}-onepercent/targets/truth-{}-sgc.fits'.format(release, light), truth)
