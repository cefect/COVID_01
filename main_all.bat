REM Setup the paths 
@ECHO off
set py_dir=C:\LS\06_SOFT\conda\miniconda3
PATH %py_dir%
PATH %PATH%;%py_dir%\DLLs
PATH %PATH%;%py_dir%\lib
PATH %PATH%;%py_dir%\lib\site-packages
PATH %PATH%;%py_dir%\lib\site-packages\win32
PATH %PATH%;%py_dir%\lib\site-packages\win32\lib
PATH %PATH%;%py_dir%\lib\site-packages\Pythonwin
PATH %PATH%;%py_dir%\Library
PATH %PATH%;%py_dir%\Library\bin
PATH %PATH%;%py_dir%\Lib\R
PATH %PATH%;%py_dir%\Lib\R\library
ECHO %PATH%

REM set R environment variables
set R_USER=MyName
set R_HOME=C:\Program Files\R\R-3.6.3


@ECHO on
REM define the simulation parameters
set sim_cnt=2

set threads=2

REM execute the script 1
set scen_nm=NoNPI
%py_dir%\python.exe main.py %sim_cnt% %scen_nm% %threads%


REM execute the script 1
set scen_nm=BI1918
%py_dir%\python.exe main.py %sim_cnt% %scen_nm% %threads%


REM execute the script 1
set scen_nm=SouthKorea
%py_dir%\python.exe main.py %sim_cnt% %scen_nm% %threads%


REM execute the script 1
set scen_nm=Reduced
%py_dir%\python.exe main.py %sim_cnt% %scen_nm% %threads%

pause

