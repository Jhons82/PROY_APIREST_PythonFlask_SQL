<!-- TODO: Methods -->

<!-- TODO: Method GET - Users -->
http://127.0.0.1:5000/api/usuarios

<!-- TODO: Method GET - User ID -->
http://127.0.0.1:5000/api/usuario/2

<!-- TODO: Method POST - Insert User -->
http://127.0.0.1:5000/api/insert

POST -> raw -> JSON

{
    "user_nombre" : "Sara",
    "user_apellido" : "Turner",
    "title" : "Tecnología Médica",
    "address" : "Av. South Plaza"
}

<!-- TODO: Method PUT - Update User -->

PUT -> raw -> JSON

{
    "user_id" : 7,
    "user_nombre" : "Sarah",
    "user_apellido" : "Turner",
    "title" : "Tecnología Médica",
    "address" : "Av. South Plaza",
    "estado" : 1
}

<!-- TODO: Method DELETE - Delete User -->

DELETE -> raw -> JSON

{
    "user_id" : 7
}

<!-- TODO: Ruta para Flask RestX Swagger -->
https://flask-restx.readthedocs.io/en/latest/swagger.html