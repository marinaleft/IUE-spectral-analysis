# %% [markdown]
# Libraries

# %%
from astropy.io import fits
import numpy as np
import os
from pathlib import Path

# %% [markdown]
# Filters data

# %%
cwl = [1216, 1304, 1640]
trans = [0.07, 0.07, 0.07]
fwhm = [50, 50, 50]
t=300


# %% [markdown]
# We are going to work with a list of all the .FITS paths. The following chunk creates such list.

# %%
def fits_paths(base_directory):

    paths = []

    base_directory = Path(base_directory)

    for root, _, files in os.walk(base_directory):
        for archivo in files:
            if archivo.upper().endswith(".FITS"):
                ruta_completa = Path(root) / archivo
                paths.append(ruta_completa)

    return paths

# %% [markdown]
# **Effective Area**
# 
# Now we create the effective area function using the data from the Phototek Detector and the mirror reflectivity.

# %%
MCP = np.loadtxt('../data/anaines/MCPFUV_Photek_inter.dat')         # QE
Reflect = np.loadtxt('../data/anaines/mirror_reflectivity_MCP.dat') # R

MCP_l = MCP[:, 0]  #wavelength
MCP_qe = MCP[:, 1] # QE

mirror_l = Reflect[:, 0] #wavelength
mirror_r = Reflect[:, 1] # R

l = np.arange(1150, 1760, 1) #wavelength array 1A step

lfuv = l 

mirror_r_i = np.interp(lfuv, mirror_l, mirror_r)  
MCP_qe_i = np.interp(lfuv, MCP_l, MCP_qe)

Aeff_FUV = MCP_qe_i * (mirror_r_i ** 3) * np.pi * (2.6/2)**2 

# %% [markdown]
# **Transmittance function**
# 
# We craft the gaussian profile for the filter

# %%
def generate_gauss(x, cwl, tram, fwhm):

    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    x = np.asarray(x)
    gaussiana = tram * np.exp(-((x - cwl)**2) / (2 * sigma**2))

    return gaussiana

# %% [markdown]
# For easy use, we store each gaussian information in a list

# %%
gaussians=[]
for center, tra, fw in zip(cwl, trans, fwhm):
    gauss_values = generate_gauss(lfuv, center, tra, fw)
    gaussians.append(gauss_values)

# %% [markdown]
# **Flux and error extraction from FITS files**
# 
# The following code chunk reads the fits file and takes the information from the wavelenght, flux and error columns in physical units erg/s/cm2/A

# %% 

def flux_obs(ruta):
    
    with fits.open(str(ruta)) as hdul:
        data = hdul[1].data
        lam = data['WAVELENGTH'].copy()
        flux = data['FLUX'].copy()
        err = data['SIGMA'].copy() 
        
    return lam, flux, err

# %% [markdown]
# Now we are defining a multiplication function that applies the effective area and the gaussians effect to the flux we extracted.

# %%

def multiplication(gaussians, flux_interp, Aeff_FUV):
    flux_corr=[]
    for gaussiana in gaussians:
        flux_multip = gaussiana*flux_interp*Aeff_FUV
        flux_corr.append(flux_multip)
    return flux_corr

# %% [markdown]
# Finally, we calculate the SNR integrating over the final multiplied flux

# %%
def sig_noise(flux_corr, cwl, t):
    SNR = []
    COUNT = []

    for idx, flux_array in enumerate(flux_corr):

        I = np.trapezoid(flux_array, lfuv)

        E_photon = 1.9864455e-8 / cwl[idx]
        S_i = I / E_photon
        if S_i<0:
            SNR_i = 'negative'
            count_i = "negative"
        else:
            SNR_i = int(np.sqrt(S_i * t))
            count_i = (S_i)
        SNR.append(SNR_i)
        COUNT.append(count_i)

    return SNR, COUNT

# %% [markdown]
# For later manipulation, we store the SNR data in a matrix that keeps the Image name and the SNR value for each filter, as well as the total photon count. The following code is the main loop that iterates over the full path list.

# %%
def matriz (paths):
    matrix = []

    for path in paths:
        
        lam, flux, err = flux_obs(path)
        flux_interp = np.interp(lfuv, lam, flux)

        flux_corr = multiplication(gaussians, flux_interp, Aeff_FUV)

        SNR, COUNT = sig_noise(flux_corr, cwl, t)
        subfolder = path.parent.name

        matrix.append((subfolder, SNR, COUNT))
    
    print("All .FITS files have been processed, Yay!")

    return(matrix)
