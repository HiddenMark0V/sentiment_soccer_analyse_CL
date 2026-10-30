# [KI_1]
# Code zur Erstellung des Plots wurde mit Hilfe eines LLMs generiert und stellenweise modifiziert.
# Siehe fuer mehr Infos unter docs/KI_dokumentation.pdf.

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# CSV-Datei einlesen (muss im selben Ordner wie dieses Skript liegen).
project_root = Path(__file__).resolve().parent.parent

# Ergebnisse aller auswertbaren Tore laden.
daten = pd.read_csv(project_root / "outputs" / "goal_windows.csv")

# Prüfen, ob alle 83 Torereignisse einen Differenzwert haben.
if len(daten) != 83 or daten["diff"].isna().any():
    raise ValueError("Erwartet werden 83 Torereignisse ohne fehlende diff-Werte.")

# Differenzen aufsteigend sortieren und laufende Nummern vergeben.
differenzen = daten["diff"].sort_values().reset_index(drop=True)
tor_nummern = range(1, len(differenzen) + 1)
mittelwert = differenzen.mean()

# Kontrollwerte aus der Datei ausgeben.
print(f"Anzahl:      {len(differenzen)}")
print(f"Mittelwert:  {mittelwert:+.6f}")
print(f"Minimum:     {differenzen.min():+.6f}")
print(f"Maximum:     {differenzen.max():+.6f}")

# Abbildung erstellen.
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(tor_nummern, differenzen, s=28, alpha=0.9)
ax.axhline(y=0, color="gray", linewidth=1, label="Keine Veränderung (0)")
ax.axhline(y=mittelwert, color="tab:orange", linestyle="--",
           linewidth=1.6, label=f"Mittelwert: {mittelwert:+.4f}")

# Beschriftungen und Gestaltung.
ax.set_title("Sentimentveränderung vor und nach Torereignissen")
ax.set_xlabel("Torereignisse (aufsteigend nach Differenz sortiert)")
ax.set_ylabel("Sentimentdifferenz (120 s danach − 120 s davor)")
ax.set_xlim(0.5, len(differenzen) + 0.5)
ax.set_xticks(range(1, len(differenzen) + 1, 10))
ax.grid(axis="y", alpha=0.25)
ax.set_axisbelow(True)
ax.legend(loc="lower right", frameon=False)

# Als druckfähige PNG-Datei speichern.
fig.tight_layout()
fig.savefig("sentiment_torereignisse.png", dpi=300, bbox_inches="tight")
plt.show()
