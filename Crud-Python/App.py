#------------------------------------SETTINGS----------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask("__name__")

#Conectar a la Base de Datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudpython'

mysql = MySQL(app)

#Configuraciones
app.secret_key = "mysecretkey"

#--------------------------------------INDEX------------------------------------------------------------

@app.route("/")
def index():
    #Select Database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()  
    return render_template("index.html", contacts = data)

#---------------------------------------ADD---------------------------------------------------------------
@app.route("/add", methods=["POST"])
def add():
    fullname = request.form["fullname"]
    phone = request.form["phone"]
    email = request.form["email"]

    #Insertar datos a la Base de Datos
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO contacts(fullname, phone, email) VALUES(%s,%s,%s)',(fullname, phone, email))
    mysql.connection.commit()

    flash("Datos  guardados correctamente")
    return redirect(url_for('index'))

#---------------------------------------EDIT---------------------------------------------------------------

@app.route("/edit/<id>")
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s",(id))
    data = cur.fetchall()
    return render_template("edit.html", contact = data[0])

@app.route("/update/<id>", methods = ["POST"])
def update(id):
    fullname = request.form ["fullname"]
    phone = request.form ["phone"]
    email = request.form ["email"]
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s    
    """, (fullname, email, phone, id))
    mysql.connection.commit()
    flash("Datos actualizados correctamente")
    return redirect(url_for("index"))

#----------------------------------------DELETE------------------------------------------------------------

@app.route("/delete/<string:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute ("DELETE FROM contacts WHERE id = {0}".format(id))
    mysql.connection.commit()
    flash('Datos eliminados correctamente')
    return redirect(url_for("index"))

#---------------------------------------SETTINGS---------------------------------------------------------

if __name__ == "__main__":
    app.run (port = 2003, debug = True)

#---------------------------------------------------------------------------------------------------------