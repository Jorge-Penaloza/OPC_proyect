import mysql.connector

class clienteDBOPC:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    def get_servers(self):
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute("SELECT id FROM ServidorOPC WHERE habilitacion = 1")
        
        #servidor = db_cursor.fetchone()
        servidor = db_cursor.fetchall()
        db_cursor.close()
        return servidor

    def get_server_by_id(self, id_servidor):
        db_cursor = self.db_connection.cursor(dictionary=True)
        db_cursor.execute("SELECT * FROM ServidorOPC WHERE id = %s", (id_servidor,))
        servidor = db_cursor.fetchone()
        db_cursor.close()
        return servidor
    
    def get_data_matrix(self, id_servidor):
        db_cursor = self.db_connection.cursor()
        db_cursor.execute("SELECT * FROM TagOPC WHERE idServidor = %s", (id_servidor,))
        data_matrix = db_cursor.fetchall()
        db_cursor.close()
        return data_matrix
    
    def get_field_names(self):
        db_cursor = self.db_connection.cursor()
        db_cursor.execute("DESCRIBE TagOPC")
        field_names = [field[0] for field in db_cursor.fetchall()]
        db_cursor.close()
        return field_names

