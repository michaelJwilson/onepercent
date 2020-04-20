import os
import glob
import numpy as np


ff    = glob.glob('run/targets/*/*/build-64-*.log')
find  = 'INFO:mockmaker.py:413:imaging_depth: Setting realistic imaging depths (including MASKBITS).\n'

found = 0

for n in ff:
    f = open(n, 'r')    
    x = f.readlines()

    if find in x:
        found += 1
        
        print('Success on {}'.format(n))


    else:
        print('Failed on {}'.format(n))
        
        cmd = 'rm -r {}'.format('/'.join(np.array(n.split('/')[:-1])))
        os.system(cmd)

print('Found {} of {}'.format(found, len(ff)))    
        
print('\n\nDone.\n\n')
