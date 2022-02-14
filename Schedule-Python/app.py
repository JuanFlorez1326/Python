
from threading import Event
from flask import Flask,render_template,redirect,request, url_for,session,flash
from flask.sessions import SessionInterface
from flask_mysqldb import MySQL,MySQLdb
from flask import flash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'Juan67927' 
app.config['MYSQL_DB'] = 'agendame'


mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route("/")
def primero():
    return render_template("login.html")

@app.route("/registro")
def segundo():
    return render_template("registro.html")

@app.route("/registro",methods = ["POST"])
def registro():
    nombre = request.form ["nombre"]
    apellidos = request.form ["apellidos"]
    edad = request.form ["edad"]
    ocupacion = request.form ["ocupacion"]
    correo = request.form ["correo"]
    contraseña = request.form ["contraseña"]
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO usuarios(nombre,apellidos,edad,ocupacion,correo,contraseña) VALUES (%s,%s,%s,%s,%s,%s)",(nombre,apellidos,edad,ocupacion,correo,contraseña))
    mysql.connection.commit()
    return render_template("registro.html")

@app.route("/",methods = ["POST"])
def ingresar():
    correo = request.form ["correo"]
    contraseña = request.form ["contraseña"]
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM usuarios WHERE correo = '{correo}' and contraseña = '{contraseña}'")
    user = cursor.fetchone()
    cursor.close()
    if len(user) >0:
        session["username"] = user[1]
        session["id"]=user[0]
        return redirect ("/index")
    else:
        return redirect("/")

@app.route('/index')
def cuarta():
    return render_template("index.html")


@app.route('/eventos')
def eventos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM eventos')
    data = cur.fetchall()
    cur.close()
    return render_template('eventos.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        lugar = request.form['lugar']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO eventos ( idusuarios,nombre, fecha,lugar, descripcion) VALUES (%s,%s,%s,%s,%s)", (session["id"],nombre, fecha,lugar,descripcion))
        mysql.connection.commit()
        flash('Evento añadido satisfactoriamente')
        return redirect(url_for('eventos'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM eventos WHERE id = %s', (id,))
    data = cur.fetchone()
    cur.close()
    print(data)
    return render_template('edit-contact.html', contact = data)

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        lugar = request.form['lugar']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE eventos
            SET nombre = %s,
                fecha = %s,
                lugar = %s,
                descripcion = %s
            WHERE id = %s
        """, (nombre, fecha,lugar,descripcion, id))
        flash('Evento actualizado satisfactoriamente')
        mysql.connection.commit()
        return redirect(url_for('eventos'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM eventos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Evento eliminado satisfactoriamente')
    return redirect(url_for('eventos'))



if __name__ == '__main__':
    app.run(debug=True,port=5000 ) 