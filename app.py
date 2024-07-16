from flask import Flask, render_template, request, url_for, redirect, g
import mysql.connector

app = Flask(__name__, template_folder="templates", static_folder="static")


def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host="bvjy0fief8tnbddoxry8-mysql.services.clever-cloud.com",
            user="uhrezqffmnurete8",
            password="jkLDZ4qhUOsvYN2JZ6OX",
            port=3306,
            database="bvjy0fief8tnbddoxry8",
        )
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    db = get_db()
    curs = db.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS details(id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(20), Price INT, Author VARCHAR(20), Description TEXT, Language TEXT, Category TEXT)"
    )
    return render_template("index.html")


@app.route("/submit", methods=["POST", "GET"])
def submit():
    db = get_db()
    curs = db.cursor(dictionary=True)
    search_input = request.form.get("ser")
    query = "SELECT * FROM details WHERE Name LIKE %s OR Author LIKE %s OR Description LIKE %s OR Language LIKE %s OR Category LIKE %s"
    curs.execute(
        query,
        (
            "%" + search_input + "%",
            "%" + search_input + "%",
            "%" + search_input + "%",
            "%" + search_input + "%",
            "%" + search_input + "%",
        ),
    )
    details = curs.fetchall()
    return render_template("search.html", details=details)


@app.route("/products/")
def products():
    db = get_db()
    curs = db.cursor(dictionary=True)
    curs.execute("SELECT * FROM details")
    details = curs.fetchall()
    return render_template("products.html", details=details)


@app.route("/product_details/home", methods=["POST", "GET"])
def product_details_ret():
    return redirect(url_for("home"))


@app.route("/product_details/", methods=["POST", "GET"])
def product_details():
    category = request.args.get("prod_name")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM details WHERE Name = %s", (category,))
    product_details = cursor.fetchone()
    if product_details:
        Name, Price, Author, Description, Language, Category = product_details
        return render_template(
            "product_details.html",
            Name=Name,
            Price=Price,
            Author=Author,
            Description=Description,
            Language=Language,
            Category=Category,
        )
    else:
        return redirect(url_for("home"))


@app.route("/Addproduct", methods=["POST", "GET"])
def Addproduct():
    if request.method == "POST":
        db = get_db()
        curs = db.cursor()
        Name = request.form.get("Name")
        Price = request.form.get("Price")
        Author = request.form.get("Author")
        Description = request.form.get("Description")
        Language = request.form.get("Language")
        Category = request.form.get("Category")

        if Name and Price and Author and Description and Language and Category:
            sql = "INSERT INTO details(Name, Price, Author, Description, Language, Category) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (Name, Price, Author, Description, Language, Category)
            curs.execute(sql, val)
            db.commit()
            return redirect(url_for("home"))
    return render_template("Addproduct.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    return render_template("contact.html")


@app.route("/price", methods=["POST", "GET"])
def price():
    db = get_db()
    curs = db.cursor(dictionary=True)
    curs.execute("SELECT * FROM details ORDER BY Price")
    details = curs.fetchall()
    return render_template("price.html", details=details)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
