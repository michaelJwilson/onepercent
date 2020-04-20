import fitsio
import numpy               as      np
import desitarget.randoms  as      randoms

from   astropy.table       import  Table
from   desiutil            import  brick
from   desitarget.targets  import  resolve


def maskbits(targets, release=8):
    print('Setting MASKBITS.')

    bricks      = brick.Bricks()

    # Return brick name of brick covering (ra, dec).
    bricknames  = bricks.brickname(targets['RA'], targets['DEC'])

    ubricknames = np.unique(bricknames)

    drdir       = '/global/project/projectdirs/cosmo/data/legacysurvey/dr{}'.format(release)

    # determine if we must traverse two sets of brick directories, i.e. north/, south/.
    drdirs      = randoms._pre_or_post_dr8(drdir)
    
    for ubrickname in ubricknames:
      indx      = targets['BRICKNAME'] == ubrickname

      rtn       = randoms.dr8_quantities_at_positions_in_a_brick(targets['RA'][indx], targets['DEC'][indx], ubrickname, drdir)
          
      if rtn:          
          for key in list(rtn.keys()):
              rtn[key.upper()] = rtn.pop(key)

          rtn        = Table(rtn)
          rtn['RA']  = targets['RA'][indx]
          rtn['DEC'] = targets['DEC'][indx]
            
          rtn        = resolve(Table(rtn))

          print(rtn.keys())

          exit(0)
          
          for key in rtn.keys():
              # Assume desitarget/mock/ target cat. model is up-to-date. 
              if key in targets.columns:
                  targets[key][indx] = rtn[key] 
          
      else:
          # Empty dict:  missing brick.
          toremove   = np.where(indx)[0] 
          targets.remove_rows[indx]
           
    return  targets
  

if  __name__ ==  '__main__':
    fpath     = '../run/targets/targets-dark-lite.fits'

    dat       = Table.read(fpath)
    
    dat       = maskbits(dat, release=8)
    
    print(dat)
