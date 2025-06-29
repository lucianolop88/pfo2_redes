from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = generate_password_hash(data.get('contraseña'))

    if Usuario.query.filter_by(usuario=usuario).first():
        return jsonify({"mensaje": "Usuario ya existe"}), 400

    nuevo_usuario = Usuario(usuario=usuario, contraseña=contraseña)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')

    user = Usuario.query.filter_by(usuario=usuario).first()
    if user and check_password_hash(user.contraseña, contraseña):
        session['usuario'] = usuario
        return jsonify({"mensaje": "Login exitoso"}), 200
    return jsonify({"mensaje": "Credenciales incorrectas"}), 401



@app.route('/tareas', methods=['GET'])
def tareas():
    if 'usuario' not in session:
        return jsonify({"mensaje": "No autorizado"}), 401
    return render_template('bienvenida.html', usuario=session['usuario'])



if __name__ == '__main__':
    app.run(debug=True)