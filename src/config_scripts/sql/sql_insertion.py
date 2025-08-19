# src/mysql/sql_insertion.py
__version__ = '1.1.4'

import mysql.connector
import json
import sys
import time
from mysql.connector import OperationalError, InterfaceError

# Add the path for the MySQL configuration if not already present
if r'V:\00_CONF_ROBOS\MYSQL\Conection' not in sys.path:
    sys.path.append(r'V:\00_CONF_ROBOS\MYSQL\Conection')

# Path to the MySQL configuration JSON file
json_file_path = r'V:\00_CONF_ROBOS\MYSQL\Conection\mysql_config.json'

class InsertSQL:
    def __init__(self, query: str = None):
        self.query = query
        
    def read_connection_info(self, filename: str = None) -> dict:
        """
        Read connection information from a JSON file.
        """
        try:
            with open(filename, 'r') as rJSON:
                connection_info = json.load(rJSON)
            return connection_info
        
        except json.JSONDecodeError as e:
            print(f"JSON Decode error: {e}")
            return None

    def connection(self):
        """
        Establishes a connection to the MySQL database using information from the JSON file.
        """
        self._connection_info = self.read_connection_info(json_file_path)

        if not self._connection_info:
            print("Erro ao ler configuração do MySQL")
            return None

        conn_params = {
            'host': self._connection_info['host_recovery'],
            'port': self._connection_info['port'],
            'user': self._connection_info['user'],
            'password': self._connection_info['password'],
            'database': self._connection_info['database'],
            'connection_timeout': 5000
        }

        try:
            connection = mysql.connector.connect(**conn_params)
            return connection
        
        except mysql.connector.Error as e:
            print(f"MySQL connection error: {e}")
            return None
    
    def mysql_insert(self, value: str = None) -> None:
        """
            Executes a MySQL insert query with error handling and proper resource cleanup.
        """
        self._connection = self.connection()
        if not self._connection:
            print("Falha ao conectar para insert")
            return

        cursor = None
        try:
            cursor = self._connection.cursor()
            if value is not None and len(value) > 0:
                cursor.executemany(self.query, value)
            else:
                cursor.execute(self.query)
            self._connection.commit()
        except mysql.connector.Error as e:
            print(f"Database error on insert: {e}")
            if self._connection:
                self._connection.rollback()
        finally:
            if cursor:
                cursor.close()
            if self._connection:
                self._connection.close()

    def mysql_query(self, values: str = None, retries: int = 3, delay: float = 10.0) -> tuple[list, object]:
        """
        Executes a MySQL query with optional variable substitution and fetches all results.
        Will retry if connection is lost (timeout or disconnect).
        """
        attempt = 0

        while attempt < retries:
            self._connection = self.connection()
            if not self._connection:
                print(f"Erro ao conectar ao MySQL (tentativa {attempt+1}/{retries})")
                attempt += 1
                time.sleep(delay)
                continue

            cursor = None
            try:
                cursor = self._connection.cursor()

                if values is not None:
                    if values:
                        cursor.execute(self.query, (values,))
                else:
                    cursor.execute(self.query)

                list_result = cursor.fetchall()
                self._connection.commit()

                return list_result, cursor

            except (OperationalError, InterfaceError) as e:
                print(f"MySQL OperationalError/InterfaceError: {e}. Tentando reconectar... (tentativa {attempt+1}/{retries})")
                attempt += 1
                time.sleep(delay)
                continue

            except mysql.connector.Error as e:
                print(f"MySQL query execution error: {e}")
                if self._connection:
                    self._connection.rollback()
                break

            finally:
                if cursor:
                    cursor.close()
                if self._connection:
                    self._connection.close()

        print("Não foi possível executar a query após múltiplas tentativas.")
        return [], None

    def delete(self) -> None:
        """
        Executes a delete query on the MySQL database with proper resource cleanup.
        """
        self._connection = self.connection()
        if not self._connection:
            print("Falha ao conectar para delete")
            return

        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(self.query)
            self._connection.commit()
        except mysql.connector.Error as e:
            print(f"MySQL delete error: {e}")
            if self._connection:
                self._connection.rollback()
        finally:
            if cursor:
                cursor.close()
            if self._connection:
                self._connection.close()