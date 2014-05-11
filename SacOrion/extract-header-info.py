
from astropy.io import fits
from astropy.table import Table
from pathlib import Path

datadir = Path("/Users/will/Work/BobKPNO/TereFigs/slitdata/")

lines = {
    "H-alpha-6563": "ha",
    "S-II-6716": "siis",
    "S-II-6731": "siil",
    "S-III-6312": "siii",
    "O-I-6300": "oi",
    "N-II-6583": "nii",
    "O-III-5007": "oiii",
}
column_names = [
    "Filename", "x", "y0", "dy", "ny", "v0", "dv", "nv",
]
column_dtypes = {
    # Override default "float" for these columns
    "Filename": "<U25", "ny": int, "nv": int,
}


for longprefix, prefix in lines.items():
    table = Table(names=column_names, 
                  dtypes=[column_dtypes.get(name, float) for name in column_names])
    print(longprefix)
    for filepath in datadir.glob(prefix + "0*wcsb.fits"):
        hdu = fits.open(str(filepath))[0]
        rowdata = {
            "Filename": filepath.name,
            "x": float(filepath.stem[len(prefix)+3:-4]),
            "y0": hdu.header["CRVAL2"] + (1 - hdu.header["CRPIX2"])*hdu.header["CD2_2"],
            "dy": hdu.header["CD2_2"],
            "ny": hdu.header["NAXIS2"],
            "v0": hdu.header["CRVAL1"] + (1 - hdu.header["CRPIX1"])*hdu.header["CD1_1"],
            "dv": hdu.header["CD1_1"],
            "nv": hdu.header["NAXIS1"],
        }
        table.add_row(rowdata) 
    table.write(longprefix + ".tab", format='ascii.tab')
    table.write(longprefix + ".dat", format='ascii.fixed_width', delimiter=' ')
