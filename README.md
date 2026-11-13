# Sports Injury Analysis

## Project Description

A data analysis project that looks at who gets hurt playing sports and using sports equipment in the United States. It combines three public datasets (emergency department visits from 2013 to 2023, high school concussion rates, and game and practice injury rates) and uses linear regression and KMeans clustering to show which age groups, sports, and pieces of equipment carry the most risk. Built for DS2500 at Northeastern University.

## Key Findings

* Age matters: ages 5 to 14 and 15 to 24 had the highest sports and recreation injury rates every year from 2013 to 2023.
* Biggest in 2023: exercise equipment (482,886 injuries) and bicycles and accessories (405,688 injuries).
* Most serious: ATVs, mopeds, and minibikes had the highest share of injuries ending in hospitalization or death on arrival (19.25%), with bicycles next at 14.82%.
* Three clusters: KMeans split equipment into low risk, high volume but mostly treated and released, and high volume with many hospitalizations (mostly bicycles and exercise equipment).
* Concussions: boys football had the highest rate at 10.40 per 10,000 athletic exposures, and girls' sports ran higher than boys' overall.
* Exposure and season: more games and practices meant more injuries, and preseason was the riskiest time of year (regression R squared of 0.54).
* A simple age model was weak (R squared of 0.174), so age alone does not explain injury rates.

## Data Used

* CPSC NEISS emergency department injury estimates, 2013 to 2023, via the National Safety Council's Injury Facts
* Concussion Incidence and Trends in 20 High School Sports (Kerr et al., 2019, Pediatrics)
* Project NEURON, University of Illinois: games and practices with associated injury rates, 1988 to 2004

Full links and notes are in `data/README.md`.

## Tools Used

* Python
* pandas and NumPy
* matplotlib and seaborn
* scikit-learn (LinearRegression, KMeans, StandardScaler)

## Repository Structure

* `src/sports_product_injury_ed_visits.py`: Main analysis script. Loads and cleans the NEISS tables, plots injury rates, fits the regression, and runs the clustering.
* `data/`: Source links and notes on where each dataset comes from.
* `report/Sports_Related_Injury_Project_Report.pdf`: Full write up with every chart, the methods, and the conclusions.
* `images/`: Charts used in this README.
* `requirements.txt`: Python packages needed to run the script.

## How to Run

```bash
git clone https://github.com/YOUR_USERNAME/sports-injury-analysis.git
cd sports-injury-analysis
pip install -r requirements.txt
python src/sports_product_injury_ed_visits.py
```

Each chart opens in its own window as the script runs.

## Limitations

The data has no geographic or income information, NEISS only counts injuries that reached an emergency department, and the three sources cover different years and populations, so they are best read side by side.

## Team

Adam Kwoh, Nadim-Marc El Achkar, and Henri Pulake

[ONE OR TWO SENTENCES ON WHAT YOU PERSONALLY BUILT]
