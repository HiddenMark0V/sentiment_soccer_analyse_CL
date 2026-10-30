
import json
import re
from pathlib import Path
import pandas as pd

def load_soccer_comments():

    # [Q_1]
    # Projektverzeichnis relativ zum Speicherort dieses Skripts bestimmen.
    # json_loader.py sollte vom Ordner src/ ausgefuehrt werden
    # daher zwei Verzeichnisebenen hoeher gehen.
    project_root = Path(__file__).resolve().parent.parent

    # Vom Stammverzeichnis aus alle JSON-Dateien im "Sportschau ordner" suchen.
    folder = project_root / "data" / "cleaned_data" / "Sportschau"

    # [Q_2]
    files = sorted(list(folder.glob("*.json")))

    # Leere Liste fuer alle Kommentarsegmente.
    all_segments =  []

    # Jede JSON-Datei einlesen und Spielnamen und Halbzeit
    # aus dem Dateinamen bestimmen.
    for file in files:

        with open(file, "r", encoding="utf-8") as f:

            # Parst den Inhalt und speichert es ab.
            segments = json.load(f)

        # Mit regex den Match-Namen und die Halbzeit prüfen.
        match = re.fullmatch(
            r"^\d+_([A-Z]{3}_[A-Z]{3})_(first|second)_half\.json$",
            file.name)

        if match is not None:

            # Die beiden Gruppen zuordnen.
            game = match.group(1)
            half = match.group(2)

            # Wandelt den Text in die passende Zahl um.
            if half == "first":
                half = 1

            else:
                half = 2

        # [Q_3]
        # Manuell eigene Fehlermeldung ausloesen und Schleife abbrechen.    
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



    return df
