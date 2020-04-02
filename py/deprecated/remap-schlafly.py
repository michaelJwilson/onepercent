import time
import copy
import numpy as np
import astropy.io.fits as     fits

from   astropy.table   import Table, vstack


##  DARK: 1,2,3,4;  GRAY: 0;  BRIGHT: 5,6,7;  EXTRA: 8,9  to  DARK: 0,1,2,3,4;  GRAY: 5,6;  BRIGHT: 7,8,9,10. 
dat    = Table(fits.open('basetiles/original/schlafly-tiles.fits')[1].data)
result = Table(fits.open('basetiles/original/schlafly-tiles.fits')[1].data)
reuse  = Table(fits.open('basetiles/original/schlafly-tiles.fits')[1].data)

##  Reuse 5th BGS pass for additional GRAY-like 10th pass.                                                                                                                                                      
reuse                  = reuse[reuse['PASS'] == 5]
reuse['PASS']          = 10
reuse['OBSCONDITIONS'] = 2
reuse['PROGRAM']       = 'GRAY'
reuse['TILEID']        = reuse['TILEID'].quantity.max() + 1 + np.arange(len(reuse['TILEID'].quantity))

for _file in [dat, result]:
  ##  Remap EXTRA 8th pass to BRIGHT.
  _file['OBSCONDITIONS'][_file['PASS'] == 8] = 4
  _file['PROGRAM'][_file['PASS'] == 8]       = 'BRIGHT'

  ##  Remap EXTRA 9th pass to DARK.                                                                                                                                                                 
  _file['OBSCONDITIONS'][_file['PASS'] == 9] = 1
  _file['PROGRAM'][_file['PASS'] == 9]       = 'DARK'

dat    = vstack([dat,    reuse])  
result = vstack([result, reuse])

##  Remains to remap pass numbers.
remap = {5: 7, 6: 8, 7: 9, 8: 10, 0: 5, 10: 6, 1: 0, 2: 1, 3: 2, 4: 3, 9: 4}

for _pass in np.arange(0, 11, 1):
    print('\n\nRemapping layer {} ({} entries) to layer {} ({} entries)'.format(_pass, np.sum(dat['PASS'] == _pass), remap[_pass], np.sum(dat['PASS'] == remap[_pass])))
    
    result['PASS'][dat['PASS'] == _pass] = remap[_pass]

result.sort(['PASS', 'TILEID'])

result['TILEID'] = np.arange(len(result['TILEID']))

print('\n\nSolved for result:')

for _pass in np.arange(0, 11, 1):
  print(result[result['PASS'].quantity == _pass])

  time.sleep(5)

result.write('basetiles/schlafly-tiles.fits', overwrite=True)
