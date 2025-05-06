from flask import Flask, jsonify, current_app, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

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
@app.route('/api/usuarios', methods = ['GET'])
def usuarios():
    try:
        sql_query = text('EXEC SP_L_USERS_01')
        resultado = db.session.execute(sql_query)
        usuarios_json = [dict(row._mapping) for row in resultado]
        return jsonify(usuarios_json)
    
    except Exception as e:
        return jsonify({'Error': str(e)})
    finally:
        db.session.close()
    
#TODO: Usuario según ID
@app.route('/api/usuario/<int:id>', methods = ['GET'])
def usuario(id):
    try:
        sql_query = text('EXEC SP_L_USERS_02 @user_id=:id')

        resultado = db.session.execute(sql_query, {'id' : id})

        usuarios_json = [dict(row._mapping) for row in resultado]

        return jsonify(usuarios_json)
    
    except SQLAlchemyError as e:
        current_app.logger.error(f'Error al ejecutar la consulta: {e}')
        return jsonify({'Error': 'Error al obtener los datos del usuario.'}), 500
    finally:
        db.session.close()

#TODO: Ingresar nuevo registro a la tabla
@app.route('/api/insert', methods=['POST'])
def insert():
    try:
        data_json = request.get_json()
        user_nombre = data_json['user_nombre']
        user_apellido = data_json['user_apellido']
        title = data_json['title']
        address = data_json['address']

        sql_query = text('EXEC SP_I_USERS_01 @user_nombre=:user_nombre, @user_apellido=:user_apellido, @title=:title, @address=:address')
        db.session.execute(sql_query, {'user_nombre':user_nombre, 'user_apellido':user_apellido, 'title':title, 'address':address})
        db.session.commit()

        return jsonify({'Mensaje':'Usuario registrado Correctamente'})
    
    except SQLAlchemyError as e:
        current_app.logger.error({f'Error al ejecutar la consulta: {e}'})
        return jsonify({'Error':'Error al registrar el usuario'}), 500
    finally:
        db.session.close()

#TODO: Actualizar un registro de la tabla
@app.route('/api/update', methods=['PUT'])
def update():
    try:
        data_json = request.get_json()
        user_id = data_json['user_id']
        user_nombre = data_json['user_nombre']
        user_apellido = data_json['user_apellido']
        title = data_json['title']
        address = data_json['address']
        estado = data_json['estado']

        sql_query = text('EXEC SP_U_USERS_01 @user_id=:user_id, @user_nombre=:user_nombre, @user_apellido=:user_apellido, @title=:title, @address=:address, @estado=:estado')
        db.session.execute(sql_query, {'user_id':user_id, 'user_nombre':user_nombre, 'user_apellido':user_apellido, 'title':title, 'address':address, 'estado':estado})
        db.session.commit()

        return jsonify({'Mensaje':'Usuario actualizado Correctamente'})
    except SQLAlchemyError as e:
        current_app.logger.error({f'Error al ejecutar la consulta: {e}'})
        return jsonify({'Error':'Error al actualizar el usuario'}), 500
    finally:
        db.session.close()

#TODO: Eliminar el registro de la tabla users (estado = 0)
@app.route('/api/delete', methods=['DELETE'])
def delete():
    try:
        data_json = request.get_json()
        user_id = data_json['user_id']

        sql_query = text('EXEC SP_D_USERS_01 @user_id=:user_id')
        db.session.execute(sql_query, {'user_id':user_id})
        db.session.commit()

        return jsonify({'Mensaje':'Usuario eliminado Correctamente'})
    
    except SQLAlchemyError as e:
        current_app.logger.error({f'Error al ejecutar la consulta: {e}'})
        return jsonify({'Error':'Error al eliminar el usuario'}, 500)
    finally:
        db.session.close()

if __name__ == '__main__':
    app.run(debug=True)