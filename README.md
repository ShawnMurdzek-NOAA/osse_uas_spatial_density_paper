# Analysis Code for UAS OSSE Spatial Density Paper

DOI for paper: [10.1175/MWR-D-25-0175.1](https://doi.org/10.1175/MWR-D-25-0175.1)

## Organization

- `data`: Subset of data used to create most of the figures.
- `figs`: Directory for storing figures after creation.
- `other_code`: Additional analysis code that does not create figures.
- `plot_code`: Scripts used to create figures. Note that most of the output data actually required to create these figures is not included.

### Submodules

- [metplus_OSSE_scripts](https://github.com/ShawnMurdzek-NOAA/metplus_OSSE_scripts)
- [pyDA_utils](https://github.com/ShawnMurdzek-NOAA/pyDA_utils)

## Creating Figures

*These steps assume that you are working on a Linux machine*

*It is expected that the diag_ob_locs.py script will fail because input data is not included here*

1. Recursively clone this directory so that submodules are also cloned:

```
git clone --recurse-submodules https://github.com/ShawnMurdzek-NOAA/osse_uas_spatial_density_paper.git
cd osse_uas_spatial_density_paper
```

2. Load a Python environment. An existing Python environment you have might already work. You can also create a new environment using the `python-environment.yml` file included here. If creating a new Python environment and using HPC, you probably want to install the new environment in your scratch or work space rather than your home space owing to the small storage quotas in home. Installing a new Python environment can be done using conda:

```
conda env create -f python-environment.yml --prefix {ENV_PREFIX}   # ENV_PREFIX is where the environment will be installed
conda activate {ENV_PREFIX}
```

3. Untar and unzip the required data:

```
cd data
bash untar_link_MET_output.sh
cd UAS_obs
tar xvzf uas_obs.tar.gz
cd ../../
```

4. Create plots. Script may take half an hour or more to finish.

```
bash make_all_plots.sh
```
