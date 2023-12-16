from fast_zero.schemas import UserPublic


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


def test_create_user(client):
    response = client.post(
        '/users/',
        json=fake_user,
    )

    assert response.status_code == 201
    assert response.json() == fake_user_with_id


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'bob'},
    )

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'teste@test.com',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}

    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_should_return_400_when_updating_other_user(client, user, token):
    response = client.put(
        '/users/5',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'bob'},
    )

    assert response.status_code == 400


def test_should_return_400_when_deleting_other_user(client, user, token):
    response = client.delete(
        '/users/5',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 400


def test_should_return_400_when_creating_user_with_existing_username(
    client, user
):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'testando@outroemail.com',
            'password': 'outro_password',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already registered'}
