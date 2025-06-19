#!/bin/bash

# Input and output filenames
INPUT="domain_cfg.nc"
OUTPUT="coordinates_BMG.nc"
OUTPUT_BATHY="bathy_BMG.nc"
TMP1="tmp1.nc"
TMP2="tmp2.nc"

# 1. Select only matching variables (as in coordinates_eNEATL36)
ncks -O -v nav_lon,nav_lat,nav_lev,time_counter,glamt,glamu,glamv,glamf,gphit,gphiu,gphiv,gphif,e1t,e1u,e1v,e1f,e2t,e2u,e2v,e2f,ff_t $INPUT $TMP1

# 2. Rename ff_t → ff (to match first file)
ncrename -O -v ff_t,ff $TMP1 $TMP1

# 3. Clean global attributes
ncatted -O -a DOMAIN_number,global,d,, $TMP1                     
ncatted -O  -a DOMAIN_number_total,global,d,, $TMP1 
ncatted -O  -a DOMAIN_dimensions_ids,global,d,, $TMP1
ncatted -O  -a DOMAIN_size_global,global,d,, $TMP1
ncatted -O  -a DOMAIN_size_local,global,d,, $TMP1
ncatted -O  -a DOMAIN_position_first,global,d,, $TMP1
ncatted -O  -a DOMAIN_position_last,global,d,, $TMP1
ncatted -O  -a DOMAIN_halo_size_start,global,d,, $TMP1
ncatted -O  -a DOMAIN_halo_size_end,global,d,, $TMP1
ncatted -O  -a DOMAIN_type,global,d,, $TMP1

# 4. Add required global attributes for output
ncatted -O -a file_name,global,o,c,"mesh_hgr.nc" $TMP1
ncatted -O -a TimeStamp,global,o,c,"$(date '+%d/%m/%Y %H:%M:%S %z')" $TMP1
ncatted -O -a history,global,o,c,"Converted from domain_cfg.nc on $(date)" $TMP1
ncatted -O -a NCO,global,o,c,"$(ncks --version | head -n 1)" $TMP1

# 5. Save final result
mv $TMP1 $OUTPUT

# Clean up temporary files
rm -f $TMP2
echo "✅ Output written to $OUTPUT"


# Now, make the bathymetry file
cp $INPUT tmp.nc
ncks -v glamt $INPUT glamt
ncks -v gphit $INPUT gphit
ncks -v bathy_metry $INPUT tmp.nc
ncks -A glamt tmp.nc
ncks -A gphit tmp.nc
ncrename -d time_counter,t tmp.nc
ncrename -v bathy_metry,Bathymetry tmp.nc
ncap2 -O -s 'Bathymetry=float(Bathymetry)' tmp.nc tmp2.nc
mv tmp2.nc tmp.nc
ncks -C -O -x -v x,y tmp.nc tmp2.nc 
mv tmp2.nc tmp.nc
ncks -3 tmp.nc tmp2.nc 
mv tmp2.nc $OUTPUT_BATHY
rm tmp.nc glamt gphit
































