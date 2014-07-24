# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
""" Sensible default configuration scripts.

There are many conventions in flow cytometry regarding plotting.  This file
contains many functions that assist in setting these defaults.
"""



import numpy as np
import flowdata
from matplotlib import pylab as plt
CYTOF_LENGTH_NAMES = ['Event_length', 'Cell_length']
CYTOF_LENGTH_NAMES += [x.lower() for x in CYTOF_LENGTH_NAMES]
CYTOF_TIME_NAMES = ['time']

def default_bandwidth(channel, npoints, xmin, xmax):
    bandwidth = 0.5
    if channel.lower() in CYTOF_TIME_NAMES:
        bandwidth = (xmax - xmin)/ npoints

    if channel.lower() in CYTOF_LENGTH_NAMES:
        bandwidth = 1.

    return bandwidth


def default_scaling(channel):
    """ Return a tuple of the preferred axis scaling and transform.
    The preferred axis scaling is one of 'linear' or 'log'.
    This should refer to a valid matplotlib transform

    The transform is applied to the data before using a kernel density 
    estimator or histogram for binning.
    """

    scaling = 'log'
    transform = lambda x: np.arcsinh(x)

    if channel.lower() in [ x.lower() for x in CYTOF_LENGTH_NAMES]:
        scaling = 'linear'
        transform = lambda x: x

    return (scaling, transform)

def default_yscale(channel):
    scaling = 'log'
    if channel.lower() in ['time']:
        scaling = 'linear'
    return scaling

def bin_default(channel, xmin, xmax, bins = None):
    """Default spacing of bins given data.
    """
    if bins is None:
        bins = 100

    if channel in CYTOF_LENGTH_NAMES:
        bins = xmax - xmin

    return bins
    

def alpha(items):
    """Returns an alpha value corresponding to the number of items given.
    """
    if items == 1:
        alpha = 1
    else:
        alpha = 0.1
    return alpha

def make_list(datasets):
    """
    """

    if isinstance(datasets, flowdata.FlowCore):
        return [datasets]
    else:
        return datasets


def set_limits(data, xmin = None, xmax = None, xrange_ = None, axis = None):
    """Determine bounding range of multiple datasets
    """
    
    # First see if we have a valid xrange_ given
    try:
        xmin = xrange_[0]
        xmax = xrange_[1]
    except:
        pass

    # Otherwise, we try the keyword arguments
    if xmin is None:
        xmin = min([np.min(d) for d in data])
    if xmax is None:
        xmax = max([np.max(d) for d in data])
  
    try: 
        if axis.lower() in CYTOF_TIME_NAMES:
            xmin = 0
    except:
        pass
    return xmin, xmax


def extract_data(datasets, channels):
    datasets = make_list(datasets)
    data = []
    if isinstance(channels, str):
        channel = channels
        for ds in datasets:
            try:
                data.append(ds[channel].values)
            except KeyError:
                print('Warning, no such column name found')
        return data
    else:
        for channel in channels:
            tmp_data = []
            for ds in datasets:
                try:
                    tmp_data.append(ds[channel].values)
                except KeyError:
                    print('Warning, no such column name found')
            data.append(tmp_data)
        return data

def extract_title(datasets):
    datasets = make_list(datasets)
    try:
        titles = [ ds.title for ds in datasets]
        return titles
    except AttributeError:
        print("Does not have title attribute")

def fig_ax(axes):
    if axes is None: 
        fig, ax = plt.subplots()
    else:
        ax = axes
        fig = ax.figure
    return fig, ax