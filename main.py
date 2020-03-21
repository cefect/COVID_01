#===============================================================================
# call check
#===============================================================================
import sys
print('called w/ %i args: \n%s'%(len(sys.argv), sys.argv))

assert len(sys.argv) >2, 'failed to call w/ enough arguments'


#==============================================================================
# dependency check
#==============================================================================
# Let users know if they're missing any of our hard dependencies
hard_dependencies = ('pandas', 'numpy','seaborn','matplotlib','geopy','tqdm', 'geopandas','shapely','numba','rpy2')
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append("{0}: {1}".format(dependency, str(e)))

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
    
del hard_dependencies, dependency, missing_dependencies

#===============================================================================
# imports
#===============================================================================



import numpy as np
import pandas as pd
import datetime, time, multiprocessing, itertools, sys
import matplotlib.pyplot as plt

#===============================================================================
# setup R
#===============================================================================

import os
os.environ["R_USER"] = "R_USER"
os.environ["R_HOME"] = r"C:\Program Files\R\R-3.6.3" #point to your R install

#setup the rinterface
import rpy2.rinterface as rinterface
rinterface.initr()

#===============================================================================
# from rpy2.robjects.packages import importr
# utils = importr('utils')
# utils.install_packages('dplyr')
#===============================================================================



#===============================================================================
# import custom modules
#===============================================================================

import seir_fix01 as seir
import setup_fix01 as setup
#from COVIDScenarioPipeline.SEIR import setup
#from COVIDScenarioPipeline.SEIR import results

class WestCoastSpatialSetup():
    """
        Setup for West Coast at the county scale.
    """
    def __init__(self):
        self.setup_name = 'utah'
        self.folder = f'data/{self.setup_name}/'

        self.data = pd.read_csv(f'{self.folder}geodata.csv')
        self.mobility = np.loadtxt(f'{self.folder}mobility.txt')
        self.popnodes = self.data['pop2010'].to_numpy()
        self.nnodes = len(self.data)

if __name__ == '__main__':          # For windows thread
    """
    call this module from command line
    
    argv[1]:    number of s imulations
    argv[2]:    scenario name (see below)
    argv[3]:    number of threads to use
    
    """



    #===========================================================================
    # execute
    #===========================================================================
    s = setup.Setup(setup_name = 'mid_utah_'+sys.argv[2],
                    spatial_setup = WestCoastSpatialSetup(),
                    nsim = int(sys.argv[1]),
                    ti = datetime.date(2020, 3, 6),
                    tf = datetime.date(2020, 10, 1),
                    interactive = False,
                    write_csv = True,
                    dt = 1/4)

    if (sys.argv[2] == 'NoNPI'):
        s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario1_None.R'
    elif (sys.argv[2] == 'SC'):
        s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario2_School_Closure.R'
    elif (sys.argv[2] == 'BI1918'):
        s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario3_Bootsma_1918Influenza.R'
    elif (sys.argv[2] == 'KansasCity'):
        s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario4_KansasCity.R'
    elif (sys.argv[2] == 'Wuhan'):
        s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario5_Wuhan.R'
    else:
        raise IOError('unrecognized value %s'%sys.argv[2])
    


    print(f">>> Starting {s.nsim} model runs on {sys.argv[3]} processes")
    print(f">>> Setup *** {s.setup_name} *** from {s.ti} to {s.tf} !")
    print(f">>> writing to folder : {s.datadir}{s.setup_name}")


    tic = time.time()
  
    res_l = seir.run_parallel(s, int(sys.argv[3]))
    print(f">>> Runs done in {time.time()-tic} seconds...")
    
    
    

