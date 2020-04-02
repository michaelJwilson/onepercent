import os
import pylab           as     pl
import numpy           as     np
import astropy.io.fits as     fits

from   astropy.table   import Table


tiles = Table(fits.open('sandbox/desi-tiles.fits')[1].data)

home    = '/global/homes/m/mjwilson/svdc2019c2/'
root    = os.environ['CSCRATCH'] + '/svdc2019c2/survey/'

##                                                                                                                                                                                                                        
centers = np.loadtxt(home + '/OP-CENTERIDS')

opone   = centers[:,0].astype(np.int)
optwo   = centers[:,1][centers[:,1] >= 0].astype(np.int)
oponeb  = centers[:,2][centers[:,2] >= 0].astype(np.int)

mapping = np.loadtxt(home + '/CENTERID-MAPPING')
mapping = mapping.astype(np.int)

##  print(opone)
##  print(mapping)
'''
##  OPONE
nopone  = []

for x in opone:
  where = mapping[:,0] == x

  nopone.append(mapping[where, 1])

nopone  = np.array(nopone)

##  print(nopone)

isin    = [x in nopone for x in tiles['centerid'].quantity]
opone   = tiles[isin]

print(opone)
print(np.unique(opone['centerid']))

##  pl.plot(opone['ra'], opone['dec'], 'ko')
##  pl.show()
'''
'''
##  OPTWO
noptwo  = []

for x in optwo:
  where = mapping[:,0] == x

  noptwo.append(mapping[where, 1])

noptwo  = np.array(noptwo)

##  print(nopone)                                                                                                                                                                                                     

isin    = [x in noptwo for x in tiles['centerid'].quantity]
optwo   = tiles[isin]

print(optwo)
print(np.unique(optwo['centerid']))

##  pl.plot(optwo['ra'], optwo['dec'], 'ko')
##  pl.show()
'''

##  OPONEB                                                                                                                                                                                                                            
noponeb  = []                                                                                                                                                                                                                            
for x in oponeb:
  where = mapping[:,0] == x

  noponeb.append(mapping[where, 1])                                                                                                                                                                                                    

noponeb  = np.array(noponeb)                                                                                                                                                                                                           
                                                                                                                                                                                                                                      
isin     = [x in noponeb for x in tiles['centerid'].quantity]                                                                                                                                                                         
oponeb   = tiles[isin]                                                                                                                                                                                                                

print(oponeb)
print(np.unique(oponeb['centerid']))

##  pl.plot(oponeb['ra'], oponeb['dec'], 'ko')
##  pl.show() 

