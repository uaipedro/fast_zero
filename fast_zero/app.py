from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    UserDB,
    UserList,
    UserPartial,
    UserPublic,
    UserSchema,
)


def create_app():
    app = FastAPI()

    @app.get('/')
    def read_root():
        return {'message': 'Olá Mundo!'}

    database = []  # database in memory

    @app.post('/users/', status_code=201, response_model=UserPublic)
    def create_user(user: UserSchema):
        user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
        database.append(user_with_id)
        return user_with_id

    @app.get('/users/', response_model=UserList)
    def list_users():
        return {'users': database}

    @app.put('/users/{user_id}', response_model=UserPublic)
    def update_user(user_id: int, user: UserPartial):
        if user_id > len(database):
            raise HTTPException(status_code=404, detail='User not found')

        user_with_id = database[user_id - 1].model_dump()
        user_with_id.update(**user.model_dump(exclude_unset=True))
        database[user_id - 1] = UserDB(**user_with_id)

        return user_with_id

    @app.delete('/users/{user_id}')
    def delete_user(user_id: int):
        if user_id > len(database):
            raise HTTPException(status_code=404, detail='User not found')

        database.pop(user_id - 1)
        return {'detail': 'User deleted'}

    return app


app = create_app()
