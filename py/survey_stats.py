import os
import pylab           as     pl

from   surveysim.stats import SurveyStatistics

os.environ['DESISURVEY_OUTPUT'] = '/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020g-onepercent/run/survey/'
stats                           = SurveyStatistics(restore='stats_surveysim.fits', tiles_file='/global/cscratch1/sd/mjwilson/svdc-spring2020g-onepercent/survey/tiles/onepercent.fits',\
                                                   config_file='/global/homes/m/mjwilson/desi/survey-validation/svdc-spring2020g-onepercent/config.yaml')
stats.plot()

pl.show()
