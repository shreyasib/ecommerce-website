from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from urllib.parse import quote


from database import load_prods_from_db, load_proddetail_from_db, authenticate_user, get_user_cart, get_user_id, add_product_to_cart


app = Flask(__name__)      # app is a var #our flask app is called __name__ (default)
app.secret_key = 'sgajdkq32414'




# Home
@app.route("/")            #route is a part of url, everything after url. so google/about 
def hello_world():
    products=load_prods_from_db()
    return render_template("home.html", prods=products)


# All products
@app.route("/products")
def list_products():
    products=load_prods_from_db()


    return render_template("seperateproducts.html", products=products)



# Product detail
@app.route("/products/<p_id>")
def show_products(p_id):
    prod=load_proddetail_from_db(p_id)
    
    if not prod:
        return "Not Found"
    

    return render_template("prodpage.html", prod=prod)
    #return jsonify(products)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password").strip()
        encoded_password = quote(password)

        print(f"Received login attempt: Username - {username}, Password - {password}")
        print(f"Encoded password: {encoded_password}")

        if authenticate_user(username, encoded_password):
            session["username"] = username

            

            flash("Login successful!", "success")
            return redirect(url_for("list_products"))
        else:
            flash("Invalid username or password", "error")
            print("Authentication failed")

    return render_template("login.html")


@app.route("/logout")
def logout():
    # Clear the session data
    session.pop("username", None)
    return "Logout Successful!"





################## CART ###################


@app.route("/add_to_cart/<product_id>", methods=['GET', 'POST'])
def add_to_cart(product_id):
    # Check if user is logged in
    if 'username' not in session:
        flash('Please log in to add products to your cart.', 'danger')
        return redirect(url_for('login'))

    user_id = get_user_id(session['username'])
    print(f"User ID: {user_id}, Product ID: {product_id}")

    if request.method == 'POST':
        # Add product to the user's cart
        add_product_to_cart(user_id, product_id)

        flash('Product added to cart successfully!', 'success')
        print(f"Product {product_id} added to cart for user {user_id}")

        return redirect(url_for('view_cart'))

    # Handle GET request (if needed)
    # You can add additional handling for GET requests, or simply return a response
    return "Invalid request method for this route."




# View user's cart
@app.route("/cart")
def view_cart():
    # Check if user is logged in
    if 'username' not in session:
        flash('Please log in to view your cart.', 'danger')
        return redirect(url_for('login'))

    user_id = get_user_id(session['username'])

    # Retrieve the user's cart
    cart_items = get_user_cart(user_id)

    # Debugging: Print the cart items to the console
    print(f"Cart Items: {cart_items}")

    return render_template("cart.html", cart_items=cart_items)






if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
