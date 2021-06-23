"""
In this file all test concerning news routes.py are included.
"""
import json


def test_homepage(client):
    response = client.get('/home')
    assert response.status_code == 200


def test_get_news_with_sentiment__without_jwt(client):
    response = client.get("/news/sentiments", json={"q": "covid"})
    json_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 401
    assert json_data == {'msg': 'Missing Authorization Header'}


def test_get_news_with_sentiment__with_jwt(client):
    res = client.post('/users/login', json={"username": "user3",
                                            "password": "password"})
    credentials = res.get_json()["access_token"]
    access_headers = {"Authorization": f"Bearer {credentials}"}
    response = client.get('/news/sentiments',
                          headers=access_headers,
                          json={"q": "covid-19",
                                "sources": "cnn, bbc-news"})
    assert response.status_code == 201


def test_get_news_with_sentiment__with_jwt_no_input(client):
    res = client.post('/users/login', json={"username": "user3",
                                            "password": "password"})
    credentials = res.get_json()["access_token"]
    access_headers = {"Authorization": f"Bearer {credentials}"}
    response = client.get('/news/sentiments',
                          headers=access_headers)
    assert response.status_code == 400
    assert response.json == {"message": "No input detected"}


def test_get_positive_news__with_jwt(client):
    res = client.post('/users/login', json={"username": "user3",
                                            "password": "password"})
    credentials = res.get_json()["access_token"]
    access_headers = {"Authorization": f"Bearer {credentials}"}
    response = client.get('/news/good-news',
                          headers=access_headers,
                          json={"sources": "cnn"})
    assert response.status_code == 201


def test_get_news_emotions__with_jwt(client):
    res = client.post('/users/login', json={"username": "user3",
                                            "password": "password"})
    credentials = res.get_json()["access_token"]
    access_headers = {'Authorization': f'Bearer {credentials}'}
    response = client.get('/news/emotions',
                          headers=access_headers,
                          json={"q": "bitcoin",
                                "sources": "cnn, bbc-news"})
    assert response.status_code == 201


def test_get_happy_news(client):
    res = client.post('/users/login', json={"username": "user3",
                                            "password": "password"})
    credentials = res.get_json()["access_token"]
    access_headers = {"Authorization": f"Bearer {credentials}"}
    response = client.get('/news/happy-news',
                          headers=access_headers,
                          json={"sources": "cnn"})
    assert response.status_code == 201


def test_get_all_news_emotions_metadata(client):
    res = client.post('/users/login', json={"username": "user3",
                                            "password": "password"})
    credentials = res.get_json()["access_token"]
    access_headers = {'Authorization': f'Bearer {credentials}'}
    response = client.get('/news/emotions-metadata', headers=access_headers)
    assert response.status_code == 200


def test_get_all_news_sentiments_metadata(client):
    res = client.post('/users/login', json={"username": "admin",
                                            "password": "password"})
    credentials = res.get_json()["access_token"]
    access_headers = {'Authorization': f'Bearer {credentials}'}
    response = client.get('/news/sentiments-metadata', headers=access_headers)
    assert response.status_code == 200

