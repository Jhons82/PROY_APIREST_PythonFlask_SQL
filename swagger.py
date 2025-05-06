#TODO: Importar Bibliotecas
from flask import Flask, jsonify, current_app, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from flask_restx import Api, Resource, fields

#TODO: Iniciar API
app = Flask(__name__)

#TODO:Configuración de conexión a una BD con el controlador ODBC
nombre_usuario = 'sa'
contrasena = '*************' #Ingresar la contraseña de sa de SQL Server
nombre_servidor = 'LAPTOP-LCRALN5G\\SQLEXPRESS'
nombre_base_datos = 'proy_apirest_pythonflask_sql'
driver_odbc = 'ODBC Driver 17 for SQL Server' #También: ODBC+Driver+17+for+SQL+Server

#TODO: Cadena conexión a BD
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{nombre_usuario}:{contrasena}@{nombre_servidor}/{nombre_base_datos}?driver={driver_odbc}"
)

#TODO: Desactiva e inicia SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#TODO: Configuración de API con flask_restx
api = Api(app, version='1.0', title='API con Python Flask y SQL Server', description='API para gestionar CRUD de Usuarios. CRUD básico de Usuarios con los métodos HTTP (GET, POST, PUT, DELETE)'+'\n\n'+'Documentación Flask RestX:'+'\n'+'https://flask-restx.readthedocs.io/en/latest/')

#TODO: Define para agrupar las rutas
ns = api.namespace('Usuarios', description='Operaciones Relacionadas con Usuarios')

#TODO: Modelos de Datos
insert_user_model = api.model('InsertUser', {
    'user_nombre' : fields.String(required=True, description='Nombre del Usuario'),
    'user_apellido' : fields.String(required=True, description='Apellido del Usuario'),
    'title' : fields.String(required=True, description='Título del Usuario'),
    'address' : fields.String(required=True, description='Dirección del Usario')
})

update_user_model = api.clone('UpdateUser', insert_user_model, {
    'user_id': fields.Integer(required=True, description='ID de Usuario'),
    'estado': fields.Integer(required=True, description='Estado del Usuario')
})

delete_user_model = api.model('DeleteUser', {
    'user_id' : fields.Integer(required=True, description='ID del Usuario a Eliminar')
})

#TODO: Implementación de rutas y métodos de la API
@ns.route('/')
class UsersList(Resource):
    def get(self):
        try:
            sql_query = text('EXEC SP_L_USERS_01')
            resultado = db.session.execute(sql_query)
            usuarios_json = [dict(row._mapping) for row in resultado]
            return jsonify(usuarios_json)
    
        except Exception as e:
            return jsonify({'Error': str(e)})
        finally:
            db.session.close()

@ns.route('/<int:id>')
class UserSingle(Resource):
    def get(self,id):
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

@ns.route('/insert')
class InsertUser(Resource):
    @api.expect(insert_user_model)
    def post(self):
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

@ns.route('/update')
class UpdateUser(Resource):
    @api.expect(update_user_model)
    def put(self):
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

@ns.route('/delete')
class DeleteUser(Resource):
    @api.expect(delete_user_model)
    def delete(self):
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

#TODO: Esquema en JSON
""" @app.route('/api/doc')
def swagger_ui():
    return jsonify(api.__schema__) """

#TODO: Ejecución de la API
if __name__ == '__main__':
    app.run(debug=True)