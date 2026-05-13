#!/bin/sh

# Script to extract GRIB2 output for the nature run and RRFS runs
# These data are needed to make postage stamp plots for the ceiling case study
# It is recommended to run this job in an interactive job on a compute node (it's much faster)

module load wgrib2

# Nature run
# GRIB2 codes:
#   447 : 900-hPa SPFH
#   550 : HGT of surface
#   608 : CEIL (experimental diagnostic 2)
NR_home=/work2/noaa/wrfruc/murdzek/nature_run_winter/UPP
dates=( 202202012200 202202020000 202202020200 )
echo "Extracting NR fields"
mkdir NR_output
cd NR_output
for d in ${dates[@]}; do
  cp ${NR_home}/${d::8}/wrfprs_${d}_er.grib2 wrfprs_${d}_tmp.grib2
  wgrib2 wrfprs_${d}_tmp.grib2 -match '^(447|550|608):' -grib wrfprs_${d}_er.grib2
  rm wrfprs_${d}_tmp.grib2
done
cd ..

# RRFS runs
# GRIB2 codes:
#   659 : 900-hPa SPFH
#   757 : HGT of surface
#   900 : CEIL (experimental diagnostic 2) 
echo
echo "======================"
echo "Extracting RRFS fields"
RRFS_sims=( 'winter' 'winter_uas_150km' 'winter_uas_35km' )
fhrs=( '000' '002' '004' )
for s in ${RRFS_sims[@]}; do
  echo ${s}
  mkdir ${s}
  cd ${s}
  path="/work2/noaa/wrfruc/murdzek/RRFS_OSSE/syn_data_rrfs-workflow_orion/${s}/NCO_dirs/ptmp/prod/rrfs.20220201/22"
  for f in ${fhrs[@]}; do
    file="rrfs.t22z.prslev.f${f}.conus_3km.grib2"
    cp ${path}/${file} tmp.grib2
    wgrib2 tmp.grib2 -match '^(659|757|900):' -grib ${file}
    rm tmp.grib2
  done
  cd ..
done
