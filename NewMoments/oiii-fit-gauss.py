import numpy as np
from astropy.modeling import models, fitting
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS
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

fitter = fitting.LevMarLSQFitter()
# fitter = fitting.SLSQPLSQFitter()
WINDOW = [-50., 100.]

BOUNDS_3G_NARROW = {'amplitude_0': (0.0, None),
                    'amplitude_1': (0.0, None),
                    'amplitude_2': (0.0, None),
                    'amplitude_3': (None, None),
                    'mean_0': (0.0, 20.0),
                    'mean_1': (15.0, 35.0),
                    'mean_2': (15.0, 40.0),
                    'stddev_0': (3.0, 8.0),
                    'stddev_1': (3.0, 8.0),
                    'stddev_2': (8.0, 18.0),
}

def fit_setup_3G(bounds=BOUNDS_3G_NARROW):
    return ThreeGaussians(
        amplitude_0=1000.0, mean_0=15.0, stddev_0=5.,
        amplitude_1=2000.0, mean_1=23.0, stddev_1=5.,
        amplitude_2=300.0, mean_2=35.0, stddev_2=14.0,
        amplitude_3=10.0, bounds=bounds)


def freeze_widths(model, ncomponents):
    for k in range(ncomponents):
        model[k].stddev.fixed = True

def mean_n_rows(a, n):
    """Take mean of each chunk of `n` rows of array `a`

Return new array of shape (nrows/n, ncols)

    """
    nrows, _ = a.shape
    nchunks = nrows//n
    # Use array_split instead of vsplit so that it doesn't matter if n
    # doesn't divide nrows exactly
    return np.vstack(np.mean(chunk, axis=0)
                     for chunk in np.array_split(a, nchunks, axis=0))



# 512, 226, ..., 2, 1
binnings = 2**np.arange(9, -1, -1)
ngauss = 3

for d in t:
    hdu, = fits.open(DATADIR + d['True File'])
    wcs = WCS(hdu.header)
    ny, nv = hdu.data.shape
    wavs = d['lam0'] + (np.arange(nv) + 1)*d['lamscale']
    vels = const.c.to('km/s').value*(wavs - d['lamrest'])/d['lamrest']
    # Alternatively, get vels directly from the WCS 
    vels2 = wcs.wcs.crval[0] + (np.arange(nv) + 1
                                - wcs.wcs.crpix[0])*wcs.wcs.get_cdelt()[0]
    assert np.allclose(vels, vels2)
    vels += d['helio corr'] + d['ufiddle']
    i1 = (vels < WINDOW[0]).sum()
    i2 = (vels <= WINDOW[1]).sum()
    v = vels[i1:i2]
    fig, ax = plt.subplots(1, 1)
    data_line = ax.plot([], [])[0]
    fit_line = ax.plot([], [])[0]
    comp_lines = [ax.plot([], [], '--')[0] for _ in range(ngauss)]
    ax.set_xlim(*WINDOW)

    # Initial fit parameters
    fit = fit_setup_3G()
    previous_results_table = Table(names=fit.param_names)
    previous_results_table.add_row(fit.parameters)

    # Loop over binnings starting with the coarsest scale
    for nbin in binnings:
        binid = 'bin{:04d}'.format(nbin)

        results_table = Table(names=fit.param_names)

        for j, profile in enumerate(mean_n_rows(hdu.data, nbin)):
            print(binid, j)
            f = profile[i1:i2]
            ax.set_ylim(-0.1*f.max(), 1.1*f.max())
            plotfile = 'ThreeGaussians/{}-fit-{}-{:04d}.png'.format(d['col0'], binid, j)

            # Start with parameters from coarser binning level
            jprevious = min(j//2, len(previous_results_table) - 1)
            fit = ThreeGaussians(*previous_results_table[jprevious].as_void(), bounds=BOUNDS_3G_NARROW)
            #freeze_widths(fit, 2)  # let red component width vary
            freeze_widths(fit, 3)  # freeze red component too
            # Rescale so total flux is correct
            scale = f.sum()/fit(v).sum()
            for k in range(4):
                fit[k].amplitude *= scale
            # Perform the fitting
            fit = fitter(fit, v, f, acc=1e-5, maxiter=500)
            results_table.add_row(fit.parameters)
            data_line.set_data(v, f)
            fit_line.set_data(v, fit(v))
            for ii, comp_line in enumerate(comp_lines):
                comp_line.set_data(v, fit[ii](v))
            fig.savefig(plotfile)

        results_table.write(
            'ThreeGaussians/{}-fit-{}.tab'.format(d['col0'], binid),
            format='ascii.tab'
        )
        previous_results_table = results_table
