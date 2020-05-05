from   desimodel.footprint import tiles2pix
from   astropy.table       import Table


tiles       = Table.read('../run/survey/tiles/onepercent.fits')

healpixels  = tiles2pix(64, tiles).tolist()
string      = ' '.join([str(x) for x in healpixels])

print(string)
