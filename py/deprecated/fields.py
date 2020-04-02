import numpy               as     np
import pylab               as     pl
import astropy.units       as     u

from   astropy.coordinates import SkyCoord


##  COSMOS
cosmos       = SkyCoord(+150.11916667 * u.deg, +2.20583333 * u.deg) 
cosmos       = np.array([[cosmos.ra.degree - x, cosmos.dec.degree - y] for x in np.arange(-1, 2., 1.) for y in np.arange(-1, 2., 1.)])

print(cosmos)

pl.plot(cosmos[:,0], cosmos[:,1], 'y', label='cosmos', lw=1)


##  HSC, https://arxiv.org/pdf/1704.05858.pdf
north_one    = SkyCoord('13h20m00s', 42.0 * u.deg, frame='icrs')
north_two    = SkyCoord('13h20m00s', 44.5 * u.deg, frame='icrs')
north_three  = SkyCoord('16h40m00s', 42.0 * u.deg, frame='icrs')
north_four   = SkyCoord('16h40m00s', 44.5 * u.deg, frame='icrs')

spreq_one    = SkyCoord('08h30m00s', -2.0 * u.deg, frame='icrs')
spreq_two    = SkyCoord('08h30m00s',  5.0 * u.deg, frame='icrs')
spreq_three  = SkyCoord('15h00m00s', -2.0 * u.deg, frame='icrs')
spreq_four   = SkyCoord('15h00m00s',  5.0 * u.deg, frame='icrs')

faleq_one    = SkyCoord('22h00m00s', -1.0 * u.deg, frame='icrs')
faleq_two    = SkyCoord('22h00m00s',  7.0 * u.deg, frame='icrs')
faleq_three  = SkyCoord('02h40m00s', -1.0 * u.deg, frame='icrs')
faleq_four   = SkyCoord('02h40m00s',  7.0 * u.deg, frame='icrs')

north        = np.array([[x.ra.degree, x.dec.degree] for x in [north_one,   north_two,  north_four, north_three, north_one]])
spreq        = np.array([[x.ra.degree, x.dec.degree] for x in [spreq_one,   spreq_two,  spreq_four, spreq_three, spreq_one]])
faleq        = np.array([[x.ra.degree, x.dec.degree] for x in [faleq_three, faleq_four, faleq_two,  faleq_one, faleq_three]])

fields, labels = [north, spreq], ['North', 'Spring Eq.']

for x, label in zip(fields, labels):
    pl.plot(x[:,0], x[:,1], label=label)

##  Wrap-around for Fall. Eq.
segments = []
segments.append(np.array([[faleq_two.ra.degree, faleq_two.dec.degree], [360., faleq_two.dec.degree]]))
segments.append(np.array([[faleq_two.ra.degree, faleq_one.dec.degree], [360., faleq_one.dec.degree]]))

segments.append(np.array([[0.0, faleq_two.dec.degree], [faleq_three.ra.degree, faleq_two.dec.degree]]))
segments.append(np.array([[0.0, faleq_one.dec.degree], [faleq_three.ra.degree, faleq_one.dec.degree]]))

segments.append(np.array([[faleq_three.ra.degree, faleq_three.dec.degree], [faleq_four.ra.degree, faleq_four.dec.degree]]))
segments.append(np.array([[faleq_one.ra.degree,   faleq_one.dec.degree],   [faleq_two.ra.degree,   faleq_two.dec.degree]]))

for segment in segments:
  pl.plot(segment[:,0], segment[:,1], c='k')

##  Fake-line for label
pl.plot(segment[-1,0], segment[-1,1], c='k', label='Fall Eq.')
 
pl.xlim(-1, 361.)

pl.legend(frameon=False)

pl.savefig('hsc.pdf')

