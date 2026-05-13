#!/bin/sh

# Script to tar and zip MET output

# MET output is copied to this directory using Globus
# Before zipping, remove unused verification:
# */additional_2D
# */ceil
# */ceil_exp2
# */lower_atm
# */precip_radar
# */RHobT
# */sfc
# */upper_air
# */upper_air_below_sfc_mask [EXCEPT ctrl, uas_150km, and uas_35km for both seasons]
# */make_submit_metplus_jobs_lower_atm.sh 
# */make_submit_metplus_jobs.sh_OLD 

sims=( spring
       spring_no_aircft
       spring_uas_100km
       spring_uas_150km
       spring_uas_300km
       spring_uas_35km
       spring_uas_35km_add_typ133_DAerr
       spring_uas_35km_autocorr0.95
       spring_uas_35km_autocorr0.985
       spring_uas_35km_no_aircft
       spring_uas_35km_reduce_RHoe
       spring_uas_75km
       winter
       winter_uas_100km
       winter_uas_150km
       winter_uas_35km
       winter_uas_75km )

mkdir MET_output_zipped
cd MET_output_unzipped_ORIGINAL
for s in ${sims[@]}; do
  tar cvzf ${s}.tar.gz ./${s}
  mv ${s}.tar.gz ../MET_output_zipped/
done
cd ..
