# write code to connect to the db & extract data from db 

import sqlalchemy
from sqlalchemy import create_engine, text
from datetime import datetime
from sqlalchemy.pool import QueuePool



# create an engine which will connect to db

# Replace 'your_server', 'your_database', 'your_username', and 'your_password' with your actual server, database, username, and password
connection_string = "mssql+pyodbc://shreyasi:USERuser1234@34.16.30.199/ecommerce_db?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection_string)


# Use a connection pool with a maximum of 5 connections.
engine = create_engine(connection_string, pool_size=5, poolclass=QueuePool)


#loading prods dict from database

def load_prods_from_db():
    with engine.connect() as conn:
        result=conn.execute(text("select * from products"))

    #list of dictionaries ; inside the lists there are objects..
        products = []
        for row in result.all():
            products.append(row._asdict())
        return products
    

def load_proddetail_from_db(p_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM products WHERE p_id = :val"), {"val": p_id} )
 
        
        rows=result.all()
        
        if len(rows) == 0:
          return None
        else:
          return (rows[0]._asdict())
        

   
def authenticate_user(username, password):
    with engine.connect() as conn:
        query = text("SELECT * FROM users WHERE user_id = :username AND password = :password")
        print(f"Executing query: {query}")
        print(f"Checking for user: {username}, Password: {password}")
        result = conn.execute(query, {"username": username, "password": password})

        rows = result.fetchall()
        if not rows:
            print("No matching user found.")
            return False

        # Assuming 'password' is the fourth column in the result set
        decoded_password = rows[0][3]
        print(f"Decoded password from database: {decoded_password}")

        return True





########## CART


# Function to add a product to the user's cart
def add_product_to_cart(user_id, product_id):
    with engine.connect() as conn:
        query = text(
            "INSERT INTO cart (user_id, product_id, created_at, updated_at) "
            "VALUES (:user_id, :product_id, :created_at, :updated_at)"
        )
        conn.execute(
            query,
            {
                "user_id": user_id,
                "product_id": product_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
        )
    

# Function to retrieve the user's cart
def get_user_cart(user_id):
    with engine.connect() as conn:
        query = text(
            "SELECT products.* FROM products "
            "JOIN cart ON products.p_id = cart.product_id "
            "WHERE cart.user_id = :user_id")

        # Debugging: Print the SQL query to the console
        print(f"SQL Query in get_user_cart: {query}")

        result = conn.execute(query, {"user_id": user_id})

        cart_items = []
        for row in result.all():
            cart_items.append(row._asdict())

        # Debugging: Print the cart items to the console
        print(f"Cart Items in get_user_cart: {cart_items}")

        return cart_items
    




# Function to get the user's ID based on the user_id
def get_user_id(user_id):
    with engine.connect() as conn:
        query = text("SELECT user_id FROM users WHERE user_id = :user_id")
        result = conn.execute(query, {"user_id": user_id})
        user_id = result.scalar()

        # Debugging: Print the user_id to the console
        print(f"User ID in get_user_id: {user_id}")

        return user_id

