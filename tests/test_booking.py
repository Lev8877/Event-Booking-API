
def test_get_bookings_without_token(client):
    response = client.get('/bookings')

    assert response.status_code == 401, response.json()


def test_get_my_bookings_empty(client):
    reg_response = client.post('/register', json={'username': 'sans', 'email': 'sans@mail.com', 'password': 'ererer'})
    log_response = client.post('/login', data={'username': 'sans', 'password': 'ererer'})

    assert reg_response.status_code == 200, reg_response.json()
    assert log_response.status_code == 200, log_response.json()

    access_token = log_response.json()['access_token']
    response = client.get('/bookings', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200, response.json()
    assert response.json()['bookings'] == []


def test_booking_without_token(client):
    response = client.post('/events/9999/bookings')

    assert response.status_code == 401, response.json()


def test_booking_event_not_found(client):
    reg_response = client.post('/register', json={'username': 'sans', 'email': 'sans@mail.com', 'password': 'ererer'})
    log_response = client.post('/login', data={'username': 'sans', 'password': 'ererer'})

    assert reg_response.status_code == 200, reg_response.json()
    assert log_response.status_code == 200, log_response.json()

    access_token = log_response.json()['access_token']
    response = client.post('/events/9999/bookings', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 404, response.json()


def test_delete_booking_not_found(client):
    reg_response = client.post('/register', json={'username': 'sans', 'email': 'sans@mail.com', 'password': 'ererer'})
    log_response = client.post('/login', data={'username': 'sans', 'password': 'ererer'})

    assert reg_response.status_code == 200, reg_response.json()
    assert log_response.status_code == 200, log_response.json()

    access_token = log_response.json()['access_token']
    response = client.delete('/bookings/9999', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 404, response.json()
