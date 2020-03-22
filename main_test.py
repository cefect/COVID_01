#===============================================================================
# test dependencies
#===============================================================================


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
#import matplotlib.pyplot as plt

#===============================================================================
# setup R
#===============================================================================

import os
os.environ["R_USER"] = "R_USER"
#os.environ["R_HOME"] = r"C:\Program Files\R\R-3.6.3" #point to your R install

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

    #===========================================================================
    # test pars
    #===========================================================================
    pars = {
        1: 2, #number of s imulations
        2: 'NoNPI',
        3: 2, #number of threadas
        }
    
    scen_dir = r'C:\LS\03_TOOLS\_git\COVID_01\scenarios'
    
    
    
    #===========================================================================
    # execute
    #===========================================================================
    s = setup.Setup(setup_name = 'mid_utah_'+pars[2],
                    spatial_setup = WestCoastSpatialSetup(),
                    nsim = int(pars[1]),
                    ti = datetime.date(2020, 3, 6),
                    tf = datetime.date(2020, 10, 1),
                    interactive = False,
                    write_csv = True,
                    dt = 1/4)
    
    
    scen_d = {
        'NoNPI':'NPI_Scenario1_None.R',
        'BI1918':'NPI_Scenario2_Bootsma_1918Influenza.R',
        'SouthKorea':'NPI_Scenario3_SouthKorea.R',
        'ReducedGamma':'NPI_Scenario4_ReducedGamma.R',       
        }
    
    




    #===========================================================================
    # if (pars[2] == 'NoNPI'):
    #     s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario1_None.R'
    # if (pars[2] == 'SC'):
    #     s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario2_School_Closure.R'
    # if (pars[2] == 'BI1918'):
    #     s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario3_Bootsma_1918Influenza.R'
    # if (pars[2] == 'KansasCity'):
    #     s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario4_KansasCity.R'
    # if (pars[2] == 'Wuhan'):
    #     s.script_npi = 'COVIDScenarioPipeline/data/NPI_Scenario5_Wuhan.R'
    #===========================================================================
    
    #s.script_import = 'COVIDScenarioPipeline/R/distribute_airport_importations_to_counties.R'

    #s.set_filter(np.loadtxt('data/west-coast-AZ-NV/filtergithub.txt'))
    print()
    print()
    print(f">>> Starting {s.nsim} model runs on {pars[3]} processes")
    print(f">>> Setup *** {s.setup_name} *** from {s.ti} to {s.tf} !")
    print(f">>> writing to folder : {s.datadir}{s.setup_name}")
    print()
    print()
    
    tic = time.time()
  
    res_l = seir.run_parallel(s, int(pars[3]))
    print(f">>> Runs done in {time.time()-tic} seconds...")
    

