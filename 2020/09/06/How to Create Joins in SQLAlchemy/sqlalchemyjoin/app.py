from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    name = db.Column(db.String(50))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    name = db.Column(db.String(50))
    salary = db.Column(db.Integer)

results = db.session.query(Employee, Department).join(Department).all()

for employee, department in results:
    print(employee.name, department.name)

results = db.session.query(Employee, Department, Company). \
    select_from(Employee).join(Department).join(Company).all()

for employee, department, company in results:
    print(employee.name, department.name, company.name)

results = db.session.query(Employee.name, Employee.salary).join(Department).join(Company). \
    filter(Department.id == 1).all()

for result in results:
    print(result)

'''
company1 = Company(name='Acme')
company2 = Company(name='Steel Industries')
company3 = Company(name='Tech Solutions')
company4 = Company(name='Generic Food')
db.session.add_all([company1,company2,company3,company4])
db.session.commit()

dep1 = Department(name='Sales',company_id=1)
dep2 = Department(name='Human Resources',company_id=1)
dep3 = Department(name='Accounting',company_id=1)

dep4 = Department(name='Receiving',company_id=2)
dep5 = Department(name='Finance',company_id=2)
dep6 = Department(name='Engineering',company_id=2)

dep7 = Department(name='Quality Assurance',company_id=3)
dep8 = Department(name='Information Technology',company_id=3)
dep9 = Department(name='Office Support',company_id=3)

dep10 = Department(name='Food Processing',company_id=4)
dep11 = Department(name='Customer Support',company_id=4)
dep12 = Department(name='Shipping',company_id=4)

db.session.add_all([dep1, dep2, dep3, dep4, dep5, dep6, dep7, dep8, dep9, dep10, dep11, dep12])
db.session.commit()

import csv
with open('MOCK_DATA.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for c in csv_reader:
        em = Employee(name=c['name'], salary=c['salary'], department_id=c['department_id'])
        db.session.add(em)
    db.session.commit()
'''