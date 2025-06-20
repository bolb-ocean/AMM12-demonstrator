
# Atlantic Margin Model (AMM12) demonstrator

This page describes the AMM12 (Atlantic Margin Model) configuration for the NEMO ocean model in its version 5.0.1. It contains a [wiki](https://github.com/bolb-ocean/AMM12-hackathon/wiki) which contains step by step tutorials on how to:

* [Tutorial 1](https://github.com/bolb-ocean/AMM12-hackathon/wiki/Tutorial-1:-Set%E2%80%90up-and-run-a-simulation): Set-up the AMM12 standard configuration and perform a simulation. It also contains some general guidance on good practice on ocean modelling.
* [Tutorial 2](https://github.com/bolb-ocean/AMM12-hackathon/wiki/Tutorial-2:-Changing-namelist-parameters-to-turn-tide-on-and-off): Change namelist parameters to set the tides on and off, and analyse the results
* [Tutorial 3](https://github.com/bolb-ocean/AMM12-hackathon/wiki/Tutorial-3:-Adding-new-Diagnostics): Add new diagnostics as model outputs.
* [Tutorial 4](https://github.com/bolb-ocean/AMM12-hackathon/wiki/Tutorial-4:-Create-domain-configuration-files-and-update-the-bathymetry): Create domain configuration files (domain_cfg.nc) and update the bathymetry.
* [Tutorial 5](https://github.com/bolb-ocean/AMM12-hackathon/wiki/Tutorial-5:-MLR-tidal-harmonic-analysis): Multiple-Linear-Regression (MLR) tidal harmonic analysis.

<p align="center" width="100%">
    <img src="https://github.com/bolb-ocean/AMM12-hackathon/blob/main/FIGURES/AMM_domain.png">
</p>

## Description

The AMM12 (O'Dea et al., 2012) configuration covers covers the North-West European shelf and part of the North-East Atlantic ocean. This configuration allows to tests several features of NEMO functionality specifically addressed to the shelf seas. 

Physics upgrades were added to AMM12 following those used in (AMM7 CO9)[https://github.com/JMMP-Group/CO_AMM7] where appropriate. Upgrades were limited to those that did not require a change in forcing files.
| Variable              | AMM12 NEMOv4 | AMM12 NEMOv5 |
| :---------------- | :------: | :----: |
| namsbc        |   ln_traqsr = .false.   | ln_traqsr = .true. |
| namsbc_apr           |   ln_ref_apr = .false. | nn_ref_apr = 0 (same physics variable name change) |
| namdrg_bot   |  rn_Cd0 = 0.0025 | rn_Cd0 = 0.001 |
| namdrg_top |  rn_Cd0 =0.0025 rn_ke0 = 0.0 | rn_Cd0 = 0.001 rn_ke0 = 0.0025 |
| nameos | ln_teos10 = .true. ln_eos90 = .false. rn_lambda2 = 7.4914e-4 | ln_teos10 = .false. ln_eos80 = .true. rn_lambda2 = 5.4914e-4 |
| namtra_adv | nn_fct_h = 2 | nn_fct_h = 4 |
| namtra_mle | ln_mle = .false. | ln_mle = .true. |
| namdyn_ldf | rn_Uv = 0.12 | rn_Uv = 0.012 |
| namzdf_gls | rn_emin = 1e-7 nn_z0_met = 2 | rn_emin = 1e-6 nn_z0_met = 1 |


