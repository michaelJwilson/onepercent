import  time
import  astropy.io.fits      as      fits
import  surveysim.stats      as      simstats
import  numpy                as      np
import  astropy.units        as      u 
import  pylab                as      pl
import  matplotlib.pyplot    as      plt 

from    astropy.table        import  Table, join
from    astropy.time         import  Time, TimeDelta
from    datetime             import  datetime
from    desisurvey.utils     import  get_location, get_airmass, local_noon_on_date, get_date 
from    expderived           import  expderived
from    astropy.coordinates  import  SkyCoord, BaseEclipticFrame


daycut       =  False

date         = '2020-04-15'
program      = 'GRAY' 

mayall       = get_location()

tiles        = fits.open('tiles/schlafly/opall.fits')
tiles        = Table(tiles[1].data) 

exps         = fits.open('exposures_surveysim.fits')
exps         = Table(exps[1].data)

exps['KPT']  = (Time([x.value for x in exps['MJD'].quantity], format='mjd') - TimeDelta(60. * 60. * 5.0, format='sec')).iso

exps         = expderived(exps, tiles=tiles)
exps['DAY']  = np.array([str(get_date(x)) for x in exps['MJD']])
exps['TWI']  = np.array([1 if x >= -15. else 0 for x in exps['SUNALT']])

cs           = [SkyCoord(ra = ra * u.degree, dec = dec * u.degree, frame='icrs').transform_to('barycentrictrueecliptic') for ra, dec in zip(exps['RA'].quantity, exps['DEC'].quantity)]
exps['ELON'] = [x.lon.value for x in cs]
exps['ELAT'] = [x.lat.value for x in cs]

##  Bright program cut. 
isin         = [x == program for x in exps['PROGRAM']]
##  exps     = exps[isin]

##  Low ecliptic latitude cut. 
isin         = [np.abs(x) <= 15. for x in exps['ELAT']]
exps         = exps[isin]

##  Lower RA field.
isin         = [np.abs(x) <= 190. for x in exps['RA']]
##  exps     = exps[isin]

exps.sort('MJD')

exps.remove_column('SKY')
exps.remove_column('IN_DESI')
exps.remove_column('BRIGHTRA')
exps.remove_column('BRIGHTDEC')
exps.remove_column('BRIGHTVTMAG')

dat          = Table(fits.open('/global/cscratch1/sd/mjwilson/svdc2019c2/survey/stats_surveysim.fits')[1].data)
dat['ISO']   = Time([x.value for x in dat['MJD'].quantity], format='mjd').iso
dat['DAY']   = np.array([x.split(' ')[0] for x in dat['ISO']])

dat['topen'] = np.sum(dat['topen'].quantity, axis=1)
dat['tdead'] = np.sum(dat['tdead'].quantity, axis=1)

if daycut:
  isin       = [x == program for x in exps['PROGRAM']]  
  exps       = exps[isin]

  isin       = [x == date for x in dat['DAY']]
  dat        = dat[isin]

dat.remove_column('completed')
dat.remove_column('nexp')
dat.remove_column('nsetup')
dat.remove_column('nsplit')
dat.remove_column('nsetup_abort')
dat.remove_column('nsplit_abort')
dat.remove_column('MJD')
dat.remove_column('ISO')

##  stats   = simstats.SurveyStatistics(restore='/global/cscratch1/sd/mjwilson/svdc2019c2/survey/stats_surveysim.fits', tiles_file='/global/cscratch1/sd/mjwilson/svdc2019c2/survey/tiles/schlafly/opall.fits', start_date='2020-04-15', stop_date='2020-05-15' )

result      = join(exps, dat, keys='DAY', join_type='outer')

tsciences   = []
tsetups     = []
tsplits     = []

for i in range(len(result['tscience'])):
  try:
    tsciences.append(result['tscience'][i, result['PASS'][i].astype(np.int)])
    tsplits.append(  result['tsplit'][i, result['PASS'][i].astype(np.int)])
    tsetups.append(  result['tsetup'][i, result['PASS'][i].astype(np.int)])
    
  except:
    tsciences.append(np.NaN)
    tsplits.append(np.NaN)
    tsetups.append(np.NaN)
    
result.remove_column('tscience')
result.remove_column('tsplit')
result.remove_column('tsetup')

result['tscience/pass'] = np.array(tsciences)
result['tsplit/pass']   = np.array(tsplits)
result['tsetup/pass']   = np.array(tsetups)

result.sort('MJD')

result.remove_column('MJD')
result.remove_column('STAR_DENSITY')
result.remove_column('EXPOSEFAC')
result.remove_column('TRANSP')

##  print(exps)
##  print(dat)
##  print(result)

for date in dat['DAY']:
  print('\n\nExposures result for day: {}\n'.format(date))

  subsample = result[result['DAY'] == date]

  opone     = subsample[subsample['RA'] < 190.]
  optwo     = subsample[subsample['RA'] > 190.]
  
  print(opone)
  print('\n\n')
  print(optwo)

  ##  opone.write('explog/{}-1.txt'.format(date), format='ascii', overwrite=True)
  ##  optwo.write('explog/{}-2.txt'.format(date), format='ascii', overwrite=True)
  
  ##  time.sleep(10)
'''  
## 
pl.scatter(exps['MOONALT'], exps['MOONFRAC'], c=exps['MOONSEP'], vmin=50., vmax=150.)
plt.colorbar(label='Separation angle [deg.]')

##  Product of moon frac. and altitude is 30 deg.
ordinate = np.arange(0., 90., 1.)

abcissae = 30. / ordinate
abcissae[abcissae > 0.6] = 0.6

pl.plot(ordinate, abcissae, 'k-')

pl.xlabel('Moon altitude [deg.]')
pl.ylabel('Moon illumination frac.')

pl.xlim(0., 90.)
pl.ylim(0.,  1.)

pl.title(program)

plt.show()
'''

print('\n\nDone.\n\n')
