from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

import fast_zero.security
from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)

router = APIRouter()
router = APIRouter(prefix='/todos', tags=['todos'])


CurrentUser = Annotated[User, Depends(fast_zero.security.get_current_user)]
Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session,
):
    db_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(
    session: Session,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int,
    session: Session,
    user: CurrentUser,
    todo: TodoUpdate,
):
    db_todo = session.scalar(select(Todo).where(Todo.id == todo_id))

    if not db_todo:
        raise HTTPException(status_code=404, detail='Task not found')

    if db_todo.user_id != user.id:
        raise HTTPException(status_code=403, detail='Not authorized')

    for field, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, field, value)

    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(
    todo_id: int,
    session: Session,
    user: CurrentUser,
):
    db_todo = session.scalar(select(Todo).where(Todo.id == todo_id))

    if not db_todo:
        raise HTTPException(status_code=404, detail='Task not found')

    if db_todo.user_id != user.id:
        raise HTTPException(status_code=403, detail='Not authorized')

    session.delete(db_todo)
    session.commit()

    return {'detail': 'Task has been deleted successfully'}
