REM Setup the paths 
set py_dir=C:\LS\06_SOFT\conda\miniconda3\
PATH %py_dir%
PATH %PATH%;%py_dir%\DLLs
PATH %PATH%;%py_dir%\lib
PATH %PATH%;%py_dir%\site-packages
PATH %PATH%;%py_dir%\site-packages\win32
PATH %PATH%;%py_dir%\site-packages\win32\lib
PATH %PATH%;%py_dir%\site-packages\Pythonwin
PATH %PATH%;%py_dir%\Library
PATH %PATH%;%py_dir%\Library\bin
PATH %PATH%;%py_dir%\Lib\R
PATH %PATH%;%py_dir%\Lib\R\library
ECHO %PATH%


REM define the simulation parameters
set sim_cnt=100
set scen_nm=NoNPI
set threads=4

REM execute the script
%py_dir%\python.exe main.py %sim_cnt% %scen_nm% %threads%

pause

