import json 

class User:
    def __init__(self, guid, isActive, name, email, phone, address):
        self.guid = guid
        self.isActive = isActive
        self.first_name = name['first']
        self.last_name = name['last']
        self.email = email 
        self.phone = phone 
        self.address = address

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<User { self.first_name }>'

json_string = '''{
    "guid": "1f1c4ac7-fc36-4008-935b-d87ffc7d8700",
    "isActive": false,
    "name": {
      "first": "Reid",
      "last": "Warren"
    },
    "email": "reid.warren@undefined.name",
    "phone": "+1 (983) 443-3504",
    "address": "359 Rapelye Street, Holtville, Marshall Islands, 9692"
  }'''

#user = User.from_json(json_string)
#print(user)
#print(user.address)
#print(user.email)
#print(user.phone)

users_list = []
with open('data.json', 'r') as json_file:
    user_data = json.loads(json_file.read())
    for u in user_data:
        users_list.append(User(**u))

print(users_list)