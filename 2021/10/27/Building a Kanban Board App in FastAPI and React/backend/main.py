import jwt

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from pydantic import BaseModel
from tortoise import fields 
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model 

JWT_SECRET = 'myjwtsecret'

app = FastAPI()

class Task(BaseModel):
    id: str
    content: str

class Tasks(BaseModel):
    __root__: dict[str, Task]

class Column(BaseModel):
    id: str
    title: str
    taskIds: list

class Columns(BaseModel):
    __root__: dict[str, Column]

class Board(BaseModel):
    tasks: Tasks
    columns: Columns
    columnOrder: list


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    board_data = fields.JSONField(default='{"tasks": {}, "columns": {}, "columnOrder": []}')

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True, exclude=('board_data',))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return await User_Pydantic.from_tortoise_orm(user)

@app.get("/board")
async def get_board(user: User_Pydantic = Depends(get_current_user)):
    return {'board': user.board_data}


@app.post("/board")
async def save_board(board: Board, user: User_Pydantic = Depends(get_current_user)):
    user = await User.get(id=user.id)
    user.board_data = board.json()
    await user.save()

    return {"status": "success"}

@app.post('/users')
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    user_obj_py = await User_Pydantic.from_tortoise_orm(user_obj)
    token = jwt.encode(user_obj_py.dict(), JWT_SECRET)
    return {'access_token' : token, 'token_type' : 'bearer'}

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {'access_token' : token, 'token_type' : 'bearer'}

register_tortoise(
    app, 
    db_url='postgres://postgres:Password1@127.0.0.1:5432/postgres',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)