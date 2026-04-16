# Analysis Code for UAS OSSE Spatial Density Paper

DOI for paper: [10.1175/MWR-D-25-0175.1](https://doi.org/10.1175/MWR-D-25-0175.1)

## Organization

- `data`: Small subset of data used to create figures.
- `figs`: Directory for storing figures after creation.
- `other_code`: Additional analysis code that does not create figures.
- `plot_code`: Scripts used to create figures. Note that most of the output data actually required to create these figures is not included.

## Dependencies

The Python environment used for this project is specified in the `environment.yml` file. In addition to these packages, the [pyDA_utils](https://github.com/ShawnMurdzek-NOAA/pyDA_utils) and [metplus_OSSE_scripts](https://github.com/ShawnMurdzek-NOAA/metplus_OSSE_scripts) packages must also be downloaded and added to the `PYTHONPATH` environment variable.
