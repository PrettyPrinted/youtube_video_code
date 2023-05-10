from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .api_models import course_model, student_model, course_input_model, student_input_model, user_model, login_model
from .extensions import db
from .models import Course, Student, User

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
ns = Namespace("api", authorizations=authorizations)

@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}

@ns.route("/courses")
class CourseListAPI(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")
    @ns.marshal_list_with(course_model)
    def get(self):
        return Course.query.filter_by(instructor=current_user).all()

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def post(self):
        course = Course(name=ns.payload["name"])
        db.session.add(course)
        db.session.commit()
        return course, 201

@ns.route("/courses/<int:id>")
class CourseAPI(Resource):
    @ns.marshal_with(course_model)
    def get(self, id):
        course = Course.query.get(id)
        return course

    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns.payload["name"]
        db.session.commit()
        return course

    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return {}, 204


@ns.route("/students")
class StudentListAPI(Resource):
    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()

    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def post(self):
        student = Student(name=ns.payload["name"], course_id=ns.payload["course_id"])
        db.session.add(student)
        db.session.commit()
        return student, 201


@ns.route("/students/<int:id>")
class StudentAPI(Resource):
    @ns.marshal_with(student_model)
    def get(self, id):
        student = Student.query.get(id)
        return student

    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def put(self, id):
        student = Student.query.get(id)
        student.name = ns.payload["name"]
        student.course_id = ns.payload["course_id"]
        db.session.commit()
        return student

    def delete(self, id):
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return {}, 204


@ns.route("/register")
class Register(Resource):

    @ns.expect(login_model)
    @ns.marshal_with(user_model)
    def post(self):
        user = User(username=ns.payload["username"], password_hash=generate_password_hash(ns.payload["password"]))
        db.session.add(user)
        db.session.commit()
        return user, 201

@ns.route("/login")
class Login(Resource):

    @ns.expect(login_model)
    def post(self):
        user = User.query.filter_by(username=ns.payload["username"]).first()
        if not user:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(user.password_hash, ns.payload["password"]):
            return {"error": "Incorrect password"}, 401
        return {"access_token": create_access_token(user)}