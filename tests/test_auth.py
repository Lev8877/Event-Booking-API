
def test_api(client):
    response = client.get('/me')

    assert response.status_code == 401


def test_register(client):
    response = client.post('/register', json={})

    assert response.status_code == 422


def test_register_success(client):
    response = client.post('/register', json={'username': 'sans', 'email': 'ketchuplover@mail.com', 'password': 'ererer'})
    data = response.json()

    assert response.status_code == 200, response.json()
    assert data['username'] == 'sans'
    assert data['email'] == 'ketchuplover@mail.com'


def test_register_error(client):
    fresponse = client.post('/register', json={'username': 'sans', 'email': 'ketchuplover@mail.com', 'password': 'ererer'})
    sresponse = client.post('/register', json={'username': 'papyrus', 'email': 'ketchuplover@mail.com', 'password': 'ererer'})

    assert fresponse.status_code == 200, fresponse.json()
    assert sresponse.status_code == 409, sresponse.json()


def test_login_success(client):
    reg_response = client.post('/register', json={'username': 'sans', 'email': 'ketchuplover@mail.com', 'password': 'ererer'})
    log_response = client.post('/login', data={'username': 'sans', 'password': 'ererer'})

    assert log_response.status_code == 200, log_response.json()
    assert reg_response.status_code == 200, reg_response.json()
    assert 'access_token' in log_response.json()
    assert log_response.json()['token_type'] == 'bearer'


def test_login_wrong_password(client):
    reg_response = client.post('/register', json={'username': 'sans', 'email': 'ketchuplover@mail.com', 'password': 'ererer'})
    log_response = client.post('/login', data={'username': 'sans', 'password': '(=)'})

    assert reg_response.status_code == 200, reg_response.json()
    assert log_response.status_code == 401, log_response.json()


def test_me_authorized(client):
    reg_response = client.post('/register', json={'username': 'sans', 'email': 'ketchuplover@mail.com', 'password': 'ererer'})
    log_response = client.post('/login', data={'username': 'sans', 'password': 'ererer'})

    assert reg_response.status_code == 200, reg_response.json()
    assert log_response.status_code == 200, log_response.json()

    reg_data = reg_response.json()
    log_data = log_response.json()
    access_token = log_data['access_token']

    me_response = client.get('/me', headers={'Authorization': f'Bearer {access_token}'})
    me_data = me_response.json()

    assert me_response.status_code == 200, me_response.json()
    assert me_data['username'] == reg_data['username']
    assert me_data['email'] == reg_data['email']


def test_register_username_error(client):
    fresponse = client.post('/register', json={'username': 'sans', 'email': 'sans@mail.com', 'password': 'ererer'})
    sresponse = client.post('/register', json={'username': 'sans', 'email': 'papyrus@mail.com', 'password': 'ererer'})

    assert fresponse.status_code == 200, fresponse.json()
    assert sresponse.status_code == 409, sresponse.json()


def test_login_wrong_username(client):
    reg_response = client.post('/register', json={'username': 'sans', 'email': 'sans@mail.com', 'password': 'ererer'})
    log_response = client.post('/login', data={'username': 'papyrus', 'password': 'ererer'})

    assert reg_response.status_code == 200, reg_response.json()
    assert log_response.status_code == 401, log_response.json()


def test_me_invalid_token(client):
    response = client.get('/me', headers={'Authorization': 'Bearer wrong_token'})

    assert response.status_code == 401, response.json()
