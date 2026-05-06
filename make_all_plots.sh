#!/bin/sh

# ======================================================
# Make All Figures
#
# This script may take up to an hour to 45 min to finish
# ======================================================

# Must have the proper Python environment (from environment.yml) loaded first

date
echo

# Add root directory to PYTHONPATH
root=`pwd`
export PYTHONPATH=$PYTHONPATH:$root

# Run plotting scripts
cd plot_code
scripts=( DA_obs_error.py
          diag_ob_locs.py
          full_troposphere_verif_vprof.py
          lower_troposphere_rmse_vs_uas_number.py
          lower_troposphere_verif_vprofs_3rows.py
          lower_troposphere_verif_vprofs_no_aircft.py
          lower_troposphere_verif_vprofs_test_errors.py
          plot_hgt_agl_for_plvl.py
          plot_raw_superob_uas_vprofs.py
          plot_uas_aircft_omb.py
          plot_uas_number_vs_pressure.py
          plot_uas_sites.py
          postage_stamp_ceil_qv.py
          severe_wx_parameter_dieoff_pct.py )
for s in ${scripts[@]}; do
  echo
  echo "==================="
  echo "Running ${s}"
  python -u ${s}
done

# Run extra scripts
cd ../other_code
s=RRFS_ctrl_pct_diffs.py
echo
echo "==================="
echo "Running ${s}"
python -u ${s}

echo
echo "Done making plots"
date
