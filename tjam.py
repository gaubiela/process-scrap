#importações
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time, os
from datetime import datetime
from manipular import ManipulacaoMySQL
from SQLyog import MySQLDatabase


global j #contador
global numero_unico #Numero de processo
j = 1
#Pega o tempo da Coleta de dados
dt_cla1 = time.strftime("%d/%b/%Y")
dt_cla = datetime.strptime(dt_cla1, "%d/%b/%Y").strftime("%Y-%m-%d")


def organizar_linhas(texto):
    lines = texto.split('\n')
    result = []

    for line in lines:
        if ':' not in line:
            result.append(line)
        else:    
            key, value = line.split(':', 1)
            result.append(f"{value.strip()}({key.strip()})")

    return result

#função que permite verificar se um elemento está presente na página
def is_element_present( how, what): 
    try: browser.find_element(by=how, value=what)
    except NoSuchElementException as e: return False
    return True

#função que troca de aba
def redireciona_para_nova_janela():
 
    # Armazena a janela original
    janela_original = browser.current_window_handle
 
    # Aguarda até que uma nova janela seja aberta
    while len(browser.window_handles) == 1:
        pass
 
    # Muda o controle para a nova janela
    for janela in browser.window_handles:
        if janela != janela_original:
            browser.switch_to.window(janela)
            break

def verificar_numero(numero):
   
    if numero[13:16] == '804':
        return True
    else:
        return False
        
# Definir uma função que recebe um número de 20 caracteres e retorna o formato desejado
def formatar_numero(numero):
  # Verificar se o número tem 20 caracteres e não tem caracteres especiais
  if len(numero) == 20 and numero.isalnum():
    # Inserir os caracteres especiais usando a função format
    return "{}-{}.{}.{}.{}.{}".format(numero[:7], numero[7:9], numero[9:13], numero[13:14], numero[14:16], numero[16:])
  else:
    # Retornar uma mensagem de erro se o número não for válido
    return "Número inválido"        

def formatar_valor(valor):
    RS = valor.find('$')
    num = valor[RS + 1:].replace('.','')
    num = valor[RS + 1:].replace(',','.')
    num = float(num)
   
    return num

def formatar_data(dt):
    dt1 = dt[:10]
    dt1 += dt[13:19] 
    datetime_object = datetime.strptime(dt1, "%d/%m/%Y %H:%M")
    return datetime_object

def formatar_data_mov(dt):
    datetime_object = datetime.strptime(dt, "%d/%m/%Y")
    return datetime_object

def Take_information():
            #função para abrir a pagina
            browser.get('https://consultasaj.tjam.jus.br/cpopg/open.do')
           
            time.sleep(2)
            
            #Função que clica no botao
            browser.find_element(by=By.XPATH,value="/html/body/div[2]/form/section/div[2]/div/div[1]/div[1]/span[1]/input[1]").click()
            if is_element_present('xpath', "/html/body/div[2]/form/section/div[2]/div/div[1]/div[1]/span[1]/input[1]"):
                #verifica se o numero dado tem o tamanho necessario de um processo 
                if (len(str(row['numeroProcesso'])) == 20):
                    if verificar_numero(row['numeroProcesso']):
                        browser.find_element(by=By.XPATH,value="/html/body/div[2]/form/section/div[2]/div/div[1]/div[1]/span[1]/input[1]").send_keys((row['numeroProcesso'])[0:13])
                        browser.find_element(by=By.XPATH,value="/html/body/div[2]/form/section/div[2]/div/div[1]/div[1]/span[1]/input[3]").send_keys((row['numeroProcesso'])[16:20])
                        browser.find_element(by=By.XPATH,value="/html/body/div[2]/form/section/div[1]/div/select").click()
                        time.sleep(1)
                        #Variavel de verificação se digitou certo
                        revisao = browser.find_element(by=By.XPATH,value=f"/html/body/div[2]/form/section/div[2]/div/div[1]/div[1]/span[1]/input[4]").get_attribute("value")
                        Numero_formatado = formatar_numero(row["numeroProcesso"])
                        #Verificação se foi difitado corretamente
                        if revisao == Numero_formatado:
                            #função que aperta o botão de busca
                            browser.find_element(by=By.XPATH,value="/html/body/div[2]/form/section/div[4]/div/input").click()
                            if is_element_present("xpath", "/html/body/div[2]/div[3]/div[2]"):
                                browser.find_element(by=By.XPATH,value="/html/body/div[2]/div[2]/ul[1]/li/div/div[1]/div[1]").click()
                            else:
                                pass
                            
                            if is_element_present("xpath", "/html/body/div[5]"):
                                tx_nr_ivt = row['numeroProcesso']
                                situacao = "Segredo de justiça"
                                atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                                dbs.criarRegistro(row['numeroProcesso'],atributos,'tjam')
                            else:
                                #Verifica se o campo existe
                                if is_element_present( 'xpath', '/html/body/div[2]/div[3]'):
                                    tx_nr_ivt = row['numeroProcesso']
                                    contador_situacao = 2
                                    while contador_situacao < 3:
                                        if is_element_present( 'xpath', f'/html/body/div[1]/div[2]/div/div[1]/div/span[{contador_situacao}]'):
                                            if browser.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div[1]/div/span[2]").text:
                                                situacao = browser.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div[1]/div/span[2]").text
                                                if is_element_present("xpath","/html/body/div[1]/div[2]/div/div[1]/div/span[3]"):
                                                    situacao += "/"
                                                    situacao += browser.find_element(by=By.XPATH,value="/html/body/div[1]/div[2]/div/div[1]/div/span[3]").text
                                            contador_situacao += 1
                                        else:
                                            situacao = "Não encontrada"
                                            contador_situacao = 4
                                            
                                    existe = True
                                    contador = 1
                                    browser.find_element(by=By.XPATH,value="/html/body/div[1]/div[3]/div").click()
                                    cls = asnt_ppl = cmr = org_julgador = dt_dist = vl = None
                                    while existe:
                                        if is_element_present( 'xpath', f'/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/span'):
                                            if browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/span").text == "Classe":
                                                cls = browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/div").text
                                            elif browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/span").text == "Assunto":
                                                asnt_ppl = browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/div").text
                                            elif browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/span").text == "Foro":
                                                cmr = browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/div").text
                                            elif browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/span").text == "Vara":
                                                org_julgador = browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[2]/div/div[2]/div[{contador}]/div").text
                                            if is_element_present( 'xpath', f'/html/body/div[1]/div[3]/div/div[2]/div/div[{contador}]/span'):
                                                if browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[3]/div/div[2]/div/div[{contador}]/span").text == "Distribuição":
                                                    dt_dist = browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[3]/div/div[2]/div/div[{contador}]/div").text
                                                    dt_dist =formatar_data(dt_dist)
                                                elif browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[3]/div/div[2]/div/div[{contador}]/span").text == "Valor da ação":
                                                    vl = browser.find_element(by=By.XPATH,value=f"/html/body/div[1]/div[3]/div/div[2]/div/div[{contador}]/div").text
                                            contador += 1
                                        else:
                                            existe = False
                                    atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","dt_dist":f"{dt_dist}","cmr":f"{cmr}","org_julgador":f"{org_julgador}","vl":f"{vl}",
                                    "cls":f"{cls}","asnt_ppl":f"{asnt_ppl}","situacao":f"{situacao}"} 
                                    dbs.criarRegistro(row['numeroProcesso'],atributos,'tjam')
                                    print(atributos,"\n")
                                    
                                    #Verifica se é o banco do brasil e seus representantes
                                    d = True
                                    while d:
                                        #Verifica se tem participantes
                                        if is_element_present('xpath', f"/html/body/div[2]/div[3]"):
                                            #Se existir é verificado se tem uma posição de relevancia
                                            verificador_partes = True
                                            contador_tabelas = 1
                                            contador_partes = 1
                                            if is_element_present('xpath', f"/html/body/div[2]/div[3]/a"):
                                                browser.find_element(by=By.XPATH,value="/html/body/div[2]/div[3]/a").click()
                                                contador_tabelas += 1
                                            while verificador_partes:
                                                if is_element_present('xpath', f"/html/body/div[2]/table[{contador_tabelas}]/tbody/tr[{contador_partes}]/td[2]"):
                                                    take = browser.find_element(by=By.XPATH,value=f"/html/body/div[2]/table[{contador_tabelas}]/tbody/tr[{contador_partes}]/td[2]").text
                                                    tip_pct_prc = browser.find_element(by=By.XPATH,value=f"/html/body/div[2]/table[{contador_tabelas}]/tbody/tr[{contador_partes}]/td[1]").text.upper()
                                                    take1 = organizar_linhas(take)
                                                    verificador = True
                                                    while verificador:
                                                        verificador_pessoas = True
                                                        c = 0
                                                        while verificador_pessoas:
                                                            if c >= len(take1):
                                                                verificador_pessoas = False
                                                                verificador = False
                                                            else:
                                                                nm = take1[c]
                                                                nm1 = nm.replace(" ", "")
                                                                nm1 = nm1.upper()
                                                                if any(substring in nm1 for substring in ["BANCODOBRASIL", "BANCODOBRASIL", "BRANCODOBRASIL", "BBLEASING", "BBADMINISTRADORA","BANCOBRASIL", "BANCOCOBRASIL","BANCODOBARSIL","BANCOBARSIL","BANCOBRSIL","BANCODOBRSIL","BANCOSOBRASIL","BANDODOBRASIL", "BACODOBRASIL","BACOBRASIL","BBFINANCEIRA","BB-FINANCEIRA","BB-ADMINISTRADORA","BB-LEASING", "B.B.", "BANCODOBRAIL","BB.","BBSEGUROS","BBCORRETORA","BANCODOBRFASIL","BANCOBRFASIL","BANCODEBRASIL","BANCOD0BRASIL","BANCODABRASIL","BBADMINISTRAÇAO","BBADMINSTRADORA","BBADMISTRADORA","BBSEGURO","BSEGURO","BCOD0BRASIL","BIMBOD0BRASIL","BANCODBRASIL","BANCODOBRASIIL","BANCODOBRASI","BANCODOBRASEL","BANCODOBRANSIL","BANCODOBRAISL","BANCODIBRASIL","BANCODUBRASIL","BANCODOBRASL"]):
                                                                    contador_partes += 1
                                                                    c = len(take1)
                                                                else:
                                                                    atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}", "tip_pct_prc":f"{tip_pct_prc}","nm":f"{nm}"}
                                                                    dbs.criarRegistro(row['numeroProcesso'],atributos,'tjam_partes')
                                                                    print(atributos)
                                                                    verificador = False
                                                                c += 1
                                                        contador_partes += 1
                                                else:
                                                    verificador_partes = False                       
                                            contador_tabelas_mov = 2
                                            if is_element_present('xpath', f"/html/body/div[2]/div[3]/a"):
                                                """
                                                browser.find_element(by=By.XPATH,value="/html/body/div[2]/div[3]/a").click()"""
                                                contador_tabelas_mov = 3
                                            k = 1
                                            if is_element_present("xpath",f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[1]'):
                                                mvtc1 =  browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[1]/td[3]').text
                                                dt_mvtc1 = browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[1]/td[1]').text
                                                dt_mvtc1 =formatar_data_mov(dt_mvtc1)
                                                resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","mvtc":f"{mvtc1}"}
                                                dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjam_movimentacoes')
                                                print(resultado_mvtc)
                                                k += 1
                                                if is_element_present("xpath",f"/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[2]"):
                                                    mvtc1 =  browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[2]/td[3]').text
                                                    dt_mvtc1 = browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[2]/td[1]').text 
                                                    dt_mvtc1 =formatar_data_mov(dt_mvtc1)
                                                    resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","mvtc":f"{mvtc1}"}
                                                    dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjam_movimentacoes')
                                                    print(resultado_mvtc)
                                                    k += 1
                                                    if is_element_present("xpath",f"/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[3]"):
                                                        mvtc1 =  browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[3]/td[3]').text
                                                        dt_mvtc1 = browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[3]/td[1]').text
                                                        dt_mvtc1 =formatar_data_mov(dt_mvtc1)
                                                        resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","mvtc":f"{mvtc1}"}
                                                        dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjam_movimentacoes')
                                                        print(resultado_mvtc)
                                                        k += 1
                                                        if is_element_present("xpath",f"/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[4]"):
                                                            mvtc1 =  browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[4]/td[3]').text
                                                            dt_mvtc1 = browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[4]/td[1]').text 
                                                            dt_mvtc1 =formatar_data_mov(dt_mvtc1)
                                                            resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","mvtc":f"{mvtc1}"}
                                                            dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjam_movimentacoes')
                                                            print(resultado_mvtc)
                                                            k += 1
                                                            if is_element_present("xpath",f"/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[5]"):
                                                                mvtc1 =  browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[5]/td[3]').text
                                                                dt_mvtc1 = browser.find_element(by=By.XPATH,value=f'/html/body/div[2]/table[{contador_tabelas_mov}]/tbody[1]/tr[5]/td[1]').text 
                                                                dt_mvtc1 =formatar_data_mov(dt_mvtc1)
                                                                resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","mvtc":f"{mvtc1}"}
                                                                dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjam_movimentacoes')
                                                                print(resultado_mvtc)
                                            else:
                                                mvtc1 = "Não encontrado"
                                                resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}","mvtc":f"{mvtc1}"}
                                                dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjam_movimentacoes')
                                                print(atributos)
                                            d = False
                                        else: 
                                            d = False
                                else:
                                    #Se não tiver resultados, retorna não encontrado
                                    if is_element_present( 'xpath', '/html/body/div[2]/div[1]/table/tbody/tr[2]'):
                                        tx_nr_ivt = row['numeroProcesso']
                                        situacao = "Nenhum processo encontrado"
                                        atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                                        dbs.criarRegistro(row['numeroProcesso'],atributos,'tjam')
                                        print(atributos)

                                    #Se não tiver a mensagem de erro, pesquisa se novo
                                    else:
                                        Take_information()
                        #Se não foi digitado certo, tenta de novo
                        else:
                            Take_information()
                    else:
                        tx_nr_ivt = row['numeroProcesso']
                        situacao = "Numero fora da formatação aceita"
                        atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                        dbs.criarRegistro(row['numeroProcesso'],atributos,'tjam')
                        print(atributos)
                #Se não tiver o tamanho necessario, é inválido
                else:
                    tx_nr_ivt = row['numeroProcesso']
                    situacao = "Numero de processo inválido/antigo"
                    atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                    dbs.criarRegistro(row['numeroProcesso'],atributos,'tjam')
                    print(atributos)
            #Se não clicou, tenta de novo
            else:
                Take_information()

def programa():
    #Inicio do código
    if os.path.exists('./manipular.py'):
        #Abrir internamente a página
        global browser
        browser = webdriver.Edge()
        browser.implicitly_wait(1) # seconds
        browser.maximize_window()
        browser.set_page_load_timeout(500)
        global db
        db = MySQLDatabase()
        global dbs
        dbs = ManipulacaoMySQL()
        
        #função para abrir a pagina
        browser.get('https://consultasaj.tjam.jus.br/cpopg/open.do')

        time.sleep(1)
        
        #definicao do numero de processo
        numero_unico = dbs.getProcessosPesquisar("TJAM")
                
        #Função que pega os dados
        global row
        for row in reversed(numero_unico):
            Take_information()
            

programa()
            