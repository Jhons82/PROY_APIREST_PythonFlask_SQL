from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

nombre_usuario = 'sa'
contrasena = '969392668jhon'
nombre_servidor = 'LAPTOP-LCRALN5G\\SQLEXPRESS'
nombre_base_datos = 'proy_apirest_pythonflask_sql'
driver_odbc = 'ODBC Driver 17 for SQL Server' #También: ODBC+Driver+17+for+SQL+Server

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{nombre_usuario}:{contrasena}@{nombre_servidor}/{nombre_base_datos}?driver={driver_odbc}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#TODO: Lista de Usuarios
@app.route('/consulta_sql_directa')
def consulta_sql_directa():
    sql_query = text('EXEC SP_L_USERS_01')

    resultado = db.session.execute(sql_query)

    usuarios_json = [dict(row._mapping) for row in resultado]

    return jsonify(usuarios_json)

if __name__ == '__main__':
    app.run(debug=True)