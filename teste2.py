import json

with open('db/faces.json') as json_file:
    db = json.load(json_file)

print(json.dumps(db, indent = 2))
print(db[0]["face_0"])
print(db[0]["face_0"][1])
with open('db/faces.json', 'w') as outfile:
    json.dump(db, outfile)