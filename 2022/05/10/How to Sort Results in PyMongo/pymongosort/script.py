from pymongo import MongoClient
from faker import Faker

client = MongoClient('mongodb://root:example@localhost:27017/')
db = client.example
users_collection = db.courses
'''
fake = Faker()
users = []

for _ in range(3000):
    user = fake.simple_profile()
    user["birthdate"] = user["birthdate"].strftime("%Y-%m-%d")
    users.append(user)

users_collection.insert_many(users)
'''

users = users_collection.find().sort([("birthdate", -1), ("_id", 1)]).limit(10)
for user in users:
    print(user)