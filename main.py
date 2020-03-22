"""
call this module from command line

main runner for Utah SEIR model

"""




#==============================================================================
# dependency check
#==============================================================================
# Let users know if they're missing any of our hard dependencies
hard_dependencies = ('pandas', 'numpy','seaborn','geopy','tqdm', 'geopandas','shapely','numba','rpy2')
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

"""supress FutureWarning: from_items is deprecated"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


import pandas as pd
import datetime, time, multiprocessing, itertools, sys, os
#import matplotlib.pyplot as plt

#===============================================================================
# setup R
#===============================================================================



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
        
        
        
def run(pars, #parameter files
        #directory of scenario files
        scen_dir = r'C:\LS\03_TOOLS\_git\COVID_01\scenarios',
        
        #map to scenario files
        scen_d = {
        'NoNPI':'NPI_Scenario1_None.R',
        'BI1918':'NPI_Scenario2_Bootsma_1918Influenza.R',
        'SouthKorea':'NPI_Scenario3_SouthKorea.R',
        'Reduced':'NPI_Scenario4_ReducedGamma.R',       
        }
        ):
    
    """
    convience fucntion for running simulations
    
        
    
    argv[1]:    number of s imulations
    argv[2]:    scenario name (see below)
    argv[3]:    number of threads to use
    
    
    """
    
    
    
    #===========================================================================
    # precheck 
    #===========================================================================
    assert len(pars)==4, 'unexpected inputs count'
    print('pars: \n%s'%pars)
    
    #check the R Environment variables
    assert 'R_USER' in os.environ
    assert 'R_HOME' in os.environ
    
    #print('R_USER=%s \nR_HOME=%s'%(os.getenv('R_USER'), os.getenv('R_HOME')))

    
    
    
    
    #===========================================================================
    # setup
    #===========================================================================
    s = setup.Setup(setup_name = 'mid_utah_'+pars[2],
                    spatial_setup = WestCoastSpatialSetup(),
                    nsim = int(pars[1]),
                    ti = datetime.date(2020, 3, 6),
                    tf = datetime.date(2020, 10, 1),
                    interactive = False,
                    write_csv = True,
                    dt = 1/4)
    
    #===========================================================================
    # set the scenario parmaters
    #===========================================================================

    
    
    assert pars[2] in scen_d, 'unrecognized scenario: %s'%pars[2]
    
    rfp = os.path.join(scen_dir, scen_d[pars[2]])
    assert os.path.exists(rfp)
    
    s.script_npi = rfp
    
    print('set script_npi=%s'%s.script_npi)

    #===========================================================================
    # execute
    #===========================================================================

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
    
    

if __name__ == '__main__':          # For windows thread
    

    

    
    if len(sys.argv)<=1:
        
        import os
        #setup the R environment
        os.environ["R_USER"] = "R_USER"
        os.environ["R_HOME"] = r"C:\Program Files\R\R-3.6.3" #point to your R install
        
        
        for indxr, sname in enumerate([
            'NoNPI', 
            #'SouthKorea',  
            #'Reduced', 
            #'BI1918'
            ]):
            print('\n \nrun %i: %s \n \n'%(indxr, sname))
            
            try:
                run({
                0:'placeholder',
                1: 10000, #number of s imulations
                2: sname,
                3: 5, #number of threadas
                })
            except Exception as e:
                print('FAILED on %s w/ \n%s'%(sname, e))
    else:
        

        print('called w/ %i args: \n%s'%(len(sys.argv), sys.argv))
        
        assert len(sys.argv) >2, 'failed to call w/ enough arguments'
    
        run(sys.argv)
        
    print('finished')


    
    
    

