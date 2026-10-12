
from datetime import datetime, timedelta


def test_get_events(client):
    response = client.get('/events')

    assert response.status_code == 200, response.json()
    assert response.json()['events'] == []


def test_get_event_not_found(client):
    response = client.get('/events/9999')

    assert response.status_code == 404, response.json()


def test_events_wrong_status(client):
    response = client.get('/events', params={'status': 'wrong'})

    assert response.status_code == 422, response.json()


def test_create_event_without_token(client):
    event_data = {
        'title': 'Python Meetup',
        'description': 'Backend meeting',
        'address': 'Moscow',
        'date_and_time_of_event': (datetime.now() + timedelta(days=30)).isoformat(),
        'max_participants': 10
    }

    response = client.post('/events', json=event_data)

    assert response.status_code == 401, response.json()


def test_create_event_as_user(client):
    reg_response = client.post('/register', json={'username': 'sans', 'email': 'sans@mail.com', 'password': 'ererer'})
    log_response = client.post('/login', data={'username': 'sans', 'password': 'ererer'})

    assert reg_response.status_code == 200, reg_response.json()
    assert log_response.status_code == 200, log_response.json()

    access_token = log_response.json()['access_token']

    event_data = {
        'title': 'Python Meetup',
        'description': 'Backend meeting',
        'address': 'Moscow',
        'date_and_time_of_event': (datetime.now() + timedelta(days=30)).isoformat(),
        'max_participants': 10
    }

    response = client.post('/events', json=event_data, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 403, response.json()
