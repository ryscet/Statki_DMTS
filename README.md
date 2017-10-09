#Gabors psychophysics experiment
Investigate whether eeg activity determines probabillity of stimulus detection

* Find the 77% accuracy threshold using a staircase procedure
* Present threshold, identical and easily detectable stimuli while recording eeg



#TO PREPARE THE ENVIRONMENT (tested on mac)
--> Install conda and make a virtual environment with python 2.7 >> conda create -n <name_of_virtual_env> python=2.7
--> Install dependencies (with conda install) (matplotlib, scipy, numpy, pandas)
--> install psychopy from conda cloud >> conda install -n <name_of_virtual_env> -c cogsci psychopy=1.82.01
(withoout virtual env >> conda install -c cogsci psychopy=1.82.01)
--> activate the virtual env and when inside, install pygame >> pip install pygame
DONE






TO RUN:
>> python2 gabors_exp.py


Note: experiment scripts work from conda installation (python2.7 windows 64 bit). Only add psychopy (https://anaconda.org/cogsci/psychopy) and perhaps some forgotten packages to run (pyglet, pillow, ..?).

!!NOTE!!: Port test moved to another folder

LPT controller (port_test.py) work from IDLE python2.7 installation on windows with additional psychopy from pip install. Anaconda psychopy does something funny to parallel port libraries. 

A few of steps to get port_test working:

install dependencies for psychopy (scipy) on windows from special windows wheels: 

	http://www.lfd.uci.edu/~gohlke/pythonlibs/

install wxPython (with correct path) from:

	https://wxpython.org/download.php

make sure install finishes without error, might have to unclick some options on install finish.

Install other libraries that psychopy requires using pip. These didn't pose any problems with the pip install as long as:

- scipy is installed from the special windows wheel
- pip is pointing to the IDLE python, not anaconda >> python2 -m pip install <package>
- python2 command becomes accessible after renaming python.exe to python2.exe in the IDLE installation dir. Anaconda takes over python command.

*There might be some other screwy things I forgot and this might get outdated pretty soon. Psychopy on windows with parallel ports is worse then 80s gentle rap.