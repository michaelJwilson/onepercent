from   nbodykit.lab                 import *
from   nbodykit                     import setup_logging, style

from   nbodykit.source.catalog.file import FITSCatalog
from   scipy.interpolate            import InterpolatedUnivariateSpline
from   desitarget.targets           import desi_mask, bgs_mask, mws_mask
from   nbodykit                     import CurrentMPIComm
from   mcfit                        import P2xi, xi2P
from   scipy.interpolate            import interp1d

import os
import json
import argparse

import numpy                        as     np
import nbodykit
import pylab                        as     pl 
import matplotlib.pyplot            as     plt


setup_logging()

# comm              = CurrentMPIComm.get()

# Fiducial BOSS DR12 cosmology
h                   = 0.676
Ob0                 = 0.022/h**2
Ocdm0               = 0.31 - Ob0
cosmo               = cosmology.Cosmology(h=h, Omega_b=Ob0, Omega_cdm=Ocdm0, N_ur = 2.0328, N_ncdm = 1, m_ncdm = 0.06, T_cmb=2.7255)

root                = '/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/'

#
k                   = np.logspace(-5, 1, 500)

linb                = np.sqrt(6.5)

c                   = cosmology.Planck15
Plin                = cosmology.LinearPower(c, redshift=0.7, transfer='CLASS')
Pnl                 = cosmology.HalofitPower(c, redshift=0.7)
Pzel                = cosmology.ZeldovichPower(c, redshift=0.7)

# Windowed.
s, xi               = P2xi(k)(Pnl(k))

ss, Q0, _, _, _     = np.loadtxt('Qs_onepercent_weighted_1.txt', unpack=True)
isin                = ss > 5.0

Q0                  = Q0[isin] / Q0[isin][0]
ss                  = ss[isin]

Q0                  = interp1d(ss, Q0, kind='linear', copy=True, bounds_error=False, fill_value=(Q0[0], Q0[-1]), assume_sorted=False)
Q0                  = Q0(s)

xi                 *= Q0

plt.loglog(k, linb * linb * Plin(k), c='k', linestyle='--')
plt.loglog(k, linb * linb * Pnl(k), c='k')

k, P                = xi2P(s)(xi)

plt.loglog(k, linb * linb * P, alpha=0.5, c='tab:blue')

#
for marker, weighted in zip(['s', '^'], [0,1]):
  output_dir          = "/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/clustering/pk/"
  output              = os.path.join(output_dir, "oneper_weighted_{:d}.json".format(weighted))

  r                   = ConvolvedFFTPower.load(output)

  poles               = r.poles

  pl.axhline(r.attrs['shotnoise'], xmin=0.0, xmax=1.0, c='k', alpha=0.3)

  # label             = r'$P_0$'
  label               = 'Weighted {}'.format(weighted)
  
  pl.errorbar(poles['k'],  poles['power_0'].real - r.attrs['shotnoise'], (poles['power_0'].real - r.attrs['shotnoise']) / np.sqrt(poles['modes']), label=label, lw=0.0, elinewidth=1.0, fmt='^', markersize=3)
  # pl.errorbar(poles['k'], -poles['power_2'], poles['power_2'] / np.sqrt(poles['modes']), label=r'$P_2$', lw=0.0, elinewidth=0.2, fmt='^', markersize=3)

  print('\n\n----  Weighted {} ----'.format(np.int(weighted)))
  
  for i, k, in enumerate(poles['k']):
    print('{:.6f} \t {:.6f}'.format(k, poles['power_0'][i].real - r.attrs['shotnoise']))

pl.xscale('log')
pl.yscale('log')

# format the axes
plt.legend(loc=0, frameon=False)
plt.xlabel(r"$k$ [$h \ \mathrm{Mpc}^{-1}$]")
plt.ylabel(r"$P_\ell$ [$h^{-3} \mathrm{Mpc}^3$]")
plt.xlim(0.01, 1.50)
plt.ylim(1.e2, 2.e5)

pl.show()

print('\n\nDone.\n\n')
