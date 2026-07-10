#Tutorial 5: MLR tidal harmonic analysis

This guide will detail how to activate the diamlr.f90 module and use the outputs to calculate 2D tidal harmonic fields and use these for making Cotidal charts. Further details on the tidal harmonic analysis using multiple-linear-regression analysis can be found in section 12.8 of the NEMO manual.

Prerequisites:
<br>diamlr.py was tested and adjusted using:
* Python 3.12.8
* netCDF4 1.7.2

cotides_plots.py was tested and developed using:
* xarray 2025.1.2
* Python 3.10.16
* Matplotlib 3.10.0

## Step 1 - Outputing the files
The diamlr.f90 module will activate automatically provided it detects a variable used in file_def and field_def. To perform the analysis for the M2, S2, K1, O1 harmonics the following fields have been chosen within the diamlr_fields definition in [context_nemo.xml](https://github.com/bolb-ocean/AMM12-demonstrator/blob/main/cfgs_update/context_nemo.xml):
```
<field id="diamlr_r001" field_ref="diamlr_time" expr="sin( __TDE_M2_omega__ * diamlr_time )" enabled=".TRUE."  comment="harmonic:sin:M2" />
        <field id="diamlr_r002" field_ref="diamlr_time" expr="cos( __TDE_M2_omega__ * diamlr_time )" enabled=".TRUE."  comment="harmonic:cos:M2" />
        <field id="diamlr_r003" field_ref="diamlr_time" expr="sin( __TDE_K1_omega__ * diamlr_time )" enabled=".TRUE."  comment="harmonic:sin:K1" />
        <field id="diamlr_r004" field_ref="diamlr_time" expr="cos( __TDE_K1_omega__ * diamlr_time )" enabled=".TRUE."  comment="harmonic:cos:K1" />
        <field id="diamlr_r005" field_ref="diamlr_time" expr="sin( __TDE_S2_omega__ * diamlr_time )" enabled=".TRUE."  comment="harmonic:sin:S2"  />
        <field id="diamlr_r006" field_ref="diamlr_time" expr="cos( __TDE_S2_omega__ * diamlr_time )" enabled=".TRUE."  comment="harmonic:cos:S2"  />
        <field id="diamlr_r007" field_ref="diamlr_time" expr="sin( __TDE_O1_omega__ * diamlr_time )" enabled=".TRUE."  comment="harmonic:sin:O1"  />
        <field id="diamlr_r008" field_ref="diamlr_time" expr="cos( __TDE_O1_omega__ * diamlr_time )" enabled=".TRUE."  comment="harmonic:cos:O1"  />
```
Note in context_nemo.xml you will see the rest of the harmonics are disabled. By default all of the constituents NEMO can model are defined in the diamlr_fields within the file_def_nemo-oce.xml file. You can choose constituents as you wish.
Then to save as an output, the fields are called within our [file_def_nemo-oce.xml](https://github.com/bolb-ocean/AMM12-demonstrator/blob/main/cfgs_update/file_def_nemo-oce.xml):
```
<file_group id="diamlr_files" output_freq="1h" output_level="10" enabled=".TRUE.">
	<file id="file40" name_suffix="_diamlr_grid_T" enabled=".TRUE." />
	  <field_group id="diamlr_fields" group_ref="diamlr_fields" operation="instant" enabled=".TRUE." />
      </file_group> 
```
## Step 2 - Post-processing to find regression coefficients
After running AMM12 with these settings you should have output files which look like: `AMM12_1h_20120102_20120109_diamlr_coeffs_grid_*.nc`. These files need post-processing to calculate the regression coefficients which represent the complex components of our tidal constituents. Copy the [diamlr.py](https://github.com/bolb-ocean/AMM12-demonstrator/blob/main/SCRIPTS/diamlr.py) script into a directory containing your `AMM12_1h_20120102_20120109_diamlr_*.nc` files. You will need both the scalar file and at least one grid_* file. You can run the script using the following command:
```
python diamlr.py --file_scalar="AMM12_1h_20120102_20120109_diamlr_scalar.nc" --file_grid="AMM12_1h_20120102_20120109_diamlr_grid_T.nc"
```
This should output `AMM12_1h_20120102_20120109_diamlr_coeffs_grid_T.nc`.
## Step 3 - Cotidal plots
Finally we can produce the cotide_plots using [cotide_plots.py](https://github.com/bolb-ocean/AMM12-demonstrator/blob/main/SCRIPTS/cotide_plots.py). Make sure to point data_dir to a directory containing the AMM_R12_sco_domcfg.nc (or your own domain_cfg.nc if you rebuilt in tutorial 4) and `AMM12_1h_20120102_20120109_diamlr_coeffs_grid_T.nc` regression coefficients file. This script will produce a script for each of the M2, S2, K1 and O1 harmonics. You can run this with:
```
python cotide_plots.py
```
This will produce 4 plots as `*_cotide_demo.png`. By default lines of phase are every 60 degrees. Plots should look similar to this:
![Cotidal plot of modelled M2 tidal constituent. Black lines of phase in degrees, with coloured contours of amplitude in m.](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/FIGURES/M2%20cotidal%20chart.PNG)

