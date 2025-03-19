from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated
from datetime import timedelta
from contextlib import asynccontextmanager
from sqlmodel import Session, SQLModel, select
from api.engine import get_session, engine
from api.models.item import Item, ItemCreate, ItemPublic, ItemUpdate
from api.models.user import User, UserInDB
from api.models.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from api.security import create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, get_password_hash


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

@app.post("/register", response_class=User)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    hashed_password = get_password_hash(form_data.password)
    user = UserInDB(
        username=form_data.username,
        hashed_password=hashed_password
    )
    # db_user = UserInDB.model_validate(user)
    # db_user.hashed_password = hashed_password
    # session.add(db_user)
    # session.commit()
    # session.refresh(db_user)
    return user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/items/")
def get_items(
    session: SessionDep,
):
    items = session.exec(select(Item)).all()
    return items

@app.get("/items/{item_id}")
def get_item(
    item_id: int,
    session: SessionDep,
):
    item_db = session.get(Item, item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_db

@app.post("/items/", response_model=ItemPublic)
def create_item(
    session: SessionDep,
    item: ItemCreate
):
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@app.patch("/items/{item_id}", response_model=ItemPublic)
def update_item(
    item_id: int,
    session: SessionDep,
    item: ItemUpdate,
):
    item_db = session.get(Item, item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.model_dump(exclude_unset=True)
    item_db.sqlmodel_update(item_data)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db

@app.delete("/items/{item_id}", response_model=ItemPublic)
def delete_item(
    item_id: int,
    session: SessionDep,
):
    item_db = session.get(Item, item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item_db)
    session.commit()
    return item_db