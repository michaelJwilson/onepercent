#! /bin/bash

#SBATCH -N 1                                                                                                                                                                                                                               
#SBATCH -p debug                                                                                                                                                                                                                           
#SBATCH -t 00:29:00                                                                                                                                                                                                                        
#SBATCH -J onepercent                                                                                                                                                                                                                 
#SBATCH -C haswell                                                                                                                                                                                                                         
#SBATCH -o "/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/clustering/pk/slurm-cori-%j.out"                                                                                                             
#SBATCH -e "/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/clustering/pk/slurm-cori-%j.err"                                                                                                                                                         
cd $SLURM_SUBMIT_DIR

# source /global/common/software/m3035/conda-activate.sh 3.7
conda activate e2e

# bcast-pip https://github.com/bccp/nbodykit/archive/master.zip

export PATH=/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/desitarget/bin/:$PATH
export PYTHONPATH=/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/desitarget/:/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/desitarget/py/:$PYTHONPATH

export PATH=/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/desiutil/bin/:$PATH
export PYTHONPATH=/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/desiutil/:/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020f-onepercent/desiutil/py/:$PYTHONPATH

srun -n 32 /global/homes/m/mjwilson/.conda/envs/e2e/bin/python Pk.py
