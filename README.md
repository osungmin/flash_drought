# Flash Drought
Example python scripts to detect flash drought events from gridded soil moisture data

under \prep

- soilm_weighted.sh: to create soil moisture data at a specific depth (cdo)
- pentad.sh: to convert daily soil moisture data to pentad (cdo)
- compute_qval.py: to compute n-quantile of soil moisture over a given period (e.g. 20th/40th percentile to define FD onset/termination)
- prep_quan.py: to compute soil moisture quantiles at every time steps


These scripts are used in 

Flash drought drives rapid vegetation stress in arid regions in Europe, ERL, O and Park (2023)
https://doi.org/10.1088/1748-9326/acae3a
