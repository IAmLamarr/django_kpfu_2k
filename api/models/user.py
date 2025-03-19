from sqlmodel import SQLModel, Field

class User(SQLModel):
    username: str = Field(primary_key=True)
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User, table=True):
    hashed_password: str