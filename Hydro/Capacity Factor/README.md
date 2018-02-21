# Capacity Factors


This folder contains data that describes the production of hydro station on given scenarios.


The "capacityFactorHistoric.csv" contains a historical analysis of the production of a hydro station.

  - Each row represents a hydro station.
  - Column 50% contains the median of the historical data.
  - The "25%" column is defined as the middle number between the smallest number and the median of the data set.
  - The "75%" column is the middle value between the median and the highest value of the data set.


The "Year#%" columns represent the year to which each value belongs.



The same goes for "capacityFactorAD.csv" but in this case the data are classified by average per year.

  - Each row represents a hydro station.
  - Column 50% contains the median of the annual data.
  - The "25%" column is defined as the middle number between the smallest number and the median of the annual data set.
  - The "75%" column is the middle value between the median and the highest value of the annual data set.


The "Year#%" columns represent the year to which each value belongs.




The next plot illustrates the result

![alt tag](https://github.com/sergiocastellanos/switch_mexico_data/blob/master/Hydro/Plots/percentiles.png)


You will be able to generate a plot for a given hydro station by typing on command line:

```sh
  $ python capacityFactorAD.py [state] [station name]
  ```

  - [state] argument corresponds to the state of interest, all states available are stored in this [folder][folder]
  - [station name] represents the name of the hydro station of interest.

You will be able to consult all available hydro stations on:

**[Data/Production-Drought-Precipitation][data]/ [state] / [hydroStationName.csv]**

[data]: <https://github.com/sergiocastellanos/switch_mexico_data/tree/master/Hydro/Data/Production-Drought-Precipitation>
[folder]: <https://github.com/sergiocastellanos/switch_mexico_data/tree/master/Hydro/Data/Production-Drought-Precipitation>
