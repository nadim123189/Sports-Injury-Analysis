# Data Sources

This project uses three public datasets. Here is where each one comes from and how we used it.

## 1. Sports and Recreational Injuries (CPSC NEISS data)

National Safety Council. (2023). *Sports and Recreational Injuries*. Injury Facts.
https://injuryfacts.nsc.org/home-and-community/safety-topics/sports-and-recreational-injuries/

Emergency department injury estimates from the Consumer Product Safety Commission's NEISS system, covering 2013 to 2023. We compiled the yearly tables into one Excel workbook called `Consumer Product Injury Tables.xlsx`. It has a "Product Category Summary" sheet plus one sheet per year, and the main script reads from it.

## 2. Concussion Incidence and Trends in 20 High School Sports

Kerr, Z. Y., Chandran, A., Nedimyer, A. K., Arakkal, A., Pierpoint, L. A., & Zuckerman, S. L. (2019). Concussion Incidence and Trends in 20 High School Sports. *Pediatrics*, 144(5), e20192180.
https://doi.org/10.1542/peds.2019-2180

Concussion rates per 10,000 athletic exposures by sport and gender, for the 2013 to 2014 and 2017 to 2018 school years.

## 3. Games and Practices With Associated Injury Rates

Project NEURON, University of Illinois. (2024). *Games and Practices With Associated Injury Rates*.
https://neuron.illinois.edu/simulations/games-and-practices-with-associated-injury-rates.html

Injury rates per 1,000 exposures by sport, gender, and season, with games and practices separated, from studies spanning 1988 to 2004.

## About the Excel workbook

The workbook is not included in this repository. To rerun the script, rebuild it from the yearly NEISS tables on the Injury Facts page above and save it in this folder as `Consumer Product Injury Tables.xlsx`. The script expects a sheet named "Product Category Summary" and one sheet for each year from 2013 to 2023. The charts and results from our run are in the report and the `images/` folder.
