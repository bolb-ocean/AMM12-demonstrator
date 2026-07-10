# Tutorial 3: Adding new Diagnostics

This tutorial will guide you through adding new output diagnostics to your model runs. XIOS is told which output files to create and which fields to include in file_def_nemo-oce.xml; this is covered in Stage 1. XIOS is told which fields are output from NEMO and are available for file_def to call within the field_def_nemo-oce.xml file; this is covered in Stage 2. Finally the NEMO model is told which variables to output to XIOS by calling iom_put within the source code; this is covered in Stage 3. 
## Stage 1 - Creating output files for defined fields.

The simplest way to add diagnostics your output files is to call a field defined in field_def_nemo-oce in the definition of one of your output files in file_def_nemo-oce.xml. This example is covered in our [Turning tide on and off](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/tutorials/Tutorial-2.md) section.
 
You can take this further in two ways. Firstly by defining your own file:
1. First pick or create a file_group that fits your needs. An example for 10 minutes output file is provided:
```
<file_group id='oce_10mi' output_freq="10mi" output_level="10" enabled=".TRUE.">
</file_group>
```
<br> Here output_level refers to the priority of the file output with 0 (high) and 10 (low). output_freq is the frequency that the fields are saved options are "*time_unit". Where * is an integer and time_unit is one of ts (timestep), y, mo, d, h, mi, s. Note combinations can be used; output every 36h could be "1d12h" or "36h".
2. Add your file within the file_group. For the id you can use anything not currently in use. For AMM12 anything above file34 will work. For the name_suffix you can choose anything; it is useful to refer to which grid your fields are defined on. The description  is your choice and will be added to the netcdf attributes e.g.
```
<file_group id='oce_10mi' output_freq="10mi" output_level="10" enabled=".TRUE.">
  <file id='file40' name_suffix="_budget_scalar" enabled=".TRUE." />
</file_group>
```
3. Add the fields you wish to save. Refer to `field_def_nemo_oce.xml` for what is available. You can do this by adding individual fields using the "field_ref" attribute. e.g. 
```
<file_group id='oce_10mi' output_freq="10mi" output_level="10" enabled=".TRUE.">
  <file id='file40' name_suffix="_scalar" enabled=".TRUE." />
    <field field_ref="bgtemper" operation="instant" enabled=".TRUE." />
</file_group>
```
<br>You can also save a full group of files defined in field_def_nemo-oce.xml by defining a field_group and using the group_ref attribute. 
```
<file_group id='oce_10mi' output_freq="10mi" output_level="10" enabled=".TRUE.">
  <file id='file40' name_suffix="_scalar" enabled=".TRUE." />
    <field_group group_ref="scalar" operation="instant" enabled=".TRUE." />
</file_group>
```
## Stage 2 - Defining fields by calling variables

Generally the diagnostic modules (./src/OCE/DIA) in NEMO will have their output fields preconfigured within the provided field_def_nemo-oce.xml. These will activate automatically if they are used within file_def_nemo-oce.xml. For example for the diamlr.F90 module, the fields are predefined within field_def_nemo-oce.xml. This module is then activated when the fields are called within file_def_nemo.xml:
```
<file id="file40" name_suffix="_diamlr_grid_T" enabled=".TRUE." />
  <field_group id="diamlr_fields" group_ref="diamlr_fields" operation="instant" enabled=".TRUE."/>
</file_group>
```
You also can create new fields using simple expressions within field_def_nemo-oce.xml. For example the temperature-trend advection is defined as such:
```
<field id="ttrd_ad" long_name="temperature-trend: advection" standard_name="tendency_of_sea_water_temperature_due_to_advection" unit="degC/s"> sqrt( ttrd_xad^2 + ttrd_yad^2 + ttrd_zad^2 ) </field>
```
Here the variables need to already be defined within the field_def.

## Stage 3 Creating a new diagnostic in the source code

Unlike stage 1 and 2 this step would require recompilation of NEMO. Here it is useful to create a new copy to test changes.
For a simple example we will add a diagnostic for the heat content of the first 15m to the src/OCE/DIA/diahth.F90 module:
1. Here the dia_hth_htc subroutine will calculate the heatcontent:
`CALL dia_hth_htc( Kmm, 15., ts(:,:,:,jp_tem, Kmm), z2d)`
2. We can then assign it to a XIOS field of our choice, 'hc15', and send it:
`iom_put( 'hc15', rho0_rcp*z2d)`
3. Finally we can contain this within a conditional which checks if XIOS is requesting the field:
```
IF( iom_use ('hc15') ) THEN
   CALL dia_hth_htc( Kmm, 15., ts(:,:,:,jp_tem, Kmm), z2d )
   CALL iom_put( 'hc15', rho0_rcp*z2d )
ENDIF
```

After making similar code changes you will need to recompile. The new diagnostics can be saved by adding them within field_def and file_def as above.




Documentation: 
<br>[XIOS](https://www.nemo-ocean.eu/doc/node75.html)
<br>Section 12 of [NEMO manual](https://zenodo.org/records/14515373)
