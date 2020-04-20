import glob
import os.path, time
import numpy    as np


files = np.array(glob.glob('*/*/dark/targets-*.fits'))

times = []

for file in files:
  # print('\n\n{}'.format(file))

  times.append(os.path.getctime(file))
  
times = np.array(times)

indx  = np.argsort(times).tolist()

print(files[indx])
