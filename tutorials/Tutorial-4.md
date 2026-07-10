#Tutorial 4: Create domain configuration files and update the bathymetry

This tutorial aim at providing guidelines to update the bathymetry of a NEMO regional configuration from scratch. In particular, it details how to create a domain configuration file from an external bathymetry, and gives insights on how to update the bathymetry at coastlines and provides link to tutorials to create boundary & initial conditions afterwards. Note that this tutorial use the AMM12 configuration, but can be applied to any other configuration.

## Step 1: Download an external bathymetry file

The first thing to do is to download an external bathymetry file in netcdf format. Here is some links to external bathymetry sources:
* The GEBCO bathymetry: https://www.gebco.net/data-products/gridded-bathymetry-data
* The EMODNET bathymetry: https://emodnet.ec.europa.eu/en

In this tutorial, we use a GEBCO_2020 file, but the steps are the same for any bathymetry dataset.


> _Note that the EMODNET bathymetry is distributed in tiles, you will need to merge the tiles beforehand, NEMO requires an unique netcdf file for the bathymetry input. To do this, you can follow the steps decribed in sec.1 [here](https://github.com/immerse-project/eNEATL36-BIzoo_Demonstator/wiki/1.-Create-the-input-mesh-files-(for-both-parent-&-child-domains))_.



## Step 2: Compile the DOMAINcfg tool

The first step is to compile the DOMAINcfg NEMO tool. Follow the steps in the [NEMO user guide](https://sites.nemo-ocean.io/user-guide/tools.html) to compile the tool.

## Step 3: create the domain configuration file

To run, the NEMO model needs a domain configuration file, the domain_cfg file, which contains the horizontal and vertical grid structure, land-sea mask, bathymetry, scale factors, and other static information needed to define the model's spatial configuration. The file is provided within the [AMM12 configuration input files](https://gws-access.jasmin.ac.uk/public/nemo/sette_inputs/), but is based on an outdated bathymetry. Thus, this tutorial will explain how to compute a domain configuration file from an external bathymetry.

The DOMAINcfg tool is designed to create the domain_cfg file. First, link the tool into your working directory, 

``` 
cd YOUR_WORKING_DIR
ln -fs {NEMO_DIR}/tools/DOMAINcfg/make_domain_cfg.exe .
```
Then, retrieve the domain_cfg namelist example [here](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/NAMELISTS/namelist_cfg_domcfg_AMM12_from_GEBCO) and put it into your working directory. Depending on the bathymetry you use, you will have to change the name of the bathymetry file, and the name of the bathymetry, latitude and longitude variables at the lines:

```
   nn_bathy    =    2      ! = 0 compute analyticaly
                           ! = 1 read the bathymetry file
                           ! = 2 compute from external bathymetry
                           ! = 3 compute from parent (if "key_agrif")

   cn_topo     =  'YOURFILENAME.nc'             ! external topo file (nn_bathy =1)
   cn_bath     =  'BATHY_NAME'                 ! topo name in file  (nn_bathy =1)
   cn_lon      =  'LON_NAME'                    ! lon  name in file  (nn_bathy =1)
   cn_lat      =  'LAT_NAME'                    ! lat  name in file  (nn_bathy =1)
```
Then, launch the domain_cfg tool:

``` 
./make_domain_cfg.exe 
```

At this step, you should have as output a new domain_cfg.nc file, with the GEBCO bathymetry. You can use the python scripts [plot_bathy.py](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/SCRIPTS/BATHYMETRY_TOOLS/plot_bathy.py) and [plot_bathy_diff.py](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/SCRIPTS/BATHYMETRY_TOOLS/plot_bathy_diff.py) to plot the new bathymetry and the differences with AMM12 previous bathymetry as in Figure 1.

<p align="center" width="100%">
    <img src="https://github.com/bolb-ocean/AMM12-hackathon/blob/main/FIGURES/Figure_bathy_GEBCO.png">
</p>
<p align="center" width="100%">
    <em>Figure 1: (Top) GEBCO bathymetry interpolated on domain_cfg and (bottom) differences between GEBCO and previous AMM12 bathymetry</em>
</p>

> **Troubleshooting notes:**
> * _With the version of nemo 5.0.1, the domain_cfg tool crashes if you use a regional bathymetry file (=> that does not covers the whole globe). If so, update the domhgr.f90 file in the DOMAINcfg/src/ folder with the updated domhgr.f90 file [here](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/SRC/domhgr.F90) and recompile the DOMAINcfg tool._
> * _Make sure that the bathymetry in the external bathymetry file is positive, that the longitude has no negative values (i.e: from 0 to 360) and that the bathymetry = 0 over land._
 
## Step 5: Updating the bathymetry with BMGtool

Usually, bathymetry datasets are defined on the lowest tide point, which means that area that undergo tidal immersion cycles are considered as land points. Thus, mismatches with the coastlines can occur. In order to refine the coaslines, you can download the BMG tool from IFREMER (https://mars3d.ifremer.fr/Les-outils/BathyMeshGridTOOLS) which is very useful to refine the bathymetry.

> _Note: BMGtools was develloped for previous NEMO versions (<= 3.6), but we included a script [here](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/SCRIPTS/BATHYMETRY_TOOLS/create_coords_and_bathy_BMG.sh) to create a coordinates_BMG.nc and a bathy_BMG.nc compatible with BMG from the NEMO5. domain_cfg file (check the file names within the script)._

``` 
chmod +x create_coords_and_bathy_BMG.sh
./create_coords_and_bathy_BMG.sh
``` 
Then, go to the BMGtools folder, and launch BMGtools:

``` 
./CheckBMG.sh
``` 

Go to "files" and select "Open files", and then select "NEMO" as grid file format, and load both coordinates_BMG.nc and a bathy_BMG.nc as coordinates and bathymetry file. You can also load coastline files such as gshhs coastline [available here](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/INPUTS/global_gshhs_h.line.tar.gz).

Then, you can play around with BMG. By clicking on the icon circled in blue in Figure 2, you can choose your selector (unique point, rectangle, polygon...). Depending on your selector, you can select a unique point or a whole area and assign a bathymetry value to it. In Figure 2, we opened the bay of Bristol that was referenced as land in the domain_cfg file that we created with the steps above.

<p align="center" width="100%">
    <img src="https://github.com/bolb-ocean/AMM12-hackathon/blob/main/FIGURES/figure_BMG.png">
</p>

<p align="center" width="100%">
    <em>Figure 1: Screenshots of BMGtool where we open the bay of bristol.</em>
</p>

At the end of the process, you can save the updated bathymetry as a netcdf file.

> **Troubleshooting notes:**
> * _If BMGtool does not manage to open the file, try to change the projection system when loading the file. For AMM12, the tool usually crashes when using the default projection system WGS84._
> * _If nothing appears when loading the coordinate and bathymetry file along with a coastline file, try load first the coordinate and bathymetry file only (without coastlines). Then, load the coastline file by clicking on the icon circled in red in Figure 2._

## Step 6: Using the updated bathymetry to build a new domain_cfg file

Finally, you can use the updated bathymetry file to create a domain_cfg. For this, you can use the namelist example [here](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/NAMELISTS/namelist_cfg_domcfg_AMM12_from_updated_bathy). Make sure the following lines are updated accordingly to your updated bathymetry file:

```
   nn_bathy    =    1      ! = 0 compute analyticaly
                           ! = 1 read the bathymetry file
                           ! = 2 compute from external bathymetry
                           ! = 3 compute from parent (if "key_agrif")

   cn_domcfg   =  'AMM_R12_sco_domcfg.nc'                
   cn_fcoord   =  'AMM_R12_sco_domcfg.nc'             ! external coordinates file (jphgr_msh = 0)

   cn_topo     =  'UPDATED_BATHYMETRY.nc'             ! external topo file (nn_bathy =1)
   cn_bath     =  'BATHY_NAME'                 ! topo name in file  (nn_bathy =1)
   cn_lon      =  'LON_NAME'                    ! lon  name in file  (nn_bathy =1)
   cn_lat      =  'LAT_NAME'                    ! lat  name in file  (nn_bathy =1)
```

After updating the namelist, you can run the DOMAINcfg tool as in step 3. It should create a new domain_cfg.nc file from your updated bathymetry. You can then use this bathymetry to run a NEMO simulation.

> **Run the AMM12 default configuration with the updated domain_cfg file: why it will not work**
>
> _At this step, you have created the domain configuration file domain_cfg.nc Nonetheless, since the bathymetry has changed the model will not run with the default AMM12 forcing files, and this for several reasons:_
> * _The AMM12 default configuration starts from a restart, which comes from a previous simulation using the previous AMM12 bathymetry. Thus, an initialisation file should be re-created._
> * _The forcing files used for the lateral boundary conditions should also be re-created._

## Step 7: Testing the new domain configuration file in a simplified AMM12 simulation.

The new domain cfg file can be tested with the [simplified AMM12 namelist](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/NAMELISTS/namelist_cfg_NEMO_notides_norst_nobdy). This namelists gives NEMO parameters to launch a AMM12 simulation initialised from temperature and salinity only, which use the initial state as lateral boundary condition and has no tides. Here we use the AMM12 restart as initial T&S forcing, but the fields have to be drowned (i.e: extrapolated) over the land-sea mask. To do this, you can use the python script [here](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/SCRIPTS/BATHYMETRY_TOOLS/drown_fields.py). 
 

## To go further: boundary conditions, initial forcing

As mentionned above, since the bathymetry was updated, the initial forcing and the boundary condition files should be re-created according to the new bathymetry. You can accomplish this by applying these tutorials or apply these tools to your configuration:
* **Initial condition file:** Follow this [tutorial for recreating a pseudo-restart file from the copernicus reanalysis](https://github.com/NOC-MSM/SEAsia/wiki/7.-Initial-conditions---%E2%80%90--pseudo%E2%80%90restart-file). 
* **Boundary forcing conditions**:<br> 
&nbsp; &nbsp; - Use this [tool to build the boundary conditions](https://github.com/NOC-MSM/pyBDY?tab=readme-ov-file), along with some documentation and tutorials.<br> 
&nbsp; &nbsp; - Alternatively, follow this [tutorial to make open boundary conditions](https://github.com/NOC-MSM/SEAsia/wiki/4.-Make-open-boundary-conditions).
* **River forcings**: Since the coastlines have changed, the river forcing (if present) should also be updated.<br> 
&nbsp; &nbsp; - Follow this [tutorial  to recreate the river forcing files](https://github.com/NOC-MSM/SEAsia/wiki/6.-River-Forcing).<br>
&nbsp; &nbsp; - If the river forcing is provided as surface boundary condition (`ln_rnf=.true.`), you can follow the step 1 of this [tutorial using an automated script](https://github.com/immerse-project/eNEATL36-BIzoo_Demonstator/wiki/3.-Runoffs) to replace automatically the river mouth towards.




