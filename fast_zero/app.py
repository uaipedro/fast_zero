from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    Token,
    UserList,
    UserPartial,
    UserPublic,
    UserSchema,
)
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
)
from fast_zero.security import verify_password
from fast_zero.routes import static

app = FastAPI()

app.include_router(static.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


database = []  # database in memory


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def list_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserPartial,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    for field, value in user.model_dump(exclude_unset=True).items():
        if field == 'password':
            value = get_password_hash(value)
        setattr(current_user, field, value)

    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}')
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'detail': 'User deleted'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
