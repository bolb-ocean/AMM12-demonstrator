# Tutorial 2: Changing namelist parameters to turn tide on and off

## Aim of Tutorial
The aim of this tutorial is to give the readers an opportunity to make changes to the namelist parameters and see the effects of it. Here we choose to use tidal forcing to demonstrate how to make changes to the namelist parameters. 

You try to change the namelist parameters by following the steps below or simply download from here. 
NEMO only reads `namelist_cfg` for the run, so the user needs to rename the namelist to `namelist_cfg` before running NEMO.

### namelist_cfg for tide on and off
1. [`namelist_cfg_TIDEON`](https://github.com/bolb-ocean/AMM12-hackathon/blob/e2a79bb7f1b2b6f5c8fd72345555f8298309fbab/SCRIPTS/TIDE/namelist_cfg_TIDEON)
2. [`namelist_cfg_TIDEOFF`](https://github.com/bolb-ocean/AMM12-hackathon/blob/e2a79bb7f1b2b6f5c8fd72345555f8298309fbab/SCRIPTS/TIDE/namelist_cfg_TIDEOFF)

### To output hourly ssh
1. [`file_def_nemo-oce.xml`](https://github.com/bolb-ocean/AMM12-hackathon/blob/e2a79bb7f1b2b6f5c8fd72345555f8298309fbab/SCRIPTS/TIDE/file_def_nemo-oce.xml)

It is always a good practice to copy EXP00 to a new folder for every new configuration/experiments to keep track of what you have done.

```
cp -r EXP00 EXP_tide_on
cd EXP_tide_on
```

## Step 1 Editing namelist_cfg to turn tide OFF
The tidal forcings are **on** by default in the AMM12 namelist_cfg. In this example, the tidal forcing are on and the following tidal constituents were used. 
 
```
!-----------------------------------------------------------------------
&nam_tide      !   tide parameters                                      (default: OFF)
!-----------------------------------------------------------------------
   ln_tide     = .true.        ! Activate tides
      ln_tide_pot     = .true. !  use tidal potential forcing
   sn_tide_cnames(1)  = 'Q1'   !  name of constituent
   sn_tide_cnames(2)  = 'O1'
   sn_tide_cnames(3)  = 'P1'
   sn_tide_cnames(4)  = 'S1'
   sn_tide_cnames(5)  = 'K1'
   sn_tide_cnames(6)  = '2N2'
   sn_tide_cnames(7)  = 'MU2'
   sn_tide_cnames(8)  = 'N2'
   sn_tide_cnames(9)  = 'NU2'
   sn_tide_cnames(10) = 'M2'
   sn_tide_cnames(11) = 'L2'
   sn_tide_cnames(12) = 'T2'
   sn_tide_cnames(13) = 'S2'
   sn_tide_cnames(14) = 'K2'
   sn_tide_cnames(15) = 'M4'
/
!-----------------------------------------------------------------------
&nambdy        !  unstructured open boundaries                          (default: OFF)
!-----------------------------------------------------------------------
    ln_bdy     = .true.   !  Use unstructured open boundaries
    nb_bdy     =  1       !  number of open boundary sets
    !
    cn_dyn2d     = 'flather'
    nn_dyn2d_dta =  3
    cn_tra       =  'frs'
    nn_tra_dta   =   1 
/
```

To turn the tidal forcing **off**, we need change `ln_tide` and `nn_dyn2d_dta` from `true` to `false` and `3` to `1` in the namelist_cfg respectively.
```
!-----------------------------------------------------------------------
&nam_tide      !   tide parameters                                      (default: OFF)
!-----------------------------------------------------------------------
   ln_tide     = .false.        ! Activate tides
!-----------------------------------------------------------------------
&nambdy        !  unstructured open boundaries                          (default: OFF)
!-----------------------------------------------------------------------
    nn_dyn2d_dta =  1  ! = 0, bdy data are equal to the initial state
                       ! ! = 1, bdy data are read in 'bdydata .nc' files
                       ! ! = 2, use tidal harmonic forcing data from files
                       ! ! = 3, use external data AND tidal harmonic forcing
```

## Step 2 To make NEMO output a single file and output the hourly instantaneous ssh.
We need to change the `file_definition` in `file_def_nemo-oce.xml` to `one_file`.

Add a new line ``<field field_ref="ssh"  operation="instant" enabled=".TRUE." />``


```
============================================================================================================
=                                           output files definition                                        =
=                                            Define your own files                                         =
=                                         put the variables you want...                                    =
============================================================================================================
    -->

    <file_definition type="one_file" name="@expname@_@freq@_@startdate@_@enddate@" sync_freq="10d" min_digits="4">

      <file_group id="oce_1ts" output_freq="1ts"  output_level="10" enabled=".TRUE."/> <!-- 1 time step files -->

      <!--old      <file_group id="1h" output_freq="1h"  output_level="10" enabled=".TRUE."/> old --> <!-- 1h files -->
      <!-- TB files -->
      <file_group id="oce_1h" output_freq="1h"  output_level="10" enabled=".TRUE."  >

        <file id="file1" name_suffix="_shelftb_grid_T" description="TB ocean T grid variables" enabled=".TRUE." >
          <field field_ref="sst"  operation="instant" enabled=".TRUE." />
          <field field_ref="sbt"  operation="instant" enabled=".TRUE." />
          <field field_ref="sss"  operation="instant" enabled=".TRUE." />
          <field field_ref="sbs"  operation="instant" enabled=".TRUE." />
          <field field_ref="ssh"  operation="instant" enabled=".TRUE." />
        </file>

```

## Step 3 Running NEMO with Tide OFF

Using the same command to run NEMO with 16 processors
```
mpirun -np 16 ./nemo
```

The daily, hourly and 5 days output are here.

```
AMM12_1d_20120102_20120109_grid_T.nc
AMM12_1d_20120102_20120109_grid_U.nc
AMM12_1d_20120102_20120109_grid_V.nc
AMM12_1h_20120102_20120109_shelftb_grid_T.nc
AMM12_1h_20120102_20120109_shelftb_grid_U.nc
AMM12_1h_20120102_20120109_shelftb_grid_V.nc
AMM12_5d_20120102_20120109_grid_T.nc
AMM12_5d_20120102_20120109_grid_U.nc
AMM12_5d_20120102_20120109_grid_V.nc
AMM12_5d_20120102_20120109_grid_W.nc

```
We move the files to the folder we created for analysis later.
```
mkdir TideOFF
mv AMM12_*20120102_20120109*.nc TideOFF
```

## Step 4 Running NEMO with Tide ON
We need to edit the namelist_cfg again to turn the tide **on** and run NEMO again.

To turn the tidal forcing on again, we need change ln_tide and nn_dyn2d_dta from false to true and 1 to 3 in the namelist_cfg respectively.

```
mpirun -np 16 ./nemo
mkdir TideON
mv AMM12_*20120102_20120109*.nc TideON
```

## Step 5 Visualizing the results
We select a few points within the AMM12 domain and plot the SSH along time. We compare the SSH of NEMO that is run with Tide ON and OFF.

![](https://github.com/bolb-ocean/AMM12-hackathon/blob/a8d50eb24011a069104ef23db4f703e38057530a/SCRIPTS/TIDE/Loc1.png)
![](https://github.com/bolb-ocean/AMM12-hackathon/blob/a8d50eb24011a069104ef23db4f703e38057530a/SCRIPTS/TIDE/Loc2.png)
![](https://github.com/bolb-ocean/AMM12-hackathon/blob/a8d50eb24011a069104ef23db4f703e38057530a/SCRIPTS/TIDE/Loc3.png)

We follow the [notebook](https://github.com/bolb-ocean/AMM12-hackathon/blob/572c89df462fd1b2f646e42ce8d0506fe7443d22/SCRIPTS/TIDE/VisualizingOutput.ipynb) here to plot the results.
