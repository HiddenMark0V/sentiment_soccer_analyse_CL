import json
from pathlib import Path
import pandas as pd

# Importieren der JSON-Loader Funktion.
from src.json_loader import load_soccer_comments

# Laendernamen aus dem Openfootball Datensatz den Abkuerzungen aus den
# SocCor-Daten zuweisen.
country_codes = {
    "Albania": "ALB",
    "Austria": "AUT",
    "Belgium": "BEL",
    "Croatia": "CRO",
    "Czech Republic": "CZE",
    "Denmark": "DEN",
    "England": "ENG",
    "France": "FRA",
    "Georgia": "GEO",
    "Germany": "GER",
    "Hungary": "HUN",
    "Italy": "ITA",
    "Netherlands": "NED",
    "Poland": "POL",
    "Portugal": "POR",
    "Romania": "ROU",
    "Scotland": "SCO",
    "Serbia": "SRB",
    "Slovakia": "SVK",
    "Slovenia": "SVN",
    "Spain": "ESP",
    "Switzerland": "SUI",
    "Turkey": "TUR",
    "Ukraine": "UKR"
}

# Bestimmung der Dateipfade.
project_root = Path(__file__).resolve().parent.parent
metadata_folder = project_root / "data" / "metadata"
raw_data_path = metadata_folder / "euro2024_gamescores_raw.json"
csv_path = metadata_folder / "goals.csv"

# Einlesen der 39 SocCor-Daten.
df = load_soccer_comments()
soccor_game_ids = set(df["match_id"].unique())

# Einlesen der OpenFootball Tor-Daten von der EURO2024.
with open(raw_data_path, "r", encoding="utf-8") as f:
    euro_data = json.load(f)



# Initialisierung der Liste für alle Tore.
all_goals = []
matched_ids = set()

# Aueßere Schleife: Durch die OpenFootball EURO2024-Spiele durchlaufen.
for game in euro_data["matches"]:

    # Zuweiseung der Laendercodes.
    team_1 = country_codes[game["team1"]]
    team_2 = country_codes[game["team2"]]

    # Match_id so zusammensetzen wie auch im SocCor-Korpus vorkommt.
    match_id = team_1 + "_" + team_2

    # OpenFootball EURO2024: 51 Spiele
    # SocCor-Korpus dt. Kommentare: 39 Spiele
    # Daher nur die Spiele uebernehmen, die auch in SocCor vorkommen.
    if match_id not in soccor_game_ids:
        continue

    # wenn doch vorhanden, dann Id in matched_ids speichern.
    matched_ids.add(match_id)

    # Innere Schleife: durch die Tore beider Mannschaften durchlaufen.
    for g in ["goals1", "goals2"]:


        for goal in game.get(g, []):

            # Die Minuten und moegliche Verlaengerung der Tore speichern.
            minute = goal["minute"]
            offset = goal.get("offset", 0)

            # Zuordnung zu einer konkreten Halbzeit.
            if minute <= 45:
                half = 1
            else:
                half = 2


            # Torzeitpunkte in die SocCor Sekundenannotation uebertrage.
            # x 60 Sekunden = um von der Minutenangabe aus dem OpenFootball Datensatz
            # auf die Sekunden zu kommen.
            # In der zweiten Haelfte werden 45 min. abgezogen, da SocCor-Korpus
            # ab der zweiten Halbzeit bei Sekunde 0 anfaengt.
            if half == 1:
                goal_time_half_sec = (minute + offset) * 60

            else:
                goal_time_half_sec = (minute + offset - 45) * 60


            goal_infos = {"match_id": match_id, 
                          "scorer": goal["name"],
                          "minute": minute,
                          "offset": offset,
                          "half": half,
                          "goal_time_half_sec": goal_time_half_sec}

            all_goals.append(goal_infos)


# df mit den Toren.
df_goals = pd.DataFrame(all_goals)




####### Kontrolle ############

print("Zugeordnet:", len(matched_ids))
print("Erfasste tore:", len(df_goals))

if len(matched_ids) != 39 or len(df_goals) != 85:
    raise ValueError("Anzahl stimmt nicht")


# Tore als CSV speichern
df_goals = df_goals.sort_values(["match_id", "half", "goal_time_half_sec"])
df_goals.to_csv(csv_path, index=False)

print(df_goals.head())