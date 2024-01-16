from SQLyog import MySQLDatabase

from datetime import datetime

#manipulacao de dados
class ManipulacaoMySQL(MySQLDatabase):
    #Inicializa a função
    def __init__(self):
        super().__init__()

    #Pesquisa na tabela de processp
    def getProcessosPesquisar(self, sigla):
        sqlConsulta = f"SELECT numeroProcesso FROM _pesquisar WHERE siglaTribunal= '{sigla}' AND pesquisado='N';"
        return self.consultar(sqlConsulta)
    
    def getProcessosVerificacao(self, sigla):
        sqlConsulta = f"SELECT situacao FROM tjro WHERE tx_nr_ivt= '{sigla}' AND situacao='Nenhum processo encontrado';"
        return self.consultar(sqlConsulta)
    
    def getProcessosAtualizar(self, sigla):
        sqlConsulta1 = f"SELECT numeroProcesso FROM _pesquisar WHERE siglaTribunal= '{sigla}' AND atualizado='N';"
        return self.consultar(sqlConsulta1)
    
    

    #Atualiza o processo
    def setProcessoPesquisado(self, row:str, attr: dict, table_name: str):
        print(attr)
        key_value_pairs = ', '.join(f'{key}=%({key})s' for key in attr.keys())
        attr['numeroProcesso'] = row
        sqlAtualiza = f"UPDATE {table_name} SET {key_value_pairs} WHERE tx_nr_ivt=%(tx_nr_ivt)s;"
        pesquisado = {"atualizado":"S"}
        try:
            self.executarQueryComDicionario(sqlAtualiza, attr)
            self.setProcessoAtualizar(row, pesquisado, "_pesquisar")
        except Exception as err:
            print(f"Erro ao atualizar pesquisado. Erro: {err}")
            raise
        
        #Atualiza o processo
    def setProcessoAtualizar(self, row:str, attr: dict, table_name: str):
        print(attr)
        key_value_pairs = ', '.join(f'{key}=%({key})s' for key in attr.keys())
        attr['numeroProcesso'] = row
        sqlAtualiza = f"UPDATE {table_name} SET {key_value_pairs} WHERE numeroProcesso=%(numeroProcesso)s;"
        try:
            self.executarQueryComDicionario(sqlAtualiza, attr)
        except Exception as err:
            print(f"Erro ao atualizar pesquisado. Erro: {err}")
            raise
        
    #Devolve as chaves?
    def _returning_key_list_and_placeholders(self, attr:dict):
        print(attr)
        if 'dt' in attr:
            attr['data'] = datetime.strptime(attr['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
        keys_list = ', '.join([key for key in attr.keys()])
        placeholder = ', '.join([f'%({key})s' for key in attr.keys()])
        return keys_list, placeholder


    #Cria um novo processo
    def criarRegistro(self, row: str ,attr: dict, table_name: str):
        key_list, placeholders = self._returning_key_list_and_placeholders(attr)
        sqlInserir = f"INSERT INTO {table_name} ({key_list}) VALUES ({placeholders})"
        pesquisado = {"pesquisado":"S"}
        try:
            self.executarQueryComDicionario(sqlInserir, attr)
            self.setProcessoAtualizar(row, pesquisado, "_pesquisar")
        except BaseException as err:
            print(f"Erro ao criar registro. Erro: {err}")
            raise 
        


    def get_value(data_base, table, column, linha):
        # Conecte-se ao banco de dados SQLite
        conn = ManipulacaoMySQL._conectar(data_base)
        
        # Crie um cursor
        cursor = conn.cursor()
        
        # Execute a consulta SQL
        cursor.execute(f"SELECT {column} FROM {table} WHERE tx_nr_ivt = %s", (linha,))
        
        # Obtenha o resultado
        result = cursor.fetchone()
        
        # Feche a conexão
        conn.close()
        
        # Retorne o resultado
        if result is not None:
            return result[0]
        else:
            return None

        
    
    #Deleta um registro
    def deletarRegistroUmaCondicao(self, table_name: str, campoDaCondicao: str, valorDaCondicao) -> None:
        if type(valorDaCondicao) == type('str'):
            sqlDelete = f"DELETE FROM {table_name} WHERE {campoDaCondicao} = '{valorDaCondicao}'"
        else:
            sqlDelete = f"DELETE FROM {table_name} WHERE {campoDaCondicao} = {valorDaCondicao}"
        print(sqlDelete)

        try:
            cursor = self.conn.cursor()
            cursor.execute(sqlDelete)
            self.conn.commit()

        except BaseException as err:
            raise (f"Erro ao deletar registro. Erro: {err}")   

    #finaliza o programa
    def __del__(self):
        self.desconectar()