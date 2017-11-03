import numpy as np
from astropy.modeling import models, fitting
from astropy.table import Table
from astropy.io import fits
from astropy import constants as const
from matplotlib import pyplot as plt
import seaborn as sn

class ThreeGaussians(models.Gaussian1D
                     + models.Gaussian1D
                     + models.Gaussian1D
                     + models.Const1D):
    """A superposition of three Gaussians plus a constant"""

DATADIR = '/Users/will/Work/BobKPNO/DOHoiii/'

t = Table.read(DATADIR + 'th1c.csv',
               header_start=2, format='ascii.commented_header')
WINDOW = [-50., 100.]
NGAUSS = 3

# Set up dict of arrays to receive the statistics maps
output_shape = 514, len(t)
castaneda_components = 'BAC'    # A is the middle one
mapvars = [
    'mean fit err', 'max fit err',
    'sigma(obs)', 'vmean(obs)', 'flux(obs)',
    'sigma(fit)', 'vmean(fit)',
    'sigma(AB)', 'vmean(AB)',
    'sigma(A)', 'vmean(A)', 'flux(A)',
    'sigma(B)', 'vmean(B)', 'flux(B)',
    'sigma(C)', 'vmean(C)', 'flux(C)',
]
maps = {k: np.empty(output_shape) for k in mapvars}

def find_mean_std(x, y):
    """Find mean and stddev of y(x)"""
    if y.sum() <= 0.0:
        xm, xvar = np.nan, np.nan
    else:
        xm = np.average(x, weights=y)
        xvar = np.average((x-xm)**2, weights=y)
    return xm, np.sqrt(xvar)

def sanitize(s):
    return s.replace(' ', '_').replace('(', '_').replace(')', '')

def save_map_as_fits(label, data):
    fits.PrimaryHDU(data=data).writeto(
        'oiii-3G-' + sanitize(label) + '.fits',
        clobber=True
    )

# Loop over slits
for i, d in enumerate(t):
    # Get fits data of PV image
    hdu, = fits.open(DATADIR + d['True File'])
    ny, nv = hdu.data.shape
    # set up windowed velocity array
    wavs = d['lam0'] + (np.arange(nv) + 1)*d['lamscale']
    vels = const.c.to('km/s').value*(wavs - d['lamrest'])/d['lamrest']
    vels += d['helio corr'] + d['ufiddle']
    k1 = (vels < WINDOW[0]).sum()
    k2 = (vels <= WINDOW[1]).sum()
    v = vels[k1:k2]
    fit_tab = Table.read(
        'ThreeGaussians/{}-fit-bin0001.tab'.format(d['col0']),
        format='ascii.tab')
    assert len(fit_tab) == ny
    # loop over pixels along slit
    for j, (profile, fitpars) in enumerate(zip(hdu.data, fit_tab)):
        f = profile[k1:k2]
        fit = ThreeGaussians(*fitpars.as_void())
        # Absolute fractional deviation of fit (normalized by peak value)
        err_fit = np.abs(f - fit(v))/f.max()

        # Stats for observed line
        (maps['vmean(obs)'][j, i],
         maps['sigma(obs)'][j, i]) =  find_mean_std(v, f)
        maps['flux(obs)'][j, i] = f.sum()
        # Stats for full fitted line
        (maps['vmean(fit)'][j, i],
         maps['sigma(fit)'][j, i]) =  find_mean_std(v, fit(v))
        # Stats for core (A+B components)
        (maps['vmean(AB)'][j, i],
         maps['sigma(AB)'][j, i]) =  find_mean_std(v, fit[0:2](v))
        # Stats for each component separately
        for m, ABC in enumerate(castaneda_components):
            (maps['vmean('+ABC+')'][j, i],
             maps['sigma('+ABC+')'][j, i]) =  find_mean_std(v, fit[m](v))
            maps['flux('+ABC+')'][j, i] = np.sum(fit[m](v))

        maps['mean fit err'][j, i] = np.mean(err_fit)
        maps['max fit err'][j, i] = np.max(err_fit)

# Save all the maps as FITS images
for _ in maps:
    save_map_as_fits(_, maps[_])
