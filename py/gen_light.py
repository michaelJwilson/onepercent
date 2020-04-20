import  glob 
import  fitsio


root    = '../run/targets/'
targets = glob.glob(root + '*.fits')
targets = [x.split('/')[-1] for x in targets]

targets.remove('skies.fits')

targets = [x for x in targets if x[0] != '_']
targets = [x.replace('.fits','') for x in targets if len(x.split('-')) < 3]

print(targets)

rows    = list(range(10000))

for x in targets:
  dat   = fitsio.read(root + x + '.fits', rows=rows)

  opath = root + x + '-lite.fits'

  print(opath)

  fitsio.write(opath, dat)
