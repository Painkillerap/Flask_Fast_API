from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Создание подключения к базе данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./shop.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Определение моделей SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Numeric(10, 2))


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_date = Column(DateTime)
    status = Column(String)


# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)


# Pydantic модели для валидации данных
class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str


class ProductCreate(BaseModel):
    title: str
    description: str
    price: float


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    order_date: datetime
    status: str


class UserRead(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    class Config:
        from_attributes = True


class ProductRead(BaseModel):
    id: int
    title: str
    description: str
    price: float

    class Config:
        from_attributes = True


class OrderRead(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: datetime
    status: str

    class Config:
        from_attributes = True


# Функции для взаимодействия с базой данных

def get_db():
    """ Зависимость для создания сессии базы данных """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


# Функции CRUD для пользователей, товаров и заказов
def create_user(db: Session, user: UserCreate):
    """
    Создает нового пользователя в базе данных с хэшированием пароля
    и проверкой уникальности электронной почты
    """
    # Проверка на уникальность электронной почты
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Хэширование пароля
    try:
        hashed_password = get_password_hash(user.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error hashing password: {str(e)}")

    # Создание нового пользователя
    db_user = User(name=user.name, surname=user.surname, email=user.email, password=hashed_password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # Возвращаем данные пользователя, исключая пароль
    return UserRead(id=db_user.id, name=db_user.name, surname=db_user.surname, email=db_user.email)


def get_user(db: Session, user_id: int):
    """ Получает пользователя по ID """
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_update: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    db_user.name = user_update.name
    db_user.surname = user_update.surname
    db_user.email = user_update.email
    # Предполагаем, что пароль обновлять не требуется

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


# Функции для работы с продуктами
def create_product(db: Session, product: ProductCreate):
    db_product = Product(title=product.title, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


# Функции для работы с заказами
def create_order(db: Session, order: OrderCreate):
    db_order = Order(user_id=order.user_id, product_id=order.product_id, order_date=order.order_date,
                     status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


# Создание экземпляра FastAPI приложения
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}


# Маршруты FastAPI для обработки HTTP запросов
@app.post("/users/", response_model=UserRead)
def api_create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    API-маршрут для создания нового пользователя
    """
    return create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=UserRead)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    """ Возвращает пользователя по ID через API """
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Маршруты для продуктов
@app.post("/products/", response_model=ProductRead)
def api_create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)


@app.get("/products/{product_id}", response_model=ProductRead)
def api_get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# Маршруты для заказов
@app.post("/orders/", response_model=OrderRead)
def api_create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db=db, order=order)


@app.get("/orders/{order_id}", response_model=OrderRead)
def api_get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.put("/users/{user_id}", response_model=UserRead)
def api_update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Получает информацию о пользователе по его ID.

    - **user_id**: Уникальный идентификатор пользователя.
    """
    db_user = update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}")
def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
