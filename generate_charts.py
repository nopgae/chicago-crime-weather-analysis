"""Generate visualization PNGs for chicago-crime-weather-analysis."""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

os.makedirs('images', exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────
df = pd.read_csv('merged_crime_weather_2019_fixed.csv')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])
df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
df['MonthNum'] = df['Date'].dt.month

# ── Chart 1: Correlation Heatmap ──────────────────────────────────────────
# Monthly aggregations
monthly = df.groupby('Month').agg(
    CrimeCount=('CrimeType', 'count'),
    AvgTemp=('AvgTemp', 'mean'),
    HighTemp=('HighTemp', 'mean'),
    LowTemp=('LowTemp', 'mean'),
    Precipitation=('Precipitation', 'mean')
).reset_index()

corr_cols = ['CrimeCount', 'AvgTemp', 'HighTemp', 'LowTemp', 'Precipitation']
corr = monthly[corr_cols].corr()

col_labels = ['Crime\nCount', 'Avg\nTemp', 'High\nTemp', 'Low\nTemp', 'Precip']

fig, ax = plt.subplots(figsize=(9, 7))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(
    corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
    vmin=-1, vmax=1, square=True, linewidths=1, linecolor='white',
    xticklabels=col_labels, yticklabels=col_labels,
    annot_kws={'size': 13, 'weight': 'bold'}, ax=ax,
    cbar_kws={'shrink': 0.75, 'label': 'Pearson r'}
)
ax.set_title('Correlation Matrix — Monthly Crime Count vs Weather\nChicago 2019 (260,100 incidents)',
             fontsize=16, fontweight='bold', pad=15)
ax.tick_params(axis='x', labelsize=12, rotation=0)
ax.tick_params(axis='y', labelsize=12, rotation=0)

plt.tight_layout()
plt.savefig('images/correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('✓ correlation_heatmap.png')

# ── Chart 2: Monthly crime count vs avg temperature ───────────────────────
fig, ax1 = plt.subplots(figsize=(13, 6))

color_crime = '#E53E3E'
color_temp  = '#2B6CB0'

ax1.bar(monthly['Month'], monthly['CrimeCount'], width=20,
        color=color_crime, alpha=0.7, label='Monthly Crime Count', zorder=2)
ax1.set_xlabel('Month', fontsize=13, labelpad=10)
ax1.set_ylabel('Number of Crimes', fontsize=13, color=color_crime, labelpad=10)
ax1.tick_params(axis='y', labelcolor=color_crime, labelsize=10)
ax1.tick_params(axis='x', labelsize=10, rotation=20)
ax1.spines[['top']].set_visible(False)
ax1.yaxis.grid(True, alpha=0.3, linestyle='--')
ax1.set_axisbelow(True)

ax2 = ax1.twinx()
ax2.plot(monthly['Month'], monthly['AvgTemp'], color=color_temp,
         linewidth=2.5, marker='o', markersize=6, label='Avg Temperature (°F)', zorder=3)
ax2.set_ylabel('Average Temperature (°F)', fontsize=13, color=color_temp, labelpad=10)
ax2.tick_params(axis='y', labelcolor=color_temp, labelsize=10)
ax2.spines[['top']].set_visible(False)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=12, loc='upper left', framealpha=0.9)

ax1.set_title('Monthly Crime Count vs Average Temperature — Chicago 2019\n(r = 0.84: strong positive correlation)',
              fontsize=16, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('images/crime_vs_temperature.png', dpi=150, bbox_inches='tight')
plt.close()
print('✓ crime_vs_temperature.png')

# ── Chart 3: Top 10 crime types ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 7))

top_crimes = df['CrimeType'].value_counts().head(10).sort_values()
colors_bar = ['#2B6CB0' if i >= len(top_crimes) - 3 else '#718096'
              for i in range(len(top_crimes))]

bars = ax.barh(top_crimes.index, top_crimes.values, color=colors_bar,
               edgecolor='white', linewidth=0.8, height=0.65)

for bar, val in zip(bars, top_crimes.values):
    ax.text(val + 200, bar.get_y() + bar.get_height() / 2,
            f'{val:,}', va='center', fontsize=11)

ax.set_xlabel('Number of Incidents', fontsize=13, labelpad=10)
ax.set_title('Top 10 Crime Types — Chicago 2019\n(260,100 total incidents across all districts)',
             fontsize=16, fontweight='bold', pad=15)
ax.tick_params(axis='y', labelsize=11)
ax.tick_params(axis='x', labelsize=10)
ax.set_xlim(0, top_crimes.max() * 1.15)
ax.spines[['top', 'right']].set_visible(False)
ax.xaxis.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('images/top_crime_types.png', dpi=150, bbox_inches='tight')
plt.close()
print('✓ top_crime_types.png')

print('\nAll charts saved to images/')
