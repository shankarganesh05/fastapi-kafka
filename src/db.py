from sqlmodel import SQLModel,create_engine,Session,Field

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi"

class Orders(SQLModel,table=True):
    __tablename__ = "Orders"
    order_id: int = Field(primary_key=True)
    item: str
    quantity: int = Field(nullable=False)
    price_per_item: float = Field(nullable=False)

engine = create_engine(DATABASE_URL)

def get_session():
    return Session(engine)
    
