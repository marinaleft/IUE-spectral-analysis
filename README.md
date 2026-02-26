# IUE Spectral Analysis and SNR processing for the OUL mission

This project provides an automated pipeline for processing and analyzing International Ultraviolet Explorer (IUE) satellite data, specifically tailored for the **Lunar Ultraviolet Observatory (OUL)** mission. It handles signal-to-noise ratio (SNR) calculations, photon counts, and statistical validation for stellar variability studies.

## Scientific Context: The OUL Mission

The **OUL (Observatorio Ultravioleta Lunar)** is a compact spaceborne instrument designed for a lunar polar orbit. Its primary goal is to study Earth's exosphere and magnetosphere response to solar activity by monitoring Lyman-alpha ($Ly_{\alpha}$) emissions.

Beyond Earth studies, this project supports the OUL's high-sensitivity research on:
* **Massive Star Variability:** Specifically O, B, and A-type stars.
* **Stellar Populations:** Developing a robust classification framework based on temporal flux characteristics in the Far-UV (115 nm - 195 nm).

## Overview 

The tool leverages legacy data from the **INES (IUE Newly Extracted Spectra)** archive—which contains over 110,000 spectra—to identify viable candidates for the OUL mission. It automates the download of `.FITS` files and processes them through a simulated optical pipeline based on the **WALRUS** (Wide Angle Large Reflective Unobscured System) three-mirror design.

### Key Features

* **Automated Data Acquisition:** Module to download `.FITS` files directly from the INES database using an iterative URL system based on a custom `catalog.xlsx`.
* **Flexible Data Input:** Supports both automated downloads and manual local setup (users can simply extract the provided `.zip` file in the `data/` folder).
* **Physics-Based Simulation:** 
    * Models the photometric response using **Gaussian distribution** filters ($Ly_{\alpha}$, OI, He II).
    * Calculates the **Effective Area ($A_{eff}$)** by combining the Quantum Efficiency ($QE$) of the Photek MCP340 detector and cumulative reflectivity ($R^3$).

* **Statistical Reporting:** Generates multi-sheet Excel reports including mean photon counts and standard deviations per object to assess signal quality and variability.

## Project Structure
* **`scripts/`**: Contains Jupyter Notebooks for data processing (creating an excel file with stats and raw values) and `.FITS` downloading. It contains a `.py` script for the SNR and photons count extraction form the fits. These are different files in the `scripts/` folder. 

  This folder also contains the file `catalog.xlsx` which is the list of the Images and stellar sources to process.
* **`data/`**: Input files such as the one needed for the quantum efficiency or the reflectivity of the detector.

  `data/processed/` contains the obtained excel files.

## Installation and Set Up

To run this project, you need Python 3.x

1. **Clone the repository**
   ```bash
   git clone [https://github.com/marinaleft/IUE-spectral-analysis.git](https://github.com/marinaleft/IUE-spectral-analysis.git)
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Data Preparation**
   * Option A (manual): Extract the provided `.zip` file into the `data/` folder.
   * Option B (code): Run the download notebook (ensure you have an internet connection to reach the INES database). This option may take more than one hour.