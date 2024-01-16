import os
import mysql.connector as mysql_connector
from dotenv import load_dotenv

load_dotenv()

#classe banco de dados
class MySQLDatabase:
    def __init__(self):
        self.__host = '172.16.12.206'
        self.__username = 'scrap'
        self.__password= '15935728'
        self.__port= '3306'
        self.__database= 'scrap_tribunais'

        self.conn = self._conectar()
    
    #conecta no banco
    def _conectar(self):
        try:
            conexao = mysql_connector.connect(
                user = self.__username,
                password =self.__password,
                host = self.__host,
                port = self.__port,
                database = self.__database
            )

            # Imprime as variáveis
            print(f'User: {self.__username}')
            print(f'Password: {self.__password}')  
            print(f'Host: {self.__host}')
            print(f'Port: {self.__port}')
            print(f'Database: {self.__database}')

            if conexao.is_connected():
                db_info = conexao.get_server_info()
                cursor = conexao.cursor()
                sql = "SELECT DATABASE();"
                cursor.execute(sql)
                linha = cursor.fetchone()
                print('Conectado ao servidor de banco de dados MySQL, versão: ', db_info)
                print('Banco de dados selecionado: ',linha)
                return conexao

        except ConnectionError as e:
                print('Banco não conectado - erro:', e)
                return None
            

    #desconecta do banco de dados
    def desconectar(self):
        try:

            if  self.conn.is_connected():
                db_info =  self.conn.get_server_info()
                self.conn.close()
                print('Desconectado do servidor de banco de dados MySQL, versão: ', db_info)
                return self.conn

        except Exception as e:
                print('Banco não desconectado - erro:', e)
                return None                

    #consulta na tabela
    def consultar(self, query:str):
        if (not self.conn.is_connected() or self.conn is None):
            self.conn = self._conectar()

        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    #"busca" de dados
    def executarQueryComDicionario(self, query:str, params: dict):
        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            self.conn.commit()
        except TypeError as err:
            print(f'Um erro ocorreu durante a execução da query com dicionário. Erro: {err}')
            self.conn.rollback()

    #busca tabelas
    def getDbTabelas(self) -> list:
        listaTabelas = self.consultar('SHOW tables;')
        print(f'Lista de tabelas do banco de dados: {self.__database}')
        for tabela in listaTabelas:
            print(' '.join(['-', tabela['Tables_in_' + self.__database]]))

        return listaTabelas
    
    #Pesquisa na tabela    
    def _is_on_database(self, table_name: str) -> None:
        if table_name not in self.getDbTabelas():
            raise f"Tabela {table_name} não encontrada no banco de dados"
