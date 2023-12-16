from sqlalchemy import select
from fast_zero.database import get_session
from fast_zero.models import User


def test_get_session():
    # Assuming you have imported the necessary dependencies and set up the engine

    # Call the function and get the session object
    session = next(get_session())

    # Assert that the session object is not None
    assert session is not None


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
    assert user.password == 'secret'
    assert user.email == 'teste@test'
