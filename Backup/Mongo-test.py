#!/usr/bin/python3

import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students
student = {
    'id': 2018000324,
    'name': 'Jordan',
    'age': 27,
    'gender': 'male'
}
result = collection.insert_one(student)
print(result)
print(result.inserted_id)

student1 = {
    'id': 2018000235,
    'name': 'Mike',
    'age': 24,
    'gender': 'male'
}

student2 = {
    'id': 2018000178,
    'name': 'julia',
    'age': 22,
    'gender': 'female'
}

result = collection.insert_many([student1, student2])
print(result)
print(result.inserted_ids)

rows = collection.find({'age': {'$gt': 20}})
for row in rows:
    print(row)