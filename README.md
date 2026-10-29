# Ereigniszentrierte Sentimentanalyse deutschsprachiger Fußball-Livekommentare
- Kurs: Computerlinguistische Programmierung (050042-SoSe 2026)
- Name: Egehan Cakar
- Martrikelnummer: 108017106965
- Abgabe: 31.10.2026

## Projektziel
Untersuchung von Sentimentveränderungen in Fußball Livekommentaren im zeitlichen Umfeld von geschossenen Toren.

## Datengrundlage
- Hauptdatensatz: **SocCor: A Multimodal-based Multilingual Soccer Corpus for Text Data Analytics** (https://github.com/PaulLoehr/SocCor)
  - Notwendig: Die transkribierten deutschen Sportschau-Kommentare unter cleaned_data: ![SocCor/Textdata/cleaned_data/Games/Sportschau](https://github.com/PaulLoehr/SocCor/tree/main/SocCor/Textdata/cleaned_data/Games/Sportschau)

- Referenzdatensatz für die Spielergebnisse: **Free open public domain football data in the JSON format** (https://github.com/openfootball/euro.json/tree/master?tab=readme-ov-file)
  - Notwendig: Die Spiele von der EM 2027: ![2024/euro.json](https://github.com/openfootball/euro.json/blob/master/2024/euro.json)
 
## Projektstruktur

### Übersicht
```
sentiment_soccer_analyse_CL/
├── data/
│   ├── cleaned_data/
│   │   └── Sportschau/
│   ├── metadata/    
│   │   ├── euro2024_gamescores_raw.json
│   │   └── goals.csv
│   └── raw_data    
│      
├── docs/         
│   ├── ACL_paper.pdf       
│   ├── quellen.md      
│   └── KI_dokumentation.md 
├── outputs/    
│   ├── goal_windows.csv     
│   └── sentiment_comments.csv    
└── src/       
    ├── analyze_goalwindow.py    
    ├── create_goals_references.py    
    ├── json_loader.py   
    └── run_sentiment_classifier.py    
       
       

```
### Anmerkungen
- Die relevanten SocCor-Daten für dieses Projekt müssen unter ```data/cleaned_data/Sportschau/``` liegen.
- Unter ```data/metadata/```: Daten die zur Referenz herangezogen werden, wie z. B. Tore.
- Unter ```docs/```: relevante Dokumente zu diese Projekt; unteranderem auch das CL-Paper.
- Unter ```outputs/```: Sentimentergebnisse und Berechnungen der Sentimentveränderungen im zeitlichen Umfeld von Toren.
- Unter ```src/```: Die Python Skripte.

## Voraussetzungen und Installation

- Python 3.11.9
- Virtuelle Umgebung muss zu Beginn erstellt werden

- Beachtung der requirements.txt Liste
```
pandas == 3.1.0

germansentiment == 1.1.0

transformers == 4.57.6

torch == 2.14.1

matplotlib == 3.11.2
```
### Installieren der Bibliotheken

```
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### SocCor-Daten einrichten
Nach dem Download der SocCor-Daten sollte die im folgenden Ordner liegen:
```
data/
└── cleaned_data/
    └── Sportschau/
        ├── 47_NED_TUR_first_half.json
        ├── ...
        └── [weitere Halbzeit-Dateien]
```
- Es müssten 78 JSON-Dateien vorliegen.
- Wenn alles richtig installiert wurde, dann kann man mit dem ```json_loader.py``` testen, ob alle Daten vorliegen:
  ```
  .\.venv\Scripts\python.exe -c "from src.json_loader import load_soccer_comments; print(load_soccer_comments().shape)"
  ```
  Die Ausgabe die erwartet wird: (32668, 6)

## Durchführung der Analyse
Falls die Analyse ebenfalls durchgeführt werden soll, dann kann die folgende Reihenfolge beachtet werden.
Die erstellten Outputs, die bei der Analyse entstanden sind, werden unter ```data/metadata/``` und ```outputs/``` in diesem Git-Repo mit gepusht und zur Verfügung gestellt. Das sollte beachtet werden, wenn durch das Ausführen der Skripte Outputs erstellt werden.
  
1. Erstellung der Torreferenzen: ```create_goals_references.py```
```
.\.venv\Scripts\python.exe -m src.create_goals_references
  ```
Output: Erstellt ```data/metadata/goals.csv``` mit 85 Torreferenzen.



2. Sentimentklassifikation: ```run_sentiment_classifier.py```
```
.\.venv\Scripts\python.exe -m src.run_sentiment_classifier
```



Das Skript verwendet das Sentimentmodell von ![oliverguhr/german-sentiment-bert](https://github.com/oliverguhr/german-sentiment) und klassifiziert alle 32.668 Kommentarsegmente. 

Output:  Erstellt ```outputs/sentiments_comments.csv```. Die Datei enthält 32.668 Zeilen und 11 Spalten. Darunter Sentimentlabels, Wahrscheinlichkeiten und selbst berechneter "Sentimentscore".

**Kleine Warnung vorab**: Diese Sentimentklassifizierung war bei mir sehr rechenintensiv und hat um die 2-3 Stunden gedauert. Auch dieser Output liegt diesem Git-Repo bei.



3. Analyse der Sentimentveränderungen: ```analyze_goalwindow.py```
```
.\.venv\Scripts\python.exe -m src.analyze_goalwindow
```
Vergleicht für jedes auswertbare Tore den mittleren "Sentimentscore" der Kommentare innerhalb von 120 Sekunden vor und nach dem angenäherten Torzeitpunkt.

Output: Erstellt ```outputs/goal_windows.csv```.

Es werden von den 39 Spielen und den 85 Toren, 83 Tore ausgewertet (2 Tore wurden nicht berücksichtigt wegen fehlender Kommentare in diesem Zeitfenster).

## Quellen
- SocCor: A Multimodal-based Multilingual Soccer Corpus for Text Data Analytics (2025). Löhr, Paul & Strötgen, Jannik. Korpus: https://github.com/PaulLoehr/SocCor/tree/main. Paper: https://aclanthology.org/2025.konvens-1.8.pdf.
- Broad-Coverage German Sentiment Classification Model for Dialog Systems (2020). Guhr, Oliver  and  Schumann, Anne-Kathrin  and  Bahrmann, Frank  and  Böhme, Hans Joachim. Modell: https://github.com/oliverguhr/german-sentiment. Paper: https://aclanthology.org/2020.lrec-1.202.pdf.
