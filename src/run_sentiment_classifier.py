from germansentiment import SentimentModel
from pathlib import Path

# Importieren der JSON-Loader Funktion.
from src.json_loader import load_soccer_comments

# Alle Kommentare als df einlesen.
df = load_soccer_comments()

# [Q_5]
# Laden des German Sentimentmodels.
model = SentimentModel()

#### Batch-Schleife ####
# Ueberbelastung der RAM soll verhindert werden, daher soll das Modell
# die Kommentare in Paketen von jeweils 42 verarbeiten.
batch_size = 42
all_labels = []
all_probs = []

# Beginnt bei 0, hoert bei len(df) auf und geht in 42er Schritten.
for start in range(0, len(df), batch_size):

    # Extrahiert die texte des aktuellen Blocks; mit .iloc nach Postionen.
    # predict_sentiment erwartet eime Liste, daher .tolist().
    texts = df["text"].iloc[start:start + batch_size].tolist()

    # Modell klassifiziert alle Texte des jeweiligen Blocks.
    # output_probabilities auf True gesetzt, damit Wahrscheinlichkeiten ausgegeben werden.
    labels, probabilities = model.predict_sentiment(texts, output_probabilities=True)

    # Elemente der Liste werden an die Gesamtlisten angehaengt.
    # .extend() statt .append(): .extend() fuegt jedes Element einzeln
    # an.
    all_labels.extend(labels)
    all_probs.extend(probabilities)

# zur Kontrolle:
# es sind bei den drei Ausgaben 32668 zu erwarten.
print("Kommentare:", len(df))
print("Labels", len(all_labels))
print("Wahrscheinlichkeiten:", len(all_probs))

#######################################################

# Listen initialisieren fuer die drei Sentimentklassen.
positive_class = []
negative_class = []
neutral_class = []

# Je Sentimentklasse eine Liste mit Zahlen erstellen fuer das df.
for probs in all_probs:

    # Tupelliste in ein Dict umwandeln.
    # Zugriff soll ueber den Namen der Sentimentklasse erfolgen.
    # [("positive", 0.98), ("negative", 0.01), ("neutral", 0.01)] -> {"positive": 0.98, "negative": 0.01, "neutral": 0.01}
    values = dict(probs)

    # Wahrscheinlichkeiten jeder Klasse in die dazugehoerige Liste.
    positive_class.append(values["positive"])
    negative_class.append(values["negative"])
    neutral_class.append(values["neutral"])

# Sentimentergebnisse als neue Spalten im df speichern.
df["sentiment_labels"] = all_labels
df["prob_positive"] = positive_class
df["prob_negative"] = negative_class
df["prob_neutral"] = neutral_class


# "Der Sentimentscore": P(positiv) - P(negativ)
df["sentiment_score"] = df["prob_positive"] - df["prob_negative"]


# Kontrolle
print(df.shape)
print(df[["text", "sentiment_labels", "sentiment_score"]].head())

############

# Projektordner bestimmen.
project_root = Path(__file__).resolve().parent.parent

output_folder = project_root / "outputs"
output_folder.mkdir(parents=True, exist_ok=True)

# df als CSV speichern.
df.to_csv(output_folder / "sentiment_comments.csv", index=False)


