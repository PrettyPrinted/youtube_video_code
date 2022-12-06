import responses 
import re

from flask import url_for

from project.models import User
from playwright.sync_api import expect

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

def test_take_screenshot(live_server, page):
    page.goto(url_for('main.index', _external=True))

    page.screenshot(path="screenshots/home.png")

def test_home_page_loads(live_server, page):
    page.goto(url_for('main.index', _external=True))

    expect(page).to_have_title("Home")

def test_register_login_add_city(live_server, page):
    page.goto(url_for('main.index', _external=True))

    # Register
    page.get_by_role("button", name="Register").click()

    expect(page).to_have_title("Register")

    page.get_by_placeholder("Email").click()
    page.get_by_placeholder("Email").fill("test@test.com")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("password")
    page.get_by_role("button", name="Register").click()

    expect(page).to_have_title("Home")

    # Login
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_title("Login")
    page.get_by_placeholder("Email").click()

    page.get_by_placeholder("Email").fill("test@test.com")
    page.get_by_placeholder("Email").press("Tab")
    page.get_by_placeholder("Password").fill("password")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_title("Home")


    # Add a city
    page.get_by_role("button", name="City").click()

    expect(page).to_have_title("City")

    page.get_by_placeholder("City").click()
    page.get_by_placeholder("City").fill("Ottawa")
    page.get_by_role("combobox").select_option("2")
    page.get_by_role("button", name="Add City").click()

    expect(page.locator('body')).to_have_text(re.compile("Ottawa, Canada"))