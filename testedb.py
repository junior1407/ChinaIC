import json
db = []
db.append({})
db[0]["id"] = 0
db[0]["face_0"] = [(1,1),(2,2)]
print(json.dumps(db, indent = 2))
print(db[0]["face_0"])
print(db[0]["face_0"][1])
with open('db/faces.json', 'w') as outfile:
    json.dump(db, outfile)