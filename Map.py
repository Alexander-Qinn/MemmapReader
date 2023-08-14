#!/usr/bin/env python


################################ system lib ##########################################
import os, sys
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import datetime as dt
import pandas as pd
import numpy as np

def exact_searchsorted(a, v, sorter=None):
    " exact search of sorted array, if not found return idx=-1"
    idx = np.searchsorted(a, v, side ='left', sorter=sorter)
    idx[idx>= len(a)] = 0
    found = (a[idx] == v)
    idx[~found] = -1
    return idx
    

class Map:
    pass
        