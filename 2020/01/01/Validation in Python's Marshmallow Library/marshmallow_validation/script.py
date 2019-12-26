from marshmallow import Schema, fields, post_load, ValidationError, validates, validate

class Person:
    def __init__(self, name, age, email):
        self.name = name 
        self.age = age
        self.email = email

    def __repr__(self):
        return f'{ self.name } is { self.age } years old.'


class PersonSchema(Schema):
    name = fields.String(validate=validate.Length(max=5))
    age = fields.Integer()
    email = fields.Email()
    location = fields.String(required=False)

    @validates('age')
    def validate_age(self, age):
        if age > 200:
            raise ValidationError('The age is too old!')

    @post_load
    def create_person(self, data, **kwargs):
        return Person(**data)

input_data = {}

input_data['name'] = input('What is your name? ')
input_data['age'] = input('What is your age? ')
input_data['email'] = input('What is your email? ')

try:
    schema = PersonSchema()
    person = schema.load(input_data)

    #person = Person(name=input_data['name'], age=input_data['age'])

    #print(person)

    result = schema.dump(person)

    print(result)
except ValidationError as err:
    print(err)
    print(err.valid_data)