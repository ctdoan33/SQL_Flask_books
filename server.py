from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "KeepItSecretKeepItSafe"
mysql = MySQLConnector(app,'book_db')
@app.route("/")
def library():
    query = "SELECT id, title, author, DATE_FORMAT(created_at, '%b %D %Y') AS date_added FROM books"
    books = mysql.query_db(query)
    return render_template("index.html", all_books=books)
@app.route("/add", methods=["GET"])
def add():
    return render_template("add_book.html")
@app.route("/addbook", methods=["POST"])
def addbook():
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
@app.route("/destroy/<ident>", methods=["GET"])
def delete(ident):
    session["id"]=int(ident)
    query = "SELECT title FROM books WHERE id = :id"
    data = {"id":session["id"]}
    titledic = mysql.query_db(query, data)
    return render_template("delete_book.html", title=titledic[0]["title"])
@app.route("/cancel", methods=["POST"])
def cancel():
    session.pop("id")
    return redirect("/")
@app.route("/confirm", methods=["POST"])
def confirm():
    query = "DELETE FROM books WHERE id = :id"
    data = {"id":session["id"]}
    mysql.query_db(query, data)
    session.pop("id")
    return redirect("/")
@app.route("/update/<ident>", methods=["GET"])
def update(ident):
    session["id"]=int(ident)
    query = "SELECT title, author FROM books WHERE id = :id"
    data = {"id":session["id"]}
    bookinfo = mysql.query_db(query, data)
    return render_template("update_book.html", title=bookinfo[0]["title"], author=bookinfo[0]["author"])
@app.route("/change", methods=["POST"])
def change():
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
            "id":session["id"]
        }
        mysql.query_db(query, data)
        session.pop("id")
        return redirect("/")
    return redirect("/update/"+str(session["id"]))
app.run(debug=True)