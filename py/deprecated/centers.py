import os 
import pylab               as      pl
import numpy               as      np
import astropy.io.fits     as      fits
import matplotlib.patches  as      mpatches
import matplotlib.pyplot   as      plt 

from   astropy.table       import  Table, vstack
from   desitarget.geomask  import  circles


kwargs  = {'facecolor': None, 'lw': 1., 'alpha': 0.5} 
colors  = ['k', 'r', 'y', 'g', 'b', 'magenta', 'cyan', 'darkorchid', 'orange', 'lawngreen', 'orangered']

patches = []
labels  = passes = np.arange(0, 11, 1)

print('Solving for passes: {} to {}.'.format(passes.min(), passes.max()))

for _pass, color in zip(labels, colors):
  patches.append(mpatches.Patch(color=color, alpha=0.2, label='Pass ' + str(_pass)))

home    = '/global/homes/m/mjwilson/svdc2019c2/'
root    = os.environ['CSCRATCH'] + '/svdc2019c2/survey/'
  
##
tiles   = Table(fits.open(root + '/basetiles/schlafly-tiles.fits')[1].data)
centers = np.loadtxt(home + '/OP-CENTERIDS')

base    = tiles[tiles['PASS'].quantity == 4]

opone   = centers[:,0].astype(np.int)
optwo   = centers[:,1][centers[:,1] >= 0].astype(np.int)
oponeb  = centers[:,2][centers[:,2] >= 0].astype(np.int)
 
print(opone)
print(optwo)
print(oponeb)

##
np.savetxt(root + 'tiles/schlafly/opone.txt',  opone,  fmt='%d')
np.savetxt(root + 'tiles/schlafly/optwo.txt',  optwo,  fmt='%d')
np.savetxt(root + 'tiles/schlafly/oponeb.txt', oponeb, fmt='%d')

np.savetxt(root + 'tiles/schlafly/opall.txt',  np.concatenate([opone,  optwo]), fmt='%d')
np.savetxt(root + 'tiles/schlafly/opallb.txt', np.concatenate([oponeb, optwo]), fmt='%d')

isin    = [x in opone for x in tiles['CENTERID'].quantity]
opone   = tiles[isin]

isin    = [x in optwo for x in tiles['CENTERID'].quantity]
optwo   = tiles[isin]

isin    = [x in oponeb for x in tiles['CENTERID'].quantity]
oponeb  = tiles[isin]

opall   = vstack([opone,  optwo])
opallb  = vstack([oponeb, optwo])

print(opone)
print(optwo)

print(opall)
print(opallb)

opone.sort('TILEID')
optwo.sort('TILEID')
opall.sort('TILEID')
opallb.sort('TILEID')

##  
opone.write(root + 'tiles/schlafly/opone.fits',   format='fits', overwrite=True)
optwo.write(root + 'tiles/schlafly/optwo.fits',   format='fits', overwrite=True)
opall.write(root + 'tiles/schlafly/opall.fits',   format='fits', overwrite=True)
opallb.write(root + 'tiles/schlafly/opallb.fits', format='fits', overwrite=True)

##
lims     = [[[163., 186.], [-6., 6.]], [[207., 231.], [-4., 4.]], [[197., 227.], [34., 46.]]]
programs = ['DARK', 'GRAY', 'BRIGHT']

for op, field, lim in zip([opone, optwo, oponeb], ['opone', 'optwo', 'oponeb'], lims):
  for program in ['BRIGHT']:
    pl.clf()

    circles(base['RA'].quantity, base['DEC'].quantity, s=1.67, ec='k', lw=1., fc='None', alpha=0.4)
    
    for _pass, color in zip(passes, colors):
      kwargs['facecolor'] = color

      isin = (op['PASS'].quantity == _pass) & (op['PROGRAM'] == program)

      circles(op[isin]['RA'].quantity, op[isin]['DEC'].quantity, s=1.67, c=color, alpha=0.2, label=_pass)

    pl.legend(patches, labels, frameon=False, ncol=1)
    
    ax      = pl.gca()

    plotted = []
    
    for i, txt in enumerate(op['CENTERID'].quantity):
      if txt not in plotted:
        ax.annotate(txt, (op['RA'].quantity[i], op['DEC'].quantity[i]), verticalalignment='center', horizontalalignment='center', alpha=0.8)

      plotted.append(txt)    
    
    sample = base[(base['RA'].quantity > lim[0][0]) & (base['RA'].quantity < lim[0][1]) & (base['DEC'].quantity > lim[1][0]) & (base['DEC'].quantity < lim[1][1])]

    for i, txt in enumerate(sample['CENTERID'].quantity):
      if txt not in plotted:
        ax.annotate(txt, (sample['RA'].quantity[i], sample['DEC'].quantity[i]), verticalalignment='center', horizontalalignment='center', alpha=0.2)

      plotted.append(txt)
  
    pl.xlabel('Right ascension [deg.]')
    pl.ylabel('Declination [deg.]')

    pl.title(program)

    pl.xlim(lim[0][0], lim[0][1])
    pl.ylim(lim[1][0], lim[1][1])

    plt.gca().invert_xaxis()

    pl.show()
    ##  pl.savefig('plots/tiles/program_{}_{}.pdf'.format(field, program))
