import numpy as np
from astropy.modeling import models, fitting
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS
from astropy import constants as const
from matplotlib import pyplot as plt
import seaborn as sn

class TwoGaussians(models.Gaussian1D
                   + models.Gaussian1D
                   + models.Const1D):
    """A superposition of two Gaussians plus a constant background"""

class ThreeGaussians(models.Gaussian1D
                     + models.Gaussian1D
                     + models.Gaussian1D
                     + models.Const1D):
    """A superposition of three Gaussians plus a constant"""

class FourGaussians(models.Gaussian1D
                     + models.Gaussian1D
                     + models.Gaussian1D
                     + models.Gaussian1D
                     + models.Const1D):
    """A superposition of four Gaussians plus a constant"""

class ThreeGauss_OneLorentz(models.Gaussian1D
                            + models.Gaussian1D
                            + models.Gaussian1D
                            + models.Lorentz1D
                            + models.Const1D):
    """A superposition of three Gaussians plus a Lorentzian plus constant"""

DATADIR = '/Users/will/Work/BobKPNO/KPNOsiil/'

t = Table.read(DATADIR + 'jw4.csv',
               header_start=2, format='ascii.commented_header')

fitter = fitting.LevMarLSQFitter()
# fitter = fitting.SLSQPLSQFitter()
WINDOW = [-50., 100.]


def fit_setup_3G():
    bounds = {'amplitude_0': (0.0, None),
              'amplitude_1': (0.0, None),
              'amplitude_2': (0.0, None),
              'amplitude_3': (None, None),
              'mean_0': (-10.0, 10.0),
              'mean_1': (15.0, 30.0),
              'mean_2': (20.0, 40.0),
              'stddev_0': (0.0, 5.0),
              'stddev_1': (0.0, 15.0),
              'stddev_2': (0.0, 5.0),
    }
    return ThreeGaussians(
        amplitude_0=40.0, mean_0=0.0, stddev_0=3.0,
        amplitude_1=100.0, mean_1=20.0, stddev_1=10.0,
        amplitude_2=160.0, mean_2=27.0, stddev_2=3.5,
        amplitude_3=2.0, bounds=bounds)


BOUNDS_4G = {'amplitude_0': (0.0, None),
             'amplitude_1': (0.0, None),
             'amplitude_2': (0.0, None),
             'amplitude_3': (0.0, None),
             'amplitude_4': (None, None),
             'mean_0': (-5.0, 15.0),
             'mean_1': (10.0, 27.0),
             'mean_2': (20.0, 35.0),
             'mean_3': (20.0, None),
             'stddev_0': (3.0, 8.0),
             'stddev_1': (3.0, 8.0),
             'stddev_2': (3.0, 6.5),
             'stddev_3': (6.0, 15.0),
}

BOUNDS_4G_NARROW = {'amplitude_0': (0.0, None),
                    'amplitude_1': (0.0, None),
                    'amplitude_2': (0.0, None),
                    'amplitude_3': (0.0, None),
                    'amplitude_4': (None, None),
                    'mean_0': (-5.0, 12.0),
                    'mean_1': (12.0, 27.0),
                    'mean_2': (20.0, 35.0),
                    'mean_3': (35.0, None),
                    'stddev_0': (3.0, 5.0),
                    'stddev_1': (3.0, 5.0),
                    'stddev_2': (3.0, 5.0),
                    'stddev_3': (5.0, 7.0),
}

BOUNDS_4G_MINIMAL = {'amplitude_0': (0.0, None),
'amplitude_1': (0.0, None),
                     'amplitude_2': (0.0, None),
                     'amplitude_3': (0.0, None),
                     'amplitude_4': (None, None)
}

def fit_setup_4G(bounds=BOUNDS_4G_NARROW):
    """Four Gaussian profile, hand tailored to the average profile"""
    return FourGaussians(
        amplitude_0=40.0, mean_0=4.0, stddev_0=4.0,
        amplitude_1=200.0, mean_1=20.0, stddev_1=4.0,
        amplitude_2=275.0, mean_2=27.0, stddev_2=4.0,
        amplitude_3=50.0, mean_3=38.0, stddev_3=7.0,
        amplitude_4=10.0, bounds=bounds)

def freeze_widths(model, ncomponents):
    for k in range(ncomponents):
        model[k].stddev.fixed = True

def fit_setup_4GL():
    """Using a Lorentzian for the scattered component is worse in every way"""
    bounds = {'amplitude_0': (0.0, None),
              'amplitude_1': (0.0, None),
              'amplitude_2': (0.0, None),
              'amplitude_3': (0.0, None),
              'amplitude_4': (None, None),
              'mean_0': (-10.0, 10.0),
              'mean_1': (10.0, 25.0),
              'mean_2': (20.0, 35.0),
              'x_0_3': (25.0, None),
              'stddev_0': (0.0, 5.0),
              'stddev_1': (0.0, 5.0),
              'stddev_2': (0.0, 5.0),
              'stddev_3': (0.0, 30.0),
    }
    return ThreeGauss_OneLorentz(
        amplitude_0=40.0, mean_0=4.0, stddev_0=4.0,
        amplitude_1=200.0, mean_1=20.0, stddev_1=4.0,
        amplitude_2=275.0, mean_2=27.0, stddev_2=4.0,
        amplitude_3=100.0, x_0_3=27.0, fwhm_3=20.0,
        amplitude_4=10.0, bounds=bounds)

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



# 1024, 512, 226, ..., 2, 1
binnings = 2**np.arange(10, -1, -1)


for d in t[30:31]:
    hdu, = fits.open(DATADIR + d['True File'])
    wcs = WCS(hdu.header)
    ny, nv = hdu.data.shape
    wavs = wcs.wcs.crval[0] + (np.arange(nv) + 1 - wcs.wcs.crpix[0])*wcs.wcs.cd[0,0]
    vels = const.c.to('km/s').value*(wavs - d['lamrest'])/d['lamrest'] + d['helio corr']
    i1 = (vels < WINDOW[0]).sum()
    i2 = (vels <= WINDOW[1]).sum()
    v = vels[i1:i2]
    fig, ax = plt.subplots(1, 1)
    data_line = ax.plot([], [])[0]
    fit_line = ax.plot([], [])[0]
    comp_lines = [ax.plot([], [], '--')[0] for _ in [0, 1, 2, 3]]
    ax.set_xlim(*WINDOW)

    # Initial fit parameters
    fit = fit_setup_4G()
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
            plotfile = 'FourGaussians/{}-fit-{}-{:04d}.png'.format(d['col0'], binid, j)

            # Start with parameters from coarser binning level
            fit = FourGaussians(*previous_results_table[j//2].as_void(),
                                bounds=BOUNDS_4G_NARROW)
            freeze_widths(fit, 3)  # let red component have free width
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
            'FourGaussians/{}-fit-{}.tab'.format(d['col0'], binid),
            format='ascii.tab'
        )
        previous_results_table = results_table
