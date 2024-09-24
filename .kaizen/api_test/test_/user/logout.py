import pytest
import requests

# Test scenario: Successful logout of a logged-in user
def test_logout_success():
    # Login a user to obtain a valid session
    login_response = requests.post('/user/login', json={'username': 'test_user', 'password': 'test_password'})
    assert login_response.status_code == 200
    session_cookie = login_response.cookies.get('session_id')

    # Logout the user
    logout_response = requests.get('/user/logout', cookies={'session_id': session_cookie})
    assert logout_response.status_code == 200
    assert logout_response.json() == {'message': 'successful operation'}

# Test scenario: Logout without a valid session
def test_logout_without_session():
    logout_response = requests.get('/user/logout')
    assert logout_response.status_code == 401
    assert logout_response.json() == {'error': 'Unauthorized'}

# Test scenario: Logout with an invalid session
def test_logout_with_invalid_session():
    logout_response = requests.get('/user/logout', cookies={'session_id': ' invalid_session_id'})
    assert logout_response.status_code == 401
    assert logout_response.json() == {'error': 'Unauthorized'}

# Test scenario: Logout with an expired session
def test_logout_with_expired_session():
    # Login a user to obtain a valid session
    login_response = requests.post('/user/login', json={'username': 'test_user', 'password': 'test_password'})
    assert login_response.status_code == 200
    session_cookie = login_response.cookies.get('session_id')

    # Expire the session
    requests.post('/user/logout', cookies={'session_id': session_cookie})

    # Try to logout again with the expired session
    logout_response = requests.get('/user/logout', cookies={'session_id': session_cookie})
    assert logout_response.status_code == 401
    assert logout_response.json() == {'error': 'Unauthorized'}

# Test scenario: Version compatibility
def test_logout_version_compatibility():
    # Login a user to obtain a valid session
    login_response = requests.post('/user/login', json={'username': 'test_user', 'password': 'test_password'})
    assert login_response.status_code == 200
    session_cookie = login_response.cookies.get('session_id')

    # Logout the user with a different API version
    logout_response = requests.get('/user/logout', cookies={'session_id': session_cookie}, headers={'Accept': 'application/vnd.example.v2+json'})
    assert logout_response.status_code == 200
    assert logout_response.json() == {'message': 'successful operation'}