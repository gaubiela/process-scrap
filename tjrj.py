#importações
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import time, os
from datetime import datetime
from manipular import ManipulacaoMySQL
from SQLyog import MySQLDatabase

global j #variavel para verificar quantos processos tem
global numero_unico #variável que vai receber o número da coluna D
j = 1

#Pega o tempo da Coleta de dados
dt_cla1 = time.strftime("%d/%b/%Y")
dt_cla = datetime.strptime(dt_cla1, "%d/%b/%Y").strftime("%Y-%m-%d")

#função que permite verificar se um elemento está presente na página
def is_element_present( how, what): 
    try: browser.find_element(by=how, value=what)
    except NoSuchElementException as e: return False
    return True

def is_element_present_by_class(class_name): 
    try: 
        browser.find_element(by=By.CLASS_NAME, value=class_name)
    except NoSuchElementException as e: 
        return False
    return True

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

# Definir uma função que recebe um número de 20 caracteres e retorna o formato desejado
def formatar_numero(numero):
  # Verificar se o número tem 20 caracteres e não tem caracteres especiais
  if len(numero) == 20 and numero.isalnum():
    # Inserir os caracteres especiais usando a função format
    return "{}-{}.{}.{}.{}.{}".format(numero[:7], numero[7:9], numero[9:13], numero[13:14], numero[14:16], numero[16:])
  else:
    # Retornar uma mensagem de erro se o número não for válido
    return "Número inválido"

def formatar_movimentacao(numero):
    # Encontre a posição do primeiro traço no texto
    dash_position = numero.find('-')

    # Se um traço foi encontrado, pegue todo o texto até esse traço
    if dash_position != -1:
        data = numero[:dash_position - 1]
        tit = numero[dash_position + 1:]
    else:
        data = numero
        tit = ""
    dt_mvtc1 = datetime.strptime(data, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    return dt_mvtc1, tit

def formatar_partes(numero):
    # Encontre a posição do primeiro traço no texto
    dash_position = numero.find('-')
    ultimo_dash = numero.rfind('-')
    segundo_dash = numero.rfind('-', 0, ultimo_dash - 1)
    cpf_position = numero.find('CPF:')
    cnpj_position = numero.find("CNPJ:")
    OAB_position = numero.find('OAB')
    pr_position = numero.find('(')
    ultimo_parenteses = numero.rfind('(')
    barra_position = numero.find("\n")

    # Verifique se um parênteses foi encontrado
    if ultimo_parenteses != -1:
        # Encontre o parênteses de fechamento correspondente
        fechamento_parenteses = numero.rfind(')')
        
        # Verifique se um parênteses de fechamento foi encontrado
        if fechamento_parenteses != -1:
            # Extraia o texto entre os parênteses
            texto_entre_parenteses = numero[ultimo_parenteses+1 : fechamento_parenteses]
    
    # Se um traço foi encontrado, pegue todo o texto até esse traço
    if dash_position != -1:
        nm = numero[:dash_position - 1]
        if "OAB" in numero:
            oab = numero[OAB_position + 4 : segundo_dash - 1]
        else:
            oab = "não encontrado"
        if "CNPJ" in numero:
            cpf = numero[cnpj_position + 6: pr_position - 1]
        elif "CPF" in numero:
            cpf = numero[cpf_position + 5: pr_position - 1]
        else:
            cpf = "não encontrado"
    else:
        nm = numero[:barra_position]
        cpf = "não encontrado"
        oab = "não encontrado"
        
    if ultimo_parenteses == -1:
        texto_entre_parenteses = "ADVOGADO"
        
    return texto_entre_parenteses, nm, cpf, oab

def pega_parte_ativo(b, tx_nr_ivt):
    r = True
    while r:
        if is_element_present('xpath', f"/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[1]/div/div[2]/span/div/table/tbody/tr[{str(b)}]"):
            nm = browser.find_element(by=By.XPATH,value=f'/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[1]/div/div[2]/span/div/table/tbody/tr[{str(b)}]/td[1]/span/div/span').text.upper()
            print(nm)
            nm1 = nm.replace(" ", "")
            if any(substring in nm1 for substring in ["BANCODOBRASIL", "BANCODOBRASIL", "BRANCODOBRASIL", "BBLEASING", "BBADMINISTRADORA","BANCOBRASIL", "BANCOCOBRASIL","BANCODOBARSIL","BANCOBARSIL","BANCOBRSIL","BANCODOBRSIL","BANCOSOBRASIL","BANDODOBRASIL", "BACODOBRASIL","BACOBRASIL","BBFINANCEIRA","BB-FINANCEIRA","BB-ADMINISTRADORA","BB-LEASING", "B.B.", "BANCODOBRAIL","BB.","BBSEGUROS","BBCORRETORA","BANCODOBRFASIL","BANCOBRFASIL","BANCODEBRASIL","BANCOD0BRASIL","BANCODABRASIL","BBADMINISTRAÇAO","BBADMINSTRADORA","BBADMISTRADORA","BBSEGURO","BSEGURO","BCOD0BRASIL","BIMBOD0BRASIL","BANCODBRASIL","BANCODOBRASIIL","BANCODOBRASI","BANCODOBRASEL","BANCODOBRANSIL","BANCODOBRAISL","BANCODIBRASIL","BANCODUBRASIL","BANCODOBRASL"]):
                r = False
            else: 
                nm = nm.strip()
                tip_pct_prc, nm, cpf, oab = formatar_partes(nm)
                atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}", "tip_pct_prc":f"{tip_pct_prc}","nm":f"{nm}","cpf_cnpj":f"{cpf}","cd_oab":f"{oab}"}
                dbs.criarRegistro((row["numeroProcesso"]), atributos,'tjrj_partes')
                b += 1
        else: 
            r = False
    
def pega_parte_passivo(b, tx_nr_ivt):
    r = True
    while r:
        if is_element_present('xpath', f"/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div/div[2]/span/div/table/tbody/tr[{str(b)}]"):
            nm = browser.find_element(by=By.XPATH,value=f"/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div/div[2]/span/div/table/tbody/tr[{str(b)}]").text.upper()
            nm1 = nm.replace(" ", "")
            if any(substring in nm1 for substring in ["BANCODOBRASIL", "BANCODOBRASIL", "BRANCODOBRASIL", "BBLEASING", "BBADMINISTRADORA","BANCOBRASIL", "BANCOCOBRASIL","BANCODOBARSIL","BANCOBARSIL","BANCOBRSIL","BANCODOBRSIL","BANCOSOBRASIL","BANDODOBRASIL", "BACODOBRASIL","BACOBRASIL","BBFINANCEIRA","BB-FINANCEIRA","BB-ADMINISTRADORA","BB-LEASING", "B.B.", "BANCODOBRAIL","BB.","BBSEGUROS","BBCORRETORA","BANCODOBRFASIL","BANCOBRFASIL","BANCODEBRASIL","BANCOD0BRASIL","BANCODABRASIL","BBADMINISTRAÇAO","BBADMINSTRADORA","BBADMISTRADORA","BBSEGURO","BSEGURO","BCOD0BRASIL","BIMBOD0BRASIL","BANCODBRASIL","BANCODOBRASIIL","BANCODOBRASI","BANCODOBRASEL","BANCODOBRANSIL","BANCODOBRAISL","BANCODIBRASIL","BANCODUBRASIL","BANCODOBRASL"]):
                r = False
            else:
                nm = nm.strip()
                tip_pct_prc, nm, cpf, oab = formatar_partes(nm)
                atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}", "tip_pct_prc":f"{tip_pct_prc}","nm":f"{nm}","cpf_cnpj":f"{cpf}","cd_oab":f"{oab}"}
                dbs.criarRegistro((row["numeroProcesso"]), atributos,'tjrj_partes')
                b += 1
        else: 
            r = False 
                                        
def verificar_numero(numero):
    
    if numero[13:16] == '819':
        return True
    else:
        return False

def Take_information():
    #função para abrir a pagina
    browser.get('https://www3.tjrj.jus.br/consultaprocessual/#/conspublica#porNumero')
    original_window = browser.current_window_handle
    
    time.sleep(2)
    
    #Função que coloca o numero do processo da pagina
    if is_element_present_by_class('row'):
        if (len(str(row['numeroProcesso'])) == 20):
            if verificar_numero(row['numeroProcesso']):
                formatado = formatar_numero(row['numeroProcesso'])
                elemento = browser.find_element(by=By.CSS_SELECTOR, value=".form-control.ng-valid.ng-touched.ng-dirty")
                elemento.click()
                browser.find_element(by=By.XPATH,value='//*[@id="fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso"]').send_keys(formatado[0:25])
                try:
                    Alert(browser).accept()
                    tx_nr_ivt = row['numeroProcesso']
                    situacao = "Numero de processo inválido"
                    atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                    dbs.criarRegistro((row["numeroProcesso"]),atributos,'tjrj')
                except:
                    time.sleep(1)
                    browser.find_element(by=By.XPATH,value='//*[@id="fPP:searchProcessos"]').click()
                    
                    time.sleep(5)
                    
                    #Se tiver o campo, pegar os dados
                    if is_element_present( 'xpath', '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody/tr'):
                        j = 1 #Os processos iniciam no 0
                        t = 2
                        browser.find_element(by=By.XPATH,value="/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody/tr/td[1]/a").click()
                        
                        # Mude para a janela do pop-up
                        browser.switch_to.window(browser.window_handles[1])
                        if is_element_present( 'xpath', '/html/body/div[3]/div[4]/div[1]/dl/dt/span'):
                            Take_information()                    
                        tx_nr_ivt = row['numeroProcesso']
                        dt_dist = browser.find_element(by=By.XPATH,value="/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/div[1]/div[3]/table/tbody/tr[1]/td[2]/span/div/div[2]").text
                        dt_dist = datetime.strptime(dt_dist, "%d/%m/%Y").strftime("%Y-%m-%d")
                        cmr = browser.find_element(by=By.XPATH,value="/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/div[1]/div[3]/table/tbody/tr[2]/td[1]/span/div/div[2]").text
                        org_julgador = browser.find_element(by=By.XPATH,value="/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/div[1]/div[3]/table/tbody/tr[2]/td[3]/span/div/div[2]").text
                        cls = browser.find_element(by=By.XPATH,value="/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/div[1]/div[3]/table/tbody/tr[1]/td[3]/span/div/div[2]").text
                        asnt_ppl = browser.find_element(by=By.XPATH,value="/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/div/div[1]/div[3]/table/tbody/tr[1]/td[4]/span/div/div[2]/div").text
                        
                        atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","dt_dist":f"{dt_dist}","cls":f"{cls}","cmr":f"{cmr}","org_julgador":f"{org_julgador}",
                                        "cls":f"{cls}","asnt_ppl":f"{asnt_ppl}"}
                        dbs.criarRegistro((row["numeroProcesso"]),atributos,'tjrj')
                        
                        
                        if is_element_present( 'xpath', '//*[@id="j_id134:j_id266"]'):
                            b = 1
                            v = 5
                            if is_element_present( 'xpath', '/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[1]/div/div[2]/span/div/table/tfoot/tr/td/form/div/table/tbody/tr/td[4]'):
                                pages = browser.find_elements(By.CSS_SELECTOR, 'td.rich-datascr-inact, td.rich-datascr-act')
                                last_page = int(pages[-1].text) 
                                for i in range(1, last_page + 1):
                                    pega_parte_ativo(b, tx_nr_ivt)
                                    if is_element_present('xpath', f"/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[1]/div/div[2]/span/div/table/tfoot/tr/td/form/div/table/tbody/tr/td[{str(v)}]"):
                                        browser.find_element(by=By.XPATH,value=f"/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[1]/div/div[2]/span/div/table/tfoot/tr/td/form/div/table/tbody/tr/td[{last_page + 5}]").click()
                                        b = 1
                                        v += 1
                                        time.sleep(5)
                                    else:
                                        break
                            else:
                                pega_parte_ativo(b, tx_nr_ivt)
                        
                        if is_element_present( 'xpath', '//*[@id="j_id134:j_id330"]'):
                            b = 1
                            v = 5
                            if is_element_present( 'xpath', '/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div/div[2]/span/div/table/tfoot/tr/td/form/div/table/tbody/tr/td[4]'):
                                pages = browser.find_elements(By.CSS_SELECTOR, 'td.rich-datascr-inact, td.rich-datascr-act')
                                last_page = int(pages[-1].text) 
                                for i in range(1, last_page + 1):
                                    pega_parte_passivo(b, tx_nr_ivt)
                                    if is_element_present('xpath', f"/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div/div[2]/span/div/table/tbody/tr/td/form/div/table/tbody/tr/td[{str(v)}]"):
                                        browser.find_element(by=By.XPATH,value=f"/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[2]/div/div[2]/span/div/table/tbody/tr/td/form/div/table/tbody/tr/td[{last_page + 5}]").click()
                                        b = 1
                                        v += 1
                                        time.sleep(5)
                                    else:
                                        break
                            else:
                                pega_parte_passivo(b, tx_nr_ivt)
                                    
                        k = 1
                        if is_element_present("xpath",'/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[5]/div[2]/table/tbody/tr[1]'):
                            mvtc1 =  browser.find_element(by=By.XPATH,value=f'//*[@id="j_id134:processoEvento:0:j_id495"]').text
                            dt_mvtc1, tit_mvtc1 = formatar_movimentacao(mvtc1)
                            resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","tit_mvtc":f"{tit_mvtc1}"}
                            dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjrj_movimentacoes')
                            k += 1
                            if is_element_present("xpath","/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[5]/div[2]/table/tbody/tr[2]"):
                                mvtc1 =  browser.find_element(by=By.XPATH,value=f'//*[@id="j_id134:processoEvento:1:j_id495"]').text
                                dt_mvtc1, tit_mvtc1 = formatar_movimentacao(mvtc1)
                                resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","tit_mvtc":f"{tit_mvtc1}"}
                                dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjrj_movimentacoes')
                                k += 1
                                if is_element_present("xpath","/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[5]/div[2]/table/tbody/tr[3]"):
                                    mvtc1 =  browser.find_element(by=By.XPATH,value=f'//*[@id="j_id134:processoEvento:2:j_id495"]').text
                                    dt_mvtc1, tit_mvtc1 = formatar_movimentacao(mvtc1)
                                    resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","tit_mvtc":f"{tit_mvtc1}"}
                                    dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjrj_movimentacoes')
                                    k += 1
                                    if is_element_present("xpath","/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[5]/div[2]/table/tbody/tr[4]"):
                                        mvtc1 =  browser.find_element(by=By.XPATH,value=f'//*[@id="j_id134:processoEvento:3:j_id495"]').text
                                        dt_mvtc1, tit_mvtc1 = formatar_movimentacao(mvtc1)
                                        resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","tit_mvtc":f"{tit_mvtc1}"}
                                        dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjrj_movimentacoes')
                                        k += 1
                                        if is_element_present("xpath","/html/body/div[5]/div/div/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/div[5]/div[2]/table/tbody/tr[5]"):
                                            mvtc1 =  browser.find_element(by=By.XPATH,value=f'//*[@id="j_id134:processoEvento:4:j_id495"]').text
                                            dt_mvtc1, tit_mvtc1 = formatar_movimentacao(mvtc1)
                                            resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc":f"{dt_mvtc1}","tit_mvtc":f"{tit_mvtc1}"}
                                            dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjrj_movimentacoes')
                        else:
                            tit_mvtc1 = "Não encontrado"
                            resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}","tit_mvtc":f"{tit_mvtc1}"}
                            dbs.criarRegistro((row["numeroProcesso"]), resultado_mvtc, 'tjrj_movimentacoes')
                        # Feche o pop-up
                        browser.close()
                        
                        # Volte para a janela original
                        browser.switch_to.window(browser.window_handles[0])
                        
                    else:
                        tx_nr_ivt = row['numeroProcesso']
                        situacao = "Nenhum processo encontrado"
                        atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                        dbs.criarRegistro((row["numeroProcesso"]),atributos,'tjrj')
            else:
                tx_nr_ivt = row['numeroProcesso']
                situacao = "Numero fora da formatacao aceita"
                atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                dbs.criarRegistro((row["numeroProcesso"]),atributos,'tjrj')
        else:
            tx_nr_ivt = row['numeroProcesso']
            situacao = "Numero de processo inválido ou antigo"
            atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
            dbs.criarRegistro((row["numeroProcesso"]),atributos,'tjrj')
    else:
        Take_information()

#Inicio do código
if os.path.exists('./manipular.py'):
    #Abrir internamente a página
    browser = webdriver.Edge()
    browser.implicitly_wait(1) # seconds
    browser.maximize_window()
    browser.set_page_load_timeout(100)
    dbs = ManipulacaoMySQL()

    #função para abrir a pagina
    browser.get('https://www3.tjrj.jus.br/consultaprocessual/#/conspublica#porNumero')

    time.sleep(1)

    numero_unico = dbs.getProcessosPesquisar('TJRJ')
        
    #Função que pega os dados
    for row in numero_unico:
        print(row)
        Take_information()