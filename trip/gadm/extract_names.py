import json, sys

path = sys.argv[1] if len(sys.argv) > 1 else "gadm41_IDN_3.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

for feat in data["features"]:
    p = feat["properties"]
    print(f'{p["NAME_1"]} | {p["NAME_2"]} | {p["NAME_3"]}')
