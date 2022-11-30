import responses 

from project.models import User

def test_home(client):
    response = client.get("/")
    assert b"<title>Home</title>" in response.data


def test_registration(client, app):
    response = client.post("/register", data={"email": "test@test.com", "password": "testpassword"})

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"

@responses.activate
def test_age(client):
    responses.add(
        responses.GET,
        "https://api.agify.io",
        json={"age": 33, "count": 1049384, "name": "Anthony"},
        status=200
    )
    client.post("/register", data={"email": "test@test.com", "password": "testpassword"})
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})

    response = client.post("/age", data={"name": "Anthony"})

    assert b"You are 33 years old" in response.data

def test_invalid_login(client):
    client.post("/login", data={"email": "test@test.com", "password": "testpassword"})

    response = client.get("/city")

    assert response.status_code == 401