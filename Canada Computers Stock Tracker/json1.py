import json

f = open('stock.json', 'r')
db = json.load(f)

print(db[0][0])