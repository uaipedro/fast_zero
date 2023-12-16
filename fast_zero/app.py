from fastapi import FastAPI
from fast_zero.routes import static, users, auth

app = FastAPI()

app.include_router(static.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
