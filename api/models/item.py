from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    name: str = Field(index=True)
    price: float
    is_offer: bool = Field(default=False)


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    name: str | None = None
    price: float | None = None
    is_offer: bool | None = None


class ItemPublic(ItemBase):
    id: int