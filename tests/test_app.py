fake_user = {
    'username': 'alice',
    'email': 'alice@example.com',
    'password': 'secret',
}
fake_user_with_id = {
    'id': 1,
    'username': 'alice',
    'email': 'alice@example.com',
}


def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json=fake_user,
    )

    assert response.status_code == 201
    assert response.json() == fake_user_with_id


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}

    client.post(
        '/users/',
        json=fake_user,
    )

    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': [fake_user_with_id]}


def test_update_user(client):
    response = client.post(
        '/users/',
        json=fake_user,
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }

    response = client.put('/users/1', json={'username': 'bob'})

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'alice@example.com',
    }


def test_delete_user(client):
    response = client.post(
        '/users/',
        json=fake_user,
    )

    assert response.status_code == 201

    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}

    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_should_return_404_when_updating_invalid_id(client):
    response = client.put('/users/1', json={'username': 'bob'})

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_should_return_404_when_deleting_invalid_id(client):
    response = client.delete('/users/1')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
