# Analysis Code for UAS OSSE Spatial Density Paper

DOI for paper: [10.1175/MWR-D-25-0175.1](https://doi.org/10.1175/MWR-D-25-0175.1)

## Organization

- `data`: Small subset of data used to create some of the figures.
- `figs`: Directory for storing figures after creation.
- `other_code`: Additional analysis code that does not create figures.
- `plot_code`: Scripts used to create figures. Note that most of the output data actually required to create these figures is not included.

### Submodules

- [metplus_OSSE_scripts](https://github.com/ShawnMurdzek-NOAA/metplus_OSSE_scripts)
- [pyDA_utils](https://github.com/ShawnMurdzek-NOAA/pyDA_utils)

## Creating Figures

*These steps assume that you are working on a Linux machine*

*Many of the plotting scripts will fail because the input data is not available*

1. Recursively clone this directory so that submodules are also cloned: `git clone --recurse-submodules https://github.com/ShawnMurdzek-NOAA/osse_uas_spatial_density_paper.git`
2. Load a Python environment. An existing Python environment you have might already work. You can also create a new environment using the `environment.yml` file included here. This can be done using conda:

```
conda env create -f python_environment.yml --prefix {ENV_PREFIX}
conda activate {ENV_PREFIX}
```

3. Run `bash make_all_plots.sh`. This script may take close to an hour to finish.
