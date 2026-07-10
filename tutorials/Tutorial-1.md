#Tutorial 1: Set‐up and run a simulation

This mini tutorial will provide you with additional guidance for setting up the NEMO build for the AMM12 demonstrator.
## Step 1 - Download and install NEMO

The NEMO user guide includes detailed instruction on how to install and compile NEMO and can be viewed here: https://sites.nemo-ocean.io/user-guide/install.html#introduction 

<br> This guide will assume that you have been able to compile NEMO successfully. 

## Step 2 - Compile the AMM12 configuration

Build NEMO following the instructions above. Be sure to specify the AMM12 reference configuration using the -r option:
```
./makenemo –m 'auto' –r AMM12 -n 'MY_AMM12'
```
## Step 3 - Download AMM12 forcings

Download and unzip the AMM12 configuration input files [here](https://gws-access.jasmin.ac.uk/public/nemo/sette_inputs/).

```
tar -xvzf AMM12_v5.0.1.tar.gz
```

The folder will have the following structure: 

```
- A "bdydata" folder which provides daily tidal forcing at the boundaries for the period 2012-01-01 to 2012-01-10.
- A "fluxes" folder containing daily surface fluxes, stress and sea surface temperature for the period 2012-01-01 to 2012-01-10.
- Rivers forcing file "amm12_rivers.nc" which provides daily river forcing for the the period 2012-01-01 to 2012-01-10. Note the Baltic boundary is included within the river file and is specified as a river source. Unlike ordinary river points these Baltic inputs also include salinity and temperature data.
- 2 restart files "amm12_restart_oce.nc" and "amm12_restart_oce_rk3.nc" which provide salinity and temperature initial conditions.
- 2 domain files "AMM_R12_sco_domcfg.nc" and "coordinates.bdy.nc". The first is a prebuilt domain for AMM12. The second provides the coordinates for rebuilding the domain.
```


## Step 4: Run an AMM12 simulation

1. Copy the forcing files into your experiment directory e.g. cp -r AMM12_forcings/* /nemo_5.0.1/cfgs/MY_AMM12/EXP00/.
2. At this point we recommend making a copy of your NEMO build after successfully following the previous steps. This allows you to perform new runs or rebuild nemo from a clean install.
3. Finally run the model using the following command:
```./mpirun -np 16 ./nemo```

## Step 5: Copy AMM12 hackathon config files

Download this repository using 
```
git clone git@github.com:bolb-ocean/AMM12-hackathon.git
``` 
Or by downloading and extracting from the [latest doi release](https://zenodo.org/records/15704315)

Extract and then copy the files in the cfgs_update/ directory to your AMM12 build.
```
cp -r cfgs_update/* /nemo_5.0.1/cfgs/MY_AMM12/EXP00/.
```

## Recommendations on good practices

1. If you want to change any NEMO code (.f90 files or files in src) you will need to recompile. Here it is recommended to copy your whole nemo build before making changes. 
2. If you want to change forcings, namelist options, .xml files, you do not need to recompile NEMO. Here you can make a new copy of NEMO or just a copy of your cfgs/MY_AMM12/EXP$$ folder.

You will see an example of these in [Tutorial 2](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/tutorials/Tutorial-2.md where namelist parameters are changed and [Tutorial 3](https://github.com/bolb-ocean/AMM12-hackathon/blob/main/tutorials/Tutorial-3.md) where new diagnostics are added to source code. 
