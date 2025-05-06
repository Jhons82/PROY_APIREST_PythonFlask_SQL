/** Usando @@SERVERNAME **/
SELECT @@SERVERNAME AS NombreServidor;

/** Usando SERVERPROPERTY **/
SELECT SERVERPROPERTY('MachineName') AS NombreMaquina, 
       SERVERPROPERTY('ServerName') AS NombreServidor, 
       SERVERPROPERTY('InstanceName') AS NombreInstancia;

/** Crear BD **/
CREATE DATABASE proy_apirest_pythonflask_sql

USE proy_apirest_pythonflask_sql

/** Crear tabla users */
CREATE TABLE users (
	user_id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
	user_nombre VARCHAR(150) NOT NULL,
	user_apellido VARCHAR(150) NOT NULL,
	title VARCHAR(150) NOT NULL,
	address VARCHAR(150) NOT NULL
)

/* Agregar columna a la tabla users */
ALTER TABLE users ADD estado INT NULL

SELECT * FROM users

/* Insertar valores a la tabla users */
INSERT INTO users (user_nombre, user_apellido, title, address)
		VALUES ('John', 'hards', 'Ingeniero', 'Av. Garcilazo'),
				('Joel', 'Carren', 'Doctor', 'Av. Flores'),
				('Carl', 'Gerrad', 'Abogado', 'Av. Lagunas'),
				('Simons', 'sweet', 'Arquitecto', 'Av. Santa Elisa'),
				('Alice', 'smile', 'Antropologa', 'Av. Eternal')

/* Actualizar los datos de la nueva columna de la tabla users */
UPDATE users
SET
	estado = 1


/* Habilitar sa y contraseña */
ALTER LOGIN sa ENABLE;
ALTER LOGIN sa WITH PASSWORD = '969392668jhon';

/************************************************************************/
/********************       STORAGE PROCEDURE      **********************/
/************************************************************************/

/* LISTA DE USUARIOS*/
CREATE PROCEDURE SP_L_USERS_01
AS
BEGIN
	SELECT * FROM users
END

/* LISTA DE USUARIO POR ID */
CREATE PROCEDURE SP_L_USERS_02
@user_id INT
AS
BEGIN
	SELECT * FROM users WHERE user_id = @user_id
END

EXEC SP_L_USERS_02 1

/* REGISTRAR NUEVO USUARIO EN LA TABLA */
CREATE PROCEDURE SP_I_USERS_01
@user_nombre varchar(150),
@user_apellido VARCHAR(150),
@title VARCHAR(150),
@address VARCHAR(150)
AS
BEGIN
	INSERT INTO users (user_nombre, user_apellido, title, address, estado)
	VALUES
		(@user_nombre, @user_apellido, @title, @address, 1)
END

/* ACTUALIZAR UN REGISTRO DE LA TABLA USERS SEGÚN SU ID */
CREATE PROCEDURE SP_U_USERS_01
@user_id INT,
@user_nombre VARCHAR(150),
@user_apellido VARCHAR(150),
@title VARCHAR(150),
@address VARCHAR(150),
@estado INT
AS
BEGIN
	UPDATE users
	SET
		user_nombre = @user_nombre,
		user_apellido = @user_apellido,
		title = @title,
		address = @address,
		estado = @estado
	WHERE
		user_id = @user_id
END

/* ELIMINAR EL REGISTRO DE LA TABLA USERS (estado es igual a 0) */
CREATE PROCEDURE SP_D_USERS_01
@user_id INT
AS
BEGIN
	UPDATE users
	SET
		estado = 0
	WHERE
		user_id = @user_id
END

select * from users