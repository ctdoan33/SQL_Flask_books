from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "KeepItSecretKeepItSafe"
mysql = MySQLConnector(app,'book_db')
@app.route("/")
def index():
    query = "SELECT id, title, author, DATE_FORMAT(created_at, '%b %D %Y') AS date_added FROM books"
    books = mysql.query_db(query)
    return render_template("index.html", all_books=books)
@app.route("/add", methods=["GET"])
def add():
    return render_template("add_book.html")
@app.route("/create", methods=["POST"])
def create():
    valid = True
    if len(request.form["title"]) < 1:
        flash("Title cannot be blank!")
        valid = False
    if len(request.form["author"]) < 1:
        flash("Author cannot be blank!")
        valid = False
    if valid:
        query = "INSERT INTO books (title, author, created_at, updated_at) VALUES (:title, :author,NOW(), NOW())"
        data = {
            "title":request.form["title"],
            "author":request.form["author"],
        }
        mysql.query_db(query, data)
        return redirect("/")
    return redirect("/add")
@app.route("/destroy/<book_id>", methods=["GET"])
def destroy(book_id):
    query = "SELECT title FROM books WHERE id = :id"
    data = {"id":int(book_id)}
    book = mysql.query_db(query, data)
    return render_template("delete_book.html", title=book[0]["title"], book_id=book_id)
@app.route("/delete/<book_id>", methods=["POST"])
def delete(book_id):
    query = "DELETE FROM books WHERE id = :id"
    data = {"id":int(book_id)}
    mysql.query_db(query, data)
    return redirect("/")
@app.route("/update/<book_id>", methods=["GET"])
def update(book_id):
    query = "SELECT title, author FROM books WHERE id = :id"
    data = {"id":int(book_id)}
    book = mysql.query_db(query, data)
    return render_template("update_book.html", title=book[0]["title"], author=book[0]["author"], book_id=book_id)
@app.route("/edit/<book_id>", methods=["POST"])
def edit(book_id):
    valid = True
    if len(request.form["title"]) < 1:
        flash("Title cannot be blank!")
        valid = False
    if len(request.form["author"]) < 1:
        flash("Author cannot be blank!")
        valid = False
    if valid:
        query = "UPDATE books SET title = :title, author = :author, updated_at = NOW() WHERE id = :id"
        data = {
            "title":request.form["title"],
            "author":request.form["author"],
            "id":int(book_id)
        }
        mysql.query_db(query, data)
        return redirect("/")
    return redirect("/update/"+book_id)
@app.route("/quotes/<book_id>", methods=["GET"])
def quote(book_id):
    query = "SELECT title, quote FROM books LEFT JOIN quotes ON books.id = quotes.book_id WHERE books.id = :id"
    data = {"id":int(book_id)}
    book_quotes = mysql.query_db(query, data)
    return render_template("quotes.html", book_quotes=book_quotes, book_id=book_id)
@app.route("/quotes/add/<book_id>", methods=["GET"])
def add_quote(book_id):
    query = "SELECT title FROM books WHERE id = :id"
    data = {"id":int(book_id)}
    book = mysql.query_db(query, data)
    return render_template("add_quote.html", title=book[0]["title"], book_id=book_id)
@app.route("/quotes/create/<book_id>", methods=["POST"])
def create_quote(book_id):
    if len(request.form["quote"]) < 1:
        flash("Quote cannot be blank!")
        return redirect("/quotes/add/"+book_id)
    query = "INSERT INTO quotes (quote, book_id, created_at, updated_at) VALUES (:quote, :book_id, NOW(), NOW())"
    data = {
        "quote":request.form["quote"],
        "book_id":int(book_id)
    }
    mysql.query_db(query, data)
    return redirect("/quotes/"+book_id)
app.run(debug=True)