from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "smart-farm-secret"


farmers = []
customers = []
products = []
orders = []
reviews = []


def next_id(items):
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def get_current_user():
    role = session.get("role")
    user_id = session.get("user_id")
    if not role or not user_id:
        return None, None
    if role == "farmer":
        for f in farmers:
            if f["id"] == user_id:
                return f, role
    elif role == "customer":
        for c in customers:
            if c["id"] == user_id:
                return c, role
    elif role == "admin":
        return {"username": "admin"}, role
    return None, None


def find_farmer_by_id(farmer_id):
    for f in farmers:
        if f["id"] == farmer_id:
            return f
    return None


def get_farmer_rating(farmer_id):
    farmer_reviews = [r for r in reviews if r["farmer_id"] == farmer_id]
    if not farmer_reviews:
        return 0, 0
    total = sum(r["rating"] for r in farmer_reviews)
    avg = total / len(farmer_reviews)
    return avg, len(farmer_reviews)


def seasonal_suggestions():
    month = datetime.now().month
    if month in (3, 4, 5):  # summer like
        return ["Mango", "Watermelon", "Cucumber"]
    if month in (11, 12, 1):  # winter like
        return ["Carrot", "Cabbage", "Peas"]
    if month in (6, 7, 8, 9):  # rainy / monsoon
        return ["Groundnut", "Rice", "Maize"]
    return ["Tomato", "Potato", "Onion"]


def price_suggestion(product_name):
    same = [p for p in products if p["name"].lower() == product_name.lower()]
    if not same:
        return None
    total = sum(p["price"] for p in same)
    return round(total / len(same), 2)


@app.route("/")
def home():
    user, role = get_current_user()
    return render_template(
        "home.html",
        user=user,
        role=role,
        suggestions=seasonal_suggestions(),
        farmers=farmers,
    )


@app.route("/farmer/register", methods=["GET", "POST"])
def farmer_register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        location = request.form["location"]

        for f in farmers:
            if f["username"] == username:
                flash("Farmer username already exists")
                return redirect(url_for("farmer_register"))

        farmer = {
            "id": next_id(farmers),
            "username": username,
            "password": password,
            "location": location,
        }
        farmers.append(farmer)
        flash("Farmer registered, please login")
        return redirect(url_for("login"))
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Farmer Registration</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
    <div class="container">
        <h2>Farmer Registration</h2>
        <form method="post" class="mt-3" style="max-width: 500px;">
            <div class="mb-3">
                <label class="form-label">Username</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Location (city)</label>
                <input type="text" name="location" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-success">Register</button>
        </form>
    </div>
    </body>
    </html>
    """
    return html


@app.route("/customer/register", methods=["GET", "POST"])
def customer_register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        location = request.form["location"]

        for c in customers:
            if c["username"] == username:
                flash("Customer username already exists")
                return redirect(url_for("customer_register"))

        customer = {
            "id": next_id(customers),
            "username": username,
            "password": password,
            "location": location,
        }
        customers.append(customer)
        flash("Customer registered, please login")
        return redirect(url_for("login"))
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Customer Registration</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
    <div class="container">
        <h2>Customer Registration</h2>
        <form method="post" class="mt-3" style="max-width: 500px;">
            <div class="mb-3">
                <label class="form-label">Username</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Password</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Location (city)</label>
                <input type="text" name="location" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-success">Register</button>
        </form>
    </div>
    </body>
    </html>
    """
    return html


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]
        username = request.form["username"]
        password = request.form["password"]

        if role == "admin":
            if username == "admin" and password == "admin123":
                session["role"] = "admin"
                session["user_id"] = 0
                flash("Logged in as admin")
                return redirect(url_for("admin_dashboard"))
            flash("Invalid admin login")
            return redirect(url_for("login"))

        if role == "farmer":
            for f in farmers:
                if f["username"] == username and f["password"] == password:
                    session["role"] = "farmer"
                    session["user_id"] = f["id"]
                    flash("Farmer login successful")
                    return redirect(url_for("farmer_dashboard"))

        if role == "customer":
            for c in customers:
                if c["username"] == username and c["password"] == password:
                    session["role"] = "customer"
                    session["user_id"] = c["id"]
                    flash("Customer login successful")
                    return redirect(url_for("product_list"))

        flash("Invalid username or password")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for("home"))


@app.route("/farmer/dashboard")
def farmer_dashboard():
    user, role = get_current_user()
    my_products = []
    if user and role == "farmer":
        my_products = [p for p in products if p["farmer_id"] == user["id"]]
    return render_template("farmer_dashboard.html", farmer=user, role=role, products=my_products)


@app.route("/farmer/product/add", methods=["GET", "POST"])
def add_product():
    user, role = get_current_user()
    if role != "farmer":
        flash("Farmer login required")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        image_url = request.form["image_url"]
        season = request.form["season"]

        product = {
            "id": next_id(products),
            "name": name,
            "category": category,
            "price": price,
            "quantity": quantity,
            "image_url": image_url,
            "season": season,
            "farmer_id": user["id"],
            "farmer_location": user["location"],
            "approved": True,
        }
        products.append(product)
        flash("Product added, waiting for admin approval")
        return redirect(url_for("farmer_dashboard"))

    suggest_price = None
    product_name = request.args.get("name")
    if product_name:
        suggest_price = price_suggestion(product_name)
    return render_template(
        "add_product.html",
        suggest_price=suggest_price,
        user=user,
        role=role,
    )


@app.route("/products")
def product_list():
    user, role = get_current_user()
    query = request.args.get("q", "").lower()
    season = request.args.get("season", "")

    visible = [p for p in products if p["approved"]]

    if query:
        visible = [p for p in visible if query in p["name"].lower()]
    if season:
        visible = [p for p in visible if p["season"].lower() == season.lower()]

    suggestions = seasonal_suggestions()
    return render_template(
        "product_list.html",
        products=visible,
        user=user,
        role=role,
        suggestions=suggestions,
        query=query,
        season=season,
    )


@app.route("/product/<int:product_id>", methods=["GET", "POST"])
def product_detail(product_id):
    user, role = get_current_user()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        flash("Product not found")
        return redirect(url_for("product_list"))

    farmer = find_farmer_by_id(product["farmer_id"])
    avg_rating, review_count = get_farmer_rating(farmer["id"]) if farmer else (0, 0)

    same_products = [
        p for p in products if p["name"].lower() == product["name"].lower() and p["approved"]
    ]

    # Check if the current customer has actually ordered this product
    has_ordered = False
    if user and role == "customer":
        for o in orders:
            if o["customer_id"] == user["id"]:
                for item in o["items"]:
                    if item["product_id"] == product_id:
                        has_ordered = True
                        break
                if has_ordered:
                    break

    if request.method == "POST" and role == "customer":
        if not has_ordered:
            flash("You can only review products you have ordered.")
            return redirect(url_for("product_detail", product_id=product_id))

        rating = int(request.form["rating"])
        comment = request.form["comment"]
        review = {
            "id": next_id(reviews),
            "farmer_id": farmer["id"] if farmer else None,
            "customer_id": user["id"],
            "rating": rating,
            "comment": comment,
        }
        reviews.append(review)
        flash("Review added")
        return redirect(url_for("product_detail", product_id=product_id))

    farmer_reviews = [r for r in reviews if r["farmer_id"] == farmer["id"]] if farmer else []

    return render_template(
        "product_detail.html",
        product=product,
        farmer=farmer,
        user=user,
        role=role,
        same_products=same_products,
        avg_rating=avg_rating,
        review_count=review_count,
        farmer_reviews=farmer_reviews,
        has_ordered=has_ordered,
    )


@app.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    user, role = get_current_user()
    if role != "customer":
        flash("Customer login required to add to cart")
        return redirect(url_for("login"))

    product = next((p for p in products if p["id"] == product_id and p["approved"]), None)
    if not product:
        flash("Product not found or not approved")
        return redirect(url_for("product_list"))

    cart = session.get("cart", [])
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += 1
            break
    else:
        cart.append(
            {
                "product_id": product_id,
                "name": product["name"],
                "price": product["price"],
                "quantity": 1,
                "farmer_id": product["farmer_id"],
            }
        )

    session["cart"] = cart
    flash("Added to cart")
    return redirect(url_for("cart_view"))


@app.route("/cart")
def cart_view():
    user, role = get_current_user()
    cart = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart)
    return render_template("cart.html", cart=cart, total=total, user=user, role=role)


@app.route("/cart/checkout", methods=["POST"])
def checkout():
    user, role = get_current_user()
    if role != "customer":
        flash("Customer login required")
        return redirect(url_for("login"))

    cart = session.get("cart", [])
    if not cart:
        flash("Cart is empty")
        return redirect(url_for("cart_view"))

    order = {
        "id": next_id(orders),
        "customer_id": user["id"],
        "items": cart,
        "status": "Placed",
        "created_at": datetime.now(),
    }
    orders.append(order)
    session["cart"] = []
    flash("Order placed successfully")
    return redirect(url_for("product_list"))


@app.route("/orders")
def order_history():
    user, role = get_current_user()
    if role != "customer":
        flash("Customer login required")
        return redirect(url_for("login"))

    my_orders = [o for o in orders if o["customer_id"] == user["id"]]
    return render_template("order_history.html", orders=my_orders, user=user, role=role)


@app.route("/farmer/orders")
def farmer_orders():
    user, role = get_current_user()
    if role != "farmer":
        flash("Farmer login required")
        return redirect(url_for("login"))

    my_orders = []
    for o in orders:
        for item in o["items"]:
            if item["farmer_id"] == user["id"]:
                my_orders.append(o)
                break

    return render_template("farmer_orders.html", orders=my_orders, user=user, role=role)


@app.route("/nearby_farmers")
def nearby_farmers():
    user, role = get_current_user()
    if role != "customer":
        flash("Customer login required")
        return redirect(url_for("login"))

    my_location = user["location"]
    nearby = [f for f in farmers if f["location"].lower() == my_location.lower()]

    return render_template(
        "nearby_farmers.html",
        farmers=nearby,
        my_location=my_location,
        user=user,
        role=role,
    )


@app.route("/admin")
def admin_dashboard():
    user, role = get_current_user()
    pending_products = [p for p in products if not p["approved"]]
    all_orders = orders
    return render_template(
        "admin_dashboard.html",
        products=pending_products,
        orders=all_orders,
        farmers=farmers,
        customers=customers,
        user=user,
        role=role,
    )


@app.route("/admin/product/<int:product_id>/approve")
def approve_product(product_id):
    user, role = get_current_user()
    if role != "admin":
        flash("Admin login required")
        return redirect(url_for("login"))

    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        product["approved"] = True
        flash("Product approved")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/product/<int:product_id>/delete")
def delete_product_admin(product_id):
    user, role = get_current_user()
    if role != "admin":
        flash("Admin login required")
        return redirect(url_for("login"))

    global products
    products = [p for p in products if p["id"] != product_id]
    flash("Product deleted")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True)

