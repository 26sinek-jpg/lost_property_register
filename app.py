from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
DATABASE = "lost_property.db"
 
def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            location_found TEXT NOT NULL,
            date_found TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            claimed INTEGER DEFAULT 0
        )
    """)
    connection.commit()
    connection.close()
 
  
@app.route("/")
def index():
    return render_template("index.html")
 
@app.route("/add", methods=["POST"])
def add_item():
    item_name = request.form["item_name"]
    location_found = request.form["location_found"]
    date_found = request.form["date_found"]
    description = request.form["description"]
    category = request.form["category"]
 
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
 
    cursor.execute("""
        INSERT INTO items (item_name, location_found, date_found, description,category, claimed)
        VALUES (?, ?, ?, ?, ? , 0)
    """, (item_name, location_found, date_found, description,category))
 
    connection.commit()
    connection.close()
    return redirect("/items")
 
@app.route("/items")
def view_items():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    connection.close()
    return render_template("items.html", items=items)
 
@app.route("/claim/<int:item_id>")
def claim_item(item_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE items SET claimed = 1 WHERE id =?",(item_id,))
    connection.commit()
    connection.close()
    return redirect("/items")
if __name__ == "__main__":
    create_database()
    app.run(debug=True)