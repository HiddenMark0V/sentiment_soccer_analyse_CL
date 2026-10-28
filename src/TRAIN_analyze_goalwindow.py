from pathlib import Path
import pandas as pd

# Pfad bestimmen.
project_root = Path(__file__).resolve().parent.parent

# df = Sentiment klassifizierten Kommentare.
df = pd.read_csv(project_root/ "outputs" / "sentiment_comments.csv")

# goals = Reale Tore als Referenzwert fuer die Analyse.
goals = pd.read_csv(project_root / "data" / "metadata" / "goals.csv")

# splits = Zuordnungsuebersicht der aufgeteilten Spiele in TRAIN/TEST.
splits = pd.read_csv(project_root / "data" / "metadata" / "game_split.csv")

# Aus den 39 verfuegbaren Spielen nur die 20 von TRAIN verwenden und als Menge speichern.
train_ids = set(splits.loc[splits["split"] == "train", "match_id"])

# Filtern nach den dazugehoerigen Toren und speichern.
train_goals = goals[goals["match_id"].isin(train_ids)]



# For-Schleife durch jedes Tor:

results = []

# Iteratiion mit goals durch jede Zeile.
for i, goal in train_goals.iterrows():

    # Filtern der dazugehoerigen Kommentare.
    # Gleiches Spiel + gleiche Halbzeit.
    comments = df[(df["match_id"] == goal["match_id"]) & (df["half"] == goal["half"])]

    # goal_time_half_sec = Zeitpunkt des Tores in Sekunden seit Beginn der Halbzeit.
    goal_time = goal["goal_time_half_sec"]

    # Zwei Zeitfenster um den Torzeitpunkt herum festlegen: 2 Min vor und nach einem Tor.
    # - 120 Sek. vor einem Tor und + 120 Sek. nach einem Tor.
    # >= schließt die Untergrenze mit ein und < die Obergrenze aus.
    before_goal = comments[(comments["time_half_sec"] >= goal_time - 120) &
                           (comments["time_half_sec"] < goal_time)]

    after_goal = comments[(comments["time_half_sec"] >= goal_time) &
                           (comments["time_half_sec"] < goal_time + 120)]

    # Wenn Tore keine Kommentare enthalten. ueberspringen.
    if before_goal.empty or after_goal.empty:
        continue

    # Berechnung der Mittelwerte der Sentiment Scores der jeweiligen Zeitfenster.
    mean_before_goal = before_goal["sentiment_score"].mean() 
    mean_after_goal = after_goal["sentiment_score"].mean()

    # Ergebnisse pro Tor speichern.
    results.append({
        "match_id": goal["match_id"],
        "half": goal["half"],
        "minute": goal["minute"],
        "n_before_goal": len(before_goal),
        "n_after_goal": len(after_goal),
        "mean_before_goal": mean_before_goal,
        "mean_after_goal": mean_after_goal,
        "diff":mean_after_goal - mean_before_goal
    })

# Als df abspeichern.
df_goalwindows = pd.DataFrame(results)


# Kontrollausgaben:
print("Tore in den TRAIN-Spielen:", len(train_goals))
print("Tore fuer die Analyse:", len(df_goalwindows))
print(df_goalwindows["diff"].describe())
print(df_goalwindows.head(10))

# Ergebnisse als CSV unter outputs/ speichern.
df_goalwindows.to_csv(project_root / "outputs" / "TRAIN_goal_windows.csv", index=False)