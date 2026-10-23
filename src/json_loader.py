import json

with open("C:\\Users\\Egehan\\Code\\01_uni\\projects\\sentiment_soccer_analyse_CL\\data\\cleaned_data\\Sportschau\\11_TUR_GEO_first_half.json", "r", encoding="utf-8") as file:
    segments = json.load(file)

print(segments)    