from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import jwt

app = FastAPI()

SECRET_KEY = "supersecret123"

# Database setup
conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item TEXT,
    amount INTEGER
)
""")

conn.commit()


# Models
class User(BaseModel):
    username: str
    password: str

class Order(BaseModel):
    item: str
    amount: int


# Register
@app.post("/register")
def register(user: User):
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user.username, user.password)
    )
    conn.commit()
    return {"message": "User registered"}


# Login
@app.post("/login")
def login(user: User):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user.username, user.password)
    )
    db_user = cursor.fetchone()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"user_id": db_user[0]}, SECRET_KEY, algorithm="HS256")
    return {"token": token}


# Get current user
def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


# Create order
@app.post("/orders")
def create_order(order: Order, token: str):
    user_id = get_current_user(token)

    cursor.execute(
        "INSERT INTO orders (user_id, item, amount) VALUES (?, ?, ?)",
        (user_id, order.item, order.amount)
    )
    conn.commit()

    return {"message": "Order created"}


# Get single order
@app.get("/orders/{order_id}")
def get_order(order_id: int, token: str):
    user_id = get_current_user(token)

    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = cursor.fetchone()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_id": order[0],
        "user_id": order[1],
        "item": order[2],
        "amount": order[3]
    }


# Get all orders of logged-in user
@app.get("/my-orders")
def get_my_orders(token: str):
    user_id = get_current_user(token)

    cursor.execute("SELECT * FROM orders WHERE user_id=?", (user_id,))
    orders = cursor.fetchall()

    return [
        {
            "order_id": o[0],
            "item": o[2],
            "amount": o[3]
        }
        for o in orders
    ]
@app.get("/")
def root():
    return {"message": "API working"}