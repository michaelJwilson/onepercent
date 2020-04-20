import numpy as np
import pylab as pl


for linestyle, weighted in zip(['-', '--'], [True, False]):
  ss, Q0, Q2, Q4, Q6 = np.loadtxt('Qs_onepercent_weighted_{}.txt'.format(np.int(weighted)), unpack=True)

  for ell, Q in zip([0, 2, 4, 6], [Q0, Q2, Q4, Q6]):
    isin = ss > 5.0

    norm = Q0[isin][0]
  
    pl.semilogx(ss[isin], np.abs(Q[isin]) / norm, label=r'$\ell={}$'.format(ell), marker='^', linestyle=linestyle)

pl.xlim(5., 700.)
pl.xlabel(r'$s \ [\rm{Mpch} / h]$')
pl.ylabel(r'$Q_{\ell}(s)$')
pl.legend(frameon=False)
pl.show()

print('\n\nDone.\n\n')
