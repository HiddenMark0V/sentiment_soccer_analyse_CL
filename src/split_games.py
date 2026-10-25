import random
from pathlib import Path
import pandas as pd

# Importieren der JSON-Loader Funktion.
from src.json_loader import load_soccer_comments

# Alle Spiele einlesen und als df speichern.
df = load_soccer_comments()

# Eindeutige Spiel-Ids bestimmen und sortieren.
game_ids = sorted(df["match_id"].unique())


# Spiele mit einem festen Seed mischen.
random_games = random.Random(42)
random_games.shuffle(game_ids)

# Es liegen 39 Spiele vor.
# Aufteilen in 20 Spiele für das Training
# und 19 Spiele für den Test.
train_games = game_ids[:20]
test_games = game_ids[20:]

# Aufteilung im DataFrame speichern.
df_split = pd.DataFrame({"match_id": train_games + test_games, "split": ["train"] * 20 + ["test"] * 19})


# Projektordner bestimmen.
project_root = Path(__file__).resolve().parent.parent

# Speicherort der CSV-Datei bestimmen.
metadata_folder = project_root / "data" / "metadata"
csv_path = metadata_folder / "game_split.csv"

# Aus dem df eine CSV-Datei ertellen und am bestimmen Pfad speichern.
df_split.to_csv(csv_path, index=False)

####### Kontrolle #######

print("Traingames:", len(train_games))
print("Testgames:", len(test_games))
print("Überschneidungen:", set(train_games) & set(test_games))