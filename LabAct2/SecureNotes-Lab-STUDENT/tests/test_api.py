"""API behaviour tests.

ONE example is written for you. Replace each `assert False` TODO with a real test.
Use the helpers from conftest:  login(client, user, pw) -> token,  auth(token) -> header.
Ask for the `client` fixture by adding it as a parameter (it gives you a fresh DB each time).

Run the suite:   pytest -q
Run one file:    pytest tests/test_api.py -q
"""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


# ----- TODO 1 -------------------------------------------------------------
def test_register_then_login(client):
    reg = client.post("/register", json={"username": "Jon", "password": "Jonnn_@123408765"})
    assert reg.status_code == 200
    res = login(client, "Jon", "Jonnn_@123408765")
    # Register a new user, then log in as that user.
    # Assert login returns 200 AND the access_token looks like a JWT
    # (three dot-separated parts: token.count(".") == 2).
    assert res is not None and res.count(".") == 2 


# ----- TODO 2 -------------------------------------------------------------
def test_login_wrong_password_is_401(client):
    # Log in as 'alice' with the WRONG password. Assert the status code is 401.
    res = client.post("/login", json={"username": "alice", "password": "123344345"})
    assert res.status_code == 401


# ----- TODO 3 -------------------------------------------------------------
def test_create_then_list_own_note(client):
    # Log in as alice, POST a new note, then GET /notes and assert the new
    # note's title appears in the list.
    login_token = login(client, "alice", "alicepass")
    new_note = client.post("/notes", headers=auth(login_token), json={"title": "newTitle1", "body": "This is a new not"})
    assert new_note.status_code == 200
    res = client.get("/notes", headers=auth(login_token))
    assert res.status_code == 200
    assert new_note.json()["title"] in [r["title"] for r in res.json()]
