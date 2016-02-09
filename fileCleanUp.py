#! /usr/bin/python
"""FILE CLEAN-UP TOOL
Logan Halstrom
CREATED:  09 FEB 2016
MODIFIED: 09 FEB 2016


DESCRIPTION:  Used to clean up numbered file series.  Delete numbered ranges
or ordered series of files.
"""

runlocal = 0
import sys
if runlocal == 1:
    sys.path.append('/Users/Logan/lib/python')
else:
    sys.path.append('/home/lhalstro/lib/python')
from lutil import cmd
from lutil import MakeOutputDir
from lutil import GetParentDir

import re
import glob
import os
import subprocess
import numpy as np


def Delete(filename):
    """Delete a given file"""
    cmd('rm {}'.format(filename))
    # cmd( 'ls {}'.format(filename) )

def DeleteIth(dir, header, i):
    """Within a loop, delete file in given directory with given header
    for given number"""
    #Create filename to delete ('header.number')
    filename = '{}.{}'.format(header, i)
    pathtodelete = '{}/{}'.format(dir, filename)
    #DELETE FILE
    if os.path.isfile(pathtodelete):
        print('Deleting: {}'.format(filename))
        Delete(pathtodelete)

def DeleteSeries(dir, header, istart, iend, incr=1):
    """Delete a series of files of given file header withing the number range
    specified.
    header --> filename header
    istart, iend --> numbers of beginning and end of series to delete
    incr --> number increment to delete within series range.  Default, delete all
    """
    todelete = np.append( np.arange(istart, iend, incr), iend )
    for i in todelete:
        DeleteIth(dir, header, i)

def DeleteExcept(dir, header, istart, iend, incr=1):
    """Within given range, delete everything EXCEPT the specified range"""
    #GIVEN INPUTS SAVE ALL FILES WITHIN RANGE
    if incr == 1:
        print('\nNO FILES WILL BE DELETED IN THIS SERIES\n')
        return
    #DELETE EVERY FILE NOT WITHIN GIVEN SERIES TO SAVE
    tosave = np.append( np.arange(istart, iend, incr), iend )
    for i in np.append( np.arange(istart, iend, 1), iend ):
        if not i in tosave:
            DeleteIth(dir, header, i)



def main(dir, headers, istart, iend, incr=1, allbut=False):

    #DELETE SERIES FOR EACH FILE HEADER
    for head in headers:
        if allbut:
            #DELETE ALL FILES WITHIN RANGE EXCEPT SPECIFIED SERIES
            DeleteExcept(dir, head, istart, iend, incr)
        else:
            #DELETE ONLY FILES IN SPECIFIED SERIES
            DeleteSeries(dir, head, istart, iend, incr)




if __name__ == "__main__":

    #RUN DIRECTORY
    dir = '/lustre2/work/lhalstro/parachuteProject/solutions/pendulum/dev1/dynamicRuns/m15/m0.15a180.0_wtt'
    # dir = '/lustre2/work/lhalstro/parachuteProject/solutions/pendulum/dev1/dynamicRuns/m15/m0.15a180.0_10deg'


    # cases = [ '1dt10sub', '2.5dt10sub', '2.5dt15sub', '2.5dt5sub', '5dt10sub']
    # cases = [4,5,6,7]
    # dir = '/lustre2/work/lhalstro/parachuteProject/solutions/pendulum/pendulum2014/pendulum_runs/timesens_4deg/m0.15a180.0_'
    # for case in cases:
    #     dir = '/lustre2/work/lhalstro/parachuteProject/solutions/pendulum/dev1/staticRuns/wakebox35deg/m0.15a1{}0.0'.format(case)
    #     # dir = dir + case

    # # dir = '/lustre2/work/lhalstro/parachuteProject/solutions/pendulum/pendulum2014/pendulum_runs/trialruns/m0.15a180.0_zeroStart'

    #SOLUTION SLICES
    headers = ['x.y0', 'q.y0', 'x.surf', 'q.surf']
    # headers = [ 'q.y0', 'q.surf']
    # headers = ['x.y0', 'q.y0', 'x.surf']
    # headers = ['x.surf','q.surf']

    #SOLUTION RESTART FILES
    headers = ['x', 'q']
    # # headers = ['q']

    #DELETE/SAVE INTERVAL
    istart = 20000
    iend = 160000
    incr = 10000

    main(dir, headers, istart, iend, incr, allbut=True)
