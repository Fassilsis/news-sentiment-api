"""
In this file all test concerning users routes.py are included.
"""


def test_login_without_registration(client):
    response = client.post('/users/login', json={"username": "user2",
                                                 "password": "password"})
    assert response.status_code == 404
    assert response.json == {"message": "User not found. Please enter a valid username or register!"}


def test_login_with_registration(client):
    response = client.post("/users/login", json={"username": "user1",
                                                 "password": "password"})
    assert response.status_code == 200


def test_login_with_wrong_password(client):
    response = client.post("/users/login", json={"username": "user1",
                                                 "password": "passwor"})
    assert response.status_code == 401
    assert response.json == {"message": "Login Unsuccessful. Please check password"}


def test_logout__logged_in(client):
    client.post("/users/login", json={"username": "user1",
                                      "password": "password"})

    response = client.get("/users/logout")
    assert response.status_code == 200
    assert response.json == {"message": "You are successfully logged out!"}


def test_logout__not_logged_in(client):
    response = client.get("/users/logout")
    assert response.status_code != 200


def test_if_user_has_access_to_others(client):
    client.post("/users/login", json={"username": "user1",
                                      "password": "password"})

    response = client.get("/users/account-management", json={"username": "user2"})
    assert response.status_code == 403
    assert response.json == {"message": "You are not authorised to view this resource."}

    response = client.put("/users/account-management", json={"username": "user2",
                                                             "new_username": "dummy_user1"})
    assert response.status_code == 403
    assert response.json == {"message": "You are not authorised to view this resource."}

    response = client.delete("/users/account-management", json={"username": "user2"})
    assert response.status_code == 403
    assert response.json == {"message": "You are not authorised to view this resource."}


def test_if_users_can_manage_their_own_account(client):
    client.post("/users/login", json={"username": "user3",
                                      "password": "password"})

    response = client.get("/users/account-management", json={"username": "user3"})
    assert response.status_code == 200

    response = client.put("/users/account-management", json={"username": "user3",
                                                             "new_username": "dummy_user3"})
    assert response.status_code == 201
    assert response.json == {"message": "User updated."}

    response = client.delete("/users/account-management", json={"username": "dummy_user3"})
    assert response.status_code == 201
    assert response.json == {"message": "User deleted."}


def test_for_accessing_all_users_info__logged_in_as_admin(client):
    client.post("/users/login", json={"username": "admin",
                                      "password": "password"})

    response = client.get("/users/search")
    assert response.status_code == 200


def test_for_accessing_all_users_info__logged_in_as_user(client):
    client.post("/users/login", json={"username": "user1",
                                      "password": "password"})

    response = client.get("/users/search")
    assert response.status_code == 403
    assert response.json == {"message": "You are not authorised to view this resource."}
