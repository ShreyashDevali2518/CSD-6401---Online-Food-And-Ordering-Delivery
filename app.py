from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database import DatabaseManager
from menu_factory import MenuItemFactory
from menu_proxy import MenuManagementProxy

app = Flask(__name__)
app.secret_key = "member-one-development-secret"
db = DatabaseManager()
menu_proxy = MenuManagementProxy(db)


def current_user():
    user_id = session.get("user_id")
    return db.get_user_by_id(user_id) if user_id else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = current_user()
        if not user:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        if user["role"] != "admin":
            flash("Only an administrator can manage the menu.", "error")
            return redirect(url_for("index"))
        return view(*args, **kwargs)
    return wrapped


@app.get("/")
def index():
    return render_template("index.html", foods=db.get_menu(), user=current_user())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Enter your name and email, and use a password of at least 8 characters.", "error")
            return redirect(url_for("register"))
        if db.get_user_by_email(email):
            flash("An account with that email already exists.", "error")
            return redirect(url_for("register"))
        db.create_user(name, email, generate_password_hash(password))
        flash("Account created. You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("auth.html", mode="register", user=current_user())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = db.get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Email or password is incorrect.", "error")
            return redirect(url_for("login"))
        session.clear()
        session["user_id"] = user["id"]
        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("index"))
    return render_template("auth.html", mode="login", user=current_user())


@app.post("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.get("/admin/menu")
@admin_required
def admin_menu():
    return render_template("admin_menu.html", foods=db.get_menu(), user=current_user())


@app.post("/admin/menu/add")
@admin_required
def add_menu_item():
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    category = request.form.get("category", "").strip()
    price_text = request.form.get("price", "").strip()
    try:
        price = float(price_text)
        if price <= 0:
            raise ValueError
    except ValueError:
        flash("Enter a valid price greater than zero.", "error")
        return redirect(url_for("admin_menu"))
    if not name or not description or category not in MenuItemFactory.CATEGORIES:
        flash("Complete all fields and choose a valid category.", "error")
        return redirect(url_for("admin_menu"))
    item = MenuItemFactory.create(category, name, description, price)
    menu_proxy.add_item(item, current_user())
    flash("Menu item added.", "success")
    return redirect(url_for("admin_menu"))


@app.post("/admin/menu/delete/<int:item_id>")
@admin_required
def delete_menu_item(item_id):
    menu_proxy.delete_item(item_id, current_user())
    flash("Menu item removed.", "success")
    return redirect(url_for("admin_menu"))


if __name__ == "__main__":
    db.initialize()
    app.run(debug=True, port=5001)
