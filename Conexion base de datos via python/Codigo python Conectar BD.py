#Con este codigo podemos conectar la base de datos con python para hacer posteriores analisis

import psycopg2 # Importamos la librería psycopg2 para conectarnos a la base de datos PostgreSQL

try:
    # Intentamos establecer una conexión con la base de datos PostgreSQL
    connection = psycopg2.connect(
        host='localhost',  # Dirección del servidor de base de datos
        user='postgres',  # Nombre de usuario
        password='2410Oct',  # Contraseña del usuario
        database='Proyecto_Ingeneria',  # Nombre de la base de datos a la que queremos conectarnos
        port='5433', # Puerto en el que está escuchando el servidor de base de datos
    )
    #La configuración anterior depende del computador, pero mostramos en la que nos funciona a nosotros 
    print("Conexión exitosa") # Si la conexión es exitosa, imprimimos un mensaje
    cursor = connection.cursor() # Creamos un objeto cursor para ejecutar comandos SQL

    # En esta parte del codigo vamos a visualizar cada una de las tablas de las que esta compuesta el proyecto

    #Visualización de la tabla Pais
    cursor.execute("SELECT * FROM pais")  # Ejecutamos una consulta SQL para seleccionar todos los datos de la tabla "Pais"
    rows_pais = cursor.fetchall()  # Obtenemos todas las filas resultantes de la consulta
    for row in rows_pais:
        print(row)
    
    #Visualización de la tabla Ciudad
    cursor.execute("SELECT * FROM ciudad")  # Ejecutamos una consulta SQL para seleccionar todos los datos de la tabla "Ciudad"
    rows_ciudad = cursor.fetchall()  # Obtenemos todas las filas resultantes de la consulta
    for row in rows_ciudad:
        print(row)
    
    #Visualización de la tabla Aeropuerto
    cursor.execute("SELECT * FROM aeropuerto")  # Ejecutamos una consulta SQL para seleccionar todos los datos de la tabla "Aeropuerto"
    rows_aeropuerto = cursor.fetchall()  # Obtenemos todas las filas resultantes de la consulta
    for row in rows_aeropuerto:
        print(row)
    
    #Visualización de la tabla Empresa
    cursor.execute("SELECT * FROM empresa")  # Ejecutamos una consulta SQL para seleccionar todos los datos de la tabla "Empresa"
    rows_empresa = cursor.fetchall()  # Obtenemos todas las filas resultantes de la consulta
    for row in rows_empresa:
        print(row)

    #Visualización de la tabla Vuelo
    cursor.execute("SELECT * FROM vuelo")  # Ejecutamos una consulta SQL para seleccionar todos los datos de la tabla "Vuelo"
    rows_vuelo= cursor.fetchall()  # Obtenemos todas las filas resultantes de la consulta
    for row in rows_vuelo:
        print(row)

    #Visualización de la tabla Utiliza
    cursor.execute("SELECT * FROM utiliza")  # Ejecutamos una consulta SQL para seleccionar todos los datos de la tabla "Vuelo"
    rows_utiliza= cursor.fetchall()  # Obtenemos todas las filas resultantes de la consulta
    for row in rows_utiliza:
        print(row)

except Exception as ex:
    print(ex) # Si ocurre algún error durante la ejecución del bloque try imprimira error
    
finally:
    connection.close() # Finalmente, independientemente de si hubo éxito o error, cerramos la conexión a la base de datos
    print("Conexión finalizada") # Imprimimos un mensaje para indicar que la conexión ha sido cerrada