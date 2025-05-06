import pyodbc
#TODO: Verificar la lista de controladores ODBC intalados en el sistema operativo 
#TODO: que pyODBC puede usar para conectarse a base de datos
""" print(pyodbc.drivers())
 """

#TODO: config de conexión a SQL SERVER
#TODO: Cadena de conexión
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LAPTOP-LCRALN5G\\SQLEXPRESS;"
    "DATABASE=proy_apirest_pythonflask_sql;"
    "UID=sa;"
    "PWD=969392668jhon;"
)

#TODO: Establecer conexión con BD
conn = pyodbc.connect(conn_str)

#TODO: Cursor - Realiza solicitudes a la base de datos
cursor = conn.cursor()

try:
    #TODO: Ejecuta la consulta SQL
    cursor.execute("SP_L_USERS_01")

    #TODO: Si todo es correcto, recupera y guarda en rows la info de la consulta
    rows = cursor.fetchall()

    #TODO: Itera lo obtenido y las imprime una a una
    for row in rows:
        print(row)

#TODO: Si existe error durante la ejecución, envia un mensaje con la descripción del error
except Exception as e:
    print (f"Error: {str(e)}")

#TODO: Cierre del cursor y la conexión
finally:
    if cursor:
        cursor.close()
    
    if conn:
        conn.close()