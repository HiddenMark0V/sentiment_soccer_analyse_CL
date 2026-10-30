# [Q_4]

from pathlib import Path
import pandas as pd
from scipy.stats import ttest_rel

# Ergebnisse der Torfensteranalyse laden.
df = pd.read_csv("outputs/goal_windows.csv")

# Gepaarter t-Test: nachher gegen vorher.
t_statistic, p_value =  ttest_rel(
    df["mean_after_goal"],
    df["mean_before_goal"]
)

print("Anzahl Tore:", len(df))
print("Mittelwert vorher:", df["mean_before_goal"].mean())
print("Mittelwert nachher:", df["mean_after_goal"].mean())
print("Mittlere Differenz:", df["diff"].mean())
print(f"t-Wert: {t_statistic:.3f}")
print(f"p-Wert: {p_value:.4f}")

# Ergebnisse:
## Anzahl Tore: 83
## Mittelwert vorher: -0.11430124060515573
## Mittelwert nachher: -0.09738119657318252
## Mittlere Differenz: 0.016920044031973197
## t-Wert: 0.890
## p-Wert: 0.3760