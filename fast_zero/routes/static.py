from fastapi import APIRouter, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter(prefix='/static', tags=['static'])

templates = Jinja2Templates(directory='fast_zero/templates')


@router.get('/', response_class=HTMLResponse)
def index(request: Request, hx_request: Optional[str] = Header(None)):
    books = [
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': 'The Trial', 'author': 'Franz Kafka'},
        {'title': 'The Stranger', 'author': 'Albert Camus'},
    ]
    context = {'request': request, 'books': books}
    if hx_request:
        return templates.TemplateResponse('list.html', context)
    return templates.TemplateResponse('index.html', context)
