
import json
import re
from pathlib import Path
import pandas as pd

# Projektverzeichnis relativ zum Speicherort dieses Skripts bestimmen.
# json_loader.py sollte vom Ordner src/ ausgefuehrt werden
# daher zwei Verzeichnisebenen hoeher gehen.
project_root = Path(__file__).resolve().parent.parent

# Vom Stammverzeichnis aus alle JSON-Dateien im "Sportschau ordner" suchen.
folder = project_root / "data" / "cleaned_data" / "Sportschau"
files = sorted(list(folder.glob("*.json")))

#print(len(files))

# Leere Liste fuer alle Kommentarsegmente.
all_segments =  []

# Jede JSON-Datei einlesen und Spielnamen und Halbzeit
# aus dem Dateinamen bestimmen.
for file in files:

    with open(file, "r", encoding="utf-8") as f:

        segments = json.load(f)

        #print(f"Dateiname: {file.name}, Segmente: {len(segments)}")

    match = re.fullmatch(
        r"^\d+_([A-Z]{3}_[A-Z]{3})_(first|second)_half\.json$",
        file.name)

    if match is not None:

        game = match.group(1)
        half = match.group(2)

        if half == "first":
            half = 1

        else:
            half = 2

    # Manuell eigene Fehlermeldung auslösen und Schleife abbrechen.    
    else:
        raise ValueError(f"Ungültiger Dateiname: {file.name}")

    #print(f"game={game}, half={half}")

    # Jedem Segment Spielname und Halbzeit zuordnen.
    # Zeitangaben und Kommentartexte werden uebernommen.
    for segment in segments:
        
        segment_info = {"match_id": game, 
                        "half": half, 
                        "start": segment["start"], 
                        "end": segment["end"], 
                        "text": segment["text"]}

        all_segments.append(segment_info)


df = pd.DataFrame(all_segments)

# Zeitlichen Mittelpunkl jedes Kommenats berechnen und
# dem DataFrame als neue Spalte hinzufuegen.
df["time_half_sec"] = (df["start"] + df["end"]) / 2

print(df.shape)

# print("Verarbeitet:", len(all_segments))
# print("Erstes Segment:", all_segments[0])
# print("Letztes Segment:", all_segments[-1])

