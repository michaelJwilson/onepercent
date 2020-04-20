from   nbodykit.lab                 import *
from   nbodykit                     import setup_logging, style

from   nbodykit.source.catalog.file import FITSCatalog
from   scipy.interpolate            import InterpolatedUnivariateSpline
from   desitarget.targets           import desi_mask, bgs_mask, mws_mask
from   nbodykit                     import CurrentMPIComm

import os
import argparse

import numpy                        as     np
import nbodykit
import pylab                        as     pl 
import matplotlib.pyplot            as     plt


setup_logging()

# comm              = CurrentMPIComm.get()

weighted            = True

# Fiducial BOSS DR12 cosmology
h                   = 0.676
Ob0                 = 0.022/h**2
Ocdm0               = 0.31 - Ob0
cosmo               = cosmology.Cosmology(h=h, Omega_b=Ob0, Omega_cdm=Ocdm0, N_ur = 2.0328, N_ncdm = 1, m_ncdm = 0.06, T_cmb=2.7255)

root                = '/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/'

data                = FITSCatalog(root + '/run/catalogs/dark/tarzcatdark.fits')
data['Weight']      = numpy.ones(data.csize)

if not weighted:
  randoms           = FITSCatalog(root + '/run/randoms/dark/randoms_oneper_darktime_jmtl_truez.fits')
  randoms['Weight'] = numpy.ones(randoms.csize)

else:
  randoms           = FITSCatalog(root + 'run/catalogs/dark/LRG_oneper_clus.ran.fits')
  randoms['Weight'] = randoms['WEIGHT']
  
lrgs                = (data['DESI_TARGET'] & desi_mask["LRG"]) != 0

data                = data[lrgs & (data['ZWARN'] == 0) & (data['Z'] > 0.5) & (data['Z'] < 1.0)]
randoms             = randoms[(randoms['Z'] > 0.5) & (randoms['Z'] < 1.0)]

# add Cartesian position column
data['Position']    = transform.SkyToCartesian(data['RA'], data['DEC'], data['Z'], cosmo=cosmo)
randoms['Position'] = transform.SkyToCartesian(randoms['RA'], randoms['DEC'], randoms['Z'], cosmo=cosmo)

#data               = data[::10]
#randoms            = randoms[::10]

# the sky fraction, used to compute volume in n(z)
fsky                = 140. / 41252.96

# compute n(z) from the randoms
zhist               = RedshiftHistogram(randoms, fsky, cosmo, redshift='Z', bins=25)

# re-normalize to the total size of the data catalog
alpha               = 1.0 * data.csize / randoms.csize

print('Randoms oversample density by {:.3f}'.format(1. / alpha))

# add n(z) from randoms to the FKP source; return boundary value.
print(zhist.bin_centers)
print(alpha * zhist.nbar)

nofz                = InterpolatedUnivariateSpline(zhist.bin_centers, alpha * zhist.nbar, ext=3, k=1)

data['NZ']          = nofz(data['Z'])
randoms['NZ']       = nofz(randoms['Z'])

# pl.plot(data['Z'], data['NZ'], marker='.', lw=0.0, markersize=0.2)
# pl.show()

'''
plt.plot(zhist.bin_centers, alpha*zhist.nbar)
plt.xlabel(r"$z$", fontsize=16)
plt.ylabel(r"$n(z)$ $[h^{3} \mathrm{Mpc}^{-3}]$", fontsize=16)

pl.show()
'''

# initialize the FKP source
fkp                       = FKPCatalog(data, randoms)

fkp['data/NZ']           = data['NZ']
fkp['randoms/NZ']        = randoms['NZ']

# FKP weights.
fkp['data/FKPWeight']    = 1.0 / (1 + fkp['data/NZ'] * 1.e4)
fkp['randoms/FKPWeight'] = 1.0 / (1 + fkp['randoms/NZ'] * 1.e4)

# Completeness weights, defined by number density -> w x number density. 
fkp['data/Weight']       = data['Weight']
fkp['randoms/Weight']    = randoms['Weight']

window                   = 'tsc'
mesh                     = fkp.to_mesh(Nmesh=512, nbar='NZ', comp_weight='Weight', fkp_weight='FKPWeight', window=window, interlaced=True, compensated=True)

# apply correction for the window to the mesh.
# compensation           = mesh.CompensateCIC if window == 'CIC' else mesh.CompensateTSC
# mesh                   = mesh.apply(compensation, kind='circular', mode='complex')

poles                    = [0, 2, 4]
r                        = ConvolvedFFTPower(mesh, poles=poles, dk=0.01, kmin=0.01)
'''
for key in r.attrs:
    print("%s = %s" % (key, str(r.attrs[key])))

#
poles = r.poles

for ell in poles:
    label = r'$\ell=%d$' % (ell)
    P = poles['power_%d' %ell].real
    if ell == 0: P = P - poles.attrs['shotnoise']
    plt.plot(poles['k'], P, label=label)

# format the axes
plt.legend(loc=0)
plt.xlabel(r"$k$ [$h \ \mathrm{Mpc}^{-1}$]")
plt.ylabel(r"$P_\ell$ [$h^{-3} \mathrm{Mpc}^3$]")
plt.xlim(0.01, 0.3)

pl.show()
'''
# and save!
output_dir  = "/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/clustering/pk/"
output      = os.path.join(output_dir, "oneper_weighted_{}.json".format(np.int(weighted)))

if os.path.exists(output):
    os.remove(output)

r.save(output)

print('\n\nDone.\n\n')
