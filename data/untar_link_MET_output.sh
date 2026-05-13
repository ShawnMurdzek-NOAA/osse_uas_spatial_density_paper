#!/bin/sh

# Script to untar and unzip MET output, then link output into proper directory structure

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

# Untar and unzip
mkdir MET_output_unzipped
cd MET_output_zipped
for s in ${sims[@]}; do
  tar xvzf ${s}.tar.gz ./${s}
  mv ${s} ../MET_output_unzipped/
done
cd ..

# Perform linking
echo
verif_types=( "lower_atm_below_sfc_mask" "upper_air_below_sfc_mask" "severe_wx_env" )
cd MET_output_unzipped
home=`pwd`
for vD in ${sims[@]}; do
  echo "Performing linking for ${vD}"
  for v in ${verif_types[@]}; do
    if [[ -d ${home}/${vD}/${v} ]]; then
      out_dir=${home}/${vD}/${v}/output/GridStat
      mkdir -p ${out_dir}
      all_dir=(${home}/${vD}/${v}/2*)
      for d in ${all_dir[@]}; do
        all_subdir=(${d}/output/GridStat/2*)
        for sd in ${all_subdir[@]}; do
          if [[ -d ${sd} ]]; then
            cd ${sd}
            files=(./grid*)
            for f in ${files[@]}; do
              ln -sf ${sd}/${f} ${out_dir}/${f}
            done
          fi
        done
      done
    fi
  done
done
