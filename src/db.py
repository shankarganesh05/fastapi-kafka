from sqlmodel import SQLModel,create_engine,Session,Field
from datetime import datetime,timezone

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi"

class Orders(SQLModel,table=True):
    __tablename__ = "Orders"
    order_id: int = Field(primary_key=True)
    item: str
    quantity: int = Field(nullable=False)
    price_per_item: float = Field(nullable=False)
    created_at : datetime = Field(default_factory=lambda:datetime.now(timezone.utc))
    
class Users(SQLModel,table=True):
    __tablename__ = "users"
    Email: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
    id: int = Field(default=None, primary_key=True)

engine = create_engine(DATABASE_URL)

def get_session():
    return Session(engine)

    
