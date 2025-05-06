from flask import Flask, jsonify, request

#TODO: Crea una instancia flask app 
app = Flask(__name__)

#TODO: crea lista de usuarios
usuarios = [{'user_id': 1, 'user_nombre': 'John'},{'user_id':2, 'user_nombre': 'God'},{'user_id':3, 'user_nombre': 'Win'}]    

#TODO: Crea una ruta para la URL raíz o principal
@app.route('/')
def Hola_munfo():
    return 'Hola mundo!'

#TODO: Ruta para lista de usuarios
@app.route('/usuarios')
def get_usuarios():
    #TODO: Devolver en formato JSON
    return jsonify(usuarios)

#TODO: Ruta para usuario según su ID
@app.route('/usuario/<int:user_id>')
def obtener_usuario(user_id):
    #TODO: Buscar el usuario por ID en lista (usuarios)
    usuario = next((user for user in usuarios if user['user_id'] == user_id), None)
    #TODO: Condicional para verificar si el usuario existe o no según su ID
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

#TODO:  Buscar usuario por nombre
@app.route('/buscar')
def buscar_usuario():
    #TODO: Obtener el nombre del usaurio desde la URL
    nombre = request.args.get('nombre')
    #TODO: Buscar el usuario por nombre en la lista (usuarios)
    usuario_encontrado = [user for user in usuarios if user['user_nombre'].lower() == nombre.lower()]
    #TODO: condicional para verificar si el usuario existe o no según su nombre
    if usuario_encontrado:
        return jsonify(usuario_encontrado)
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

#TODO: Inicia la aplicación Flask
if __name__ == '__main__':
    #TODO: Ejecuta la aplicación en modo de depuración
    app.run(debug=True)