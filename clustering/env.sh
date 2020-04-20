conda activate e2e

# alias python=/global/homes/m/mjwilson/.conda/envs/e2e/bin/python3.7

addrepo ../desitarget; addrepo ../desiutil

# 32 hyper threaded by 2.
export NUMEXPR_MAX_THREADS=64
