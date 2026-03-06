# Chicago Crime & Weather Correlation Analysis

SQL-based analysis of how weather conditions (temperature, precipitation, season) correlate with crime patterns across Chicago in 2019. Uses an in-memory SQLite database to run structured queries on merged crime and weather datasets, with visualizations to surface actionable patterns.

## Tech Stack

- **Language:** Python 3
- **Data:** pandas, sqlite3 (in-memory SQL engine)
- **Visualization:** seaborn, matplotlib
- **Notebook:** Jupyter

## Key Analyses

| Query | Insight |
|---|---|
| Avg temperature per crime type | Which crimes peak in heat vs. cold |
| Crime counts by temp segment (Cold / Moderate / Hot) | Temperature-based crime density |
| Weather-crime correlation | Scatterplot of AvgTemp vs. CrimeCount |
| Season-wise crime trends | Seasonal decomposition by crime category |

## Project Structure

```
.
├── 320final.ipynb            # Main analysis notebook
├── chicago_temps_18-23.csv   # Daily weather data (2018–2023)
├── images/
│   ├── correlation_heatmap.png    # Pearson r matrix — crime vs weather
│   ├── crime_vs_temperature.png   # Monthly count + temp dual-axis
│   └── top_crime_types.png        # Top 10 crime categories
└── README.md
```

> **Note:** The Chicago crime dataset (59 MB) is excluded from this repo due to size.
> Download it from the [Chicago Data Portal](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2) and place it in the project root as `Crimes_-_2019_20231112.csv`.

## How to Run

```bash
pip install pandas seaborn matplotlib notebook
jupyter notebook 320final.ipynb
```

Make sure both CSV files are in the same directory as the notebook before running.

## Sample Visualizations

- **Temperature vs. Crime Count** – scatterplot showing positive correlation in warmer months
- **Season-Wise Crime Trends** – bar chart comparing crime volumes across Winter / Spring / Summer / Fall

## Relevance to Data Science / SCM Roles

This project demonstrates the same analytical workflow used in supply chain demand planning:

- Joining heterogeneous datasets via SQL (crime + weather → supply events + external factors)
- Segmenting data by external conditions (temperature segments ↔ demand buckets)
- Identifying seasonal patterns for forecasting and planning

## Visualizations

### Correlation Matrix
![Correlation Heatmap](images/correlation_heatmap.png)
*Monthly crime count correlates strongly with temperature (r=0.84) — warmer months drive significantly higher crime volumes*

### Monthly Crime Count vs Average Temperature
![Crime vs Temperature](images/crime_vs_temperature.png)
*Summer peak in both crime (red bars) and temperature (blue line) confirms seasonal co-movement across all of 2019*

### Top 10 Crime Types
![Top Crime Types](images/top_crime_types.png)
*Theft dominates with 50K+ incidents — over 3× the volume of the next category, signaling concentrated risk*

---

*Data source: [City of Chicago Open Data Portal](https://data.cityofchicago.org/)*
