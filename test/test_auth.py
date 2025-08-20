import json
from app import create_app
from app.extensions import db


def setup_app():
    app = create_app('development')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'WTF_CSRF_ENABLED': False,
        'CACHE_TYPE': 'NullCache'
    })
    with app.app_context():
        db.create_all()
    return app


def test_register_and_login():
    app = setup_app()
    client = app.test_client()

    # Register
    r = client.post('/auth/register', json={'email': 'a@a.com', 'password': '12345678'})
    assert r.status_code == 201

    # Login
    r = client.post('/auth/login', json={'email': 'a@a.com', 'password': '12345678'})
    assert r.status_code == 200
    tokens = r.get_json()
    assert 'access_token' in tokens