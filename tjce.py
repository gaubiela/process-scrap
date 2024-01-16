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

def Take_information():
            #função para abrir a pagina
            browser.get('https://consultaprocesso.tjce.jus.br/scpu-web/pages/administracao/consultaProcessual.jsf?pesquisaparte')
            original_window = browser.current_window_handle
           
            time.sleep(2)
            
            #Função que clica no botao
            browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[2]/div[2]/div/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/div/div[2]").click()
            if is_element_present('xpath', "//*[@id='numeroProcesso']"):
                #verifica se o numero dado tem o tamanho necessario de um processo 
                if (len(str(row['numeroProcesso'])) == 20):
                    browser.find_element(by=By.XPATH,value="//*[@id='numeroProcesso']").send_keys((row['numeroProcesso'])[0:20])
                    time.sleep(1)
                    #Variavel de verificação se digitou certo
                    revisao = browser.find_element(by=By.XPATH,value=f"//*[@id='numeroProcesso']").get_attribute("value")
                
                    #função que aperta o botão de busca
                    browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[2]/div[2]/table[2]/tbody/tr/td[1]/button/span[2]").click()
                    #Verificação se foi difitado corretamente
                    if revisao == row['numeroProcesso']:
                        
                        #Verifica se o campo existe
                        if is_element_present( 'xpath', '//*[@id="tabelaProcessos"]'):
                            j = 1 #Os processos iniciam no 0
                            t = 2
                            while True:
                                #Se a coluna de dados estiver presente na pesquisa verifica se é a que a gente quer
                                if is_element_present( 'xpath', f'/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]'):
                                    #Verifica se a aba do orgao existe
                                    if is_element_present('xpath', f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[8]/div[2]"):
                                            org_julgador1 = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{str(j)}]/td[1]/div[5]/div[2]").text.upper()
                                            #Verifica se o processo é o principal
                                            if  any(substring in org_julgador1 for substring in ["VARA", "JUIZADO", "JEC", "VARA CÍVEL", "CEJUSC", "NUCLEO DE JUSTIÇA", "NUCLEO", "NÚCLEO DE JUSTIÇA", "NÚCLEO"]):
                                                print("Achei")
                                                sis = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[8]/div[2]").text
                                                #Se o processo não tiver o sistema definido é muito velho e não tem todas as infomações e pegamos apenas a capa com os dados disponiveis
                                                if (sis == ''):
                                                    #Pega os dados relevantes para a analise e armazenamento
                                                    situacao = "Processo transferido"
                                                    tx_nr_ivt = row['numeroProcesso']
                                                    dt_ptl = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[2]/div[2]").text
                                                    dt_ptl = datetime.strptime(dt_ptl, "%d/%m/%Y").strftime("%Y-%m-%d")
                                                    dt_dist = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[3]/div[2]").text
                                                    dt_dist = datetime.strptime(dt_dist, "%d/%m/%Y").strftime("%Y-%m-%d")
                                                    cmr = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[4]/div[2]").text
                                                    org_julgador = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[5]/div[2]").text
                                                    cls = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[6]/div[2]").text
                                                    asnt_ppl = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[7]/div[2]").text
                                                    sis = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[9]/div[2]").text
                                                    atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}", "dt_ptl":f"{dt_ptl}","dt_dist":f"{dt_dist}","cmr":f"{cmr}","org_julgador":f"{org_julgador}",
                                                                "cls":f"{cls}","asnt_ppl":f"{asnt_ppl}","situacao":f"{situacao}","sis":f"{sis}"}
                                                    dbs.criarRegistro(row['numeroProcesso'],atributos,'tjce1')
                                                    
                                                    #Verifica se é o banco do brasil e seus representantes
                                                    r = True
                                                    b = 1
                                                    while r:
                                                        #Verifica se tem participantes
                                                        if is_element_present('xpath', f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(b)}]/div[1]"):
                                                            #Se existir é verificado se tem uma posição de relevancia
                                                            tip_pct_prc = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(b)}]/div[1]").text.upper()
                                                            if any(substring in tip_pct_prc for substring in ["REQUERIDO", "REQUERENTE", "EMBARGADO", "EMBARGANTE", "PROMOVIDO", "PROMOVENTE", "REU", "AUTOR", "REPRESENTANTE", "ESTAGIÁRIO", "EXEQUIDO", "EXEQUENTE", "TERCEITO","EXECUTADO", "EXCUTADO","ESPÓLIO","APELANTE","APELADO"]):
                                                                nm = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(b)}]/div[2]").text.upper()
                                                                nm1 = nm.replace(" ", "")
                                                                #Se for do banco do brasil deve pular até quem não é
                                                                if any(substring in nm1 for substring in ["BANCODOBRASIL", "BANCODOBRASIL", "BRANCODOBRASIL", "BBLEASING", "BBADMINISTRADORA","BANCOBRASIL", "BANCOCOBRASIL","BANCODOBARSIL","BANCOBARSIL","BANCOBRSIL","BANCODOBRSIL","BANCOSOBRASIL","BANDODOBRASIL", "BACODOBRASIL","BACOBRASIL","BBFINANCEIRA","BB-FINANCEIRA","BB-ADMINISTRADORA","BB-LEASING", "B.B.", "BANCODOBRAIL","BB.","BBSEGUROS","BBCORRETORA","BANCODOBRFASIL","BANCOBRFASIL","BANCODEBRASIL","BANCOD0BRASIL","BANCODABRASIL","BBADMINISTRAÇAO","BBADMINSTRADORA","BBADMISTRADORA","BBSEGURO","BSEGURO","BCOD0BRASIL","BIMBOD0BRASIL","BANCODBRASIL","BANCODOBRASIIL","BANCODOBRASI","BANCODOBRASEL","BANCODOBRANSIL","BANCODOBRAISL","BANCODIBRASIL","BANCODUBRASIL","BANCODOBRASL"]):
                                                                    #Será feita uma contagem até aquele não envolvido com o banco
                                                                    b += 1  
                                                                    q = True
                                                                    while q: 
                                                                        if is_element_present('xpath', f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(b)}]/div[1]"):
                                                                            tip_pct_prc = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(b)}]/div[1]").text.upper()
                                                                            if "REPRESENTANTE" in tip_pct_prc:
                                                                                if is_element_present('xpath', f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(b + 1)}]/div[1]"):
                                                                                    b += 1
                                                                                else:
                                                                                    q = False
                                                                            else: 
                                                                                q = False
                                                                        else:
                                                                            q = False
                                                                #Salva aqueles que não são do banco
                                                                else: 
                                                                    atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}", "tip_pct_prc":f"{tip_pct_prc}","nm":f"{nm}"}
                                                                    dbs.criarRegistro(row['numeroProcesso'],atributos,'tjce_partes')
                                                                    b += 1
                                                            else: 
                                                                r = False
                                                        else: 
                                                            r = False   
                                                    break
                                                
                                                #Verifica se o processo foi transferido ou não a outro foro
                                                c = True    
                                                while c :
                                                        org_julgador1 = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{str(j)}]/td[1]/div[5]/div[2]").text.upper()
                                                        if  any(substring in org_julgador1 for substring in ["VARA", "JUIZADO", "JEC", "VARA CÍVEL", "CEJUSC", "NUCLEO DE JUSTIÇA", "NUCLEO", "NÚCLEO DE JUSTIÇA", "NÚCLEO"]):
                                                            if ((browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[8]/div[2]").text in "Remetido a outro foro ") or (browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j}]/td[1]/div[8]/div[2]").text == "Remetido a outro foro ")):
                                                                if is_element_present('xpath', f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j + 1}]/td[1]/div[8]/div[2]"):
                                                                    j += 1
                                                                else:
                                                                    j -= 1
                                                                    c = False  
                                                            else:
                                                                c = False    
                                                        else:
                                                            c = False   
                                                #Clica no link que leva ao processo inteiro
                                                
                                                if is_element_present('xpath', f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[2]/td[1]/div[1]/div[2]") == False:
                                                    browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr/td[1]/div[1]/div[2]").click()
                                                else:
                                                    browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{str(j)}]/td[1]/div[1]/div[2]").click()
                                                #Deixa salva a janela que estava e vai para a do processo
                                                redireciona_para_nova_janela()
                                                
                                                #Pega do dados relevantes do processo
                                                tx_nr_ivt = row['numeroProcesso']
                                                while is_element_present('xpath',"/html/body/div[6]/form/div[4]/div[2]/span/div[3]/div[2]") == False:
                                                    Take_information()
                                                dt_ptl = browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[4]/div[2]/span/div[3]/div[2]").text
                                                dt_ptl = datetime.strptime(dt_ptl, "%d/%m/%Y").strftime("%Y-%m-%d")
                                                dt_dist = browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[4]/div[2]/span/div[4]/div[2]").text
                                                dt_dist = datetime.strptime(dt_dist, "%d/%m/%Y").strftime("%Y-%m-%d")
                                                cmr = browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[4]/div[2]/span/div[5]/div[2]").text
                                                org_julgador = browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[4]/div[2]/span/div[6]/div[2]").text
                                                cls = browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[4]/div[2]/span/div[7]/div[2]").text
                                                asnt_ppl = browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[4]/div[2]/span/div[8]/div[2]").text
                                                situacao = browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[4]/div[2]/span/div[9]/div[2]").text
                                                sis = browser.find_element(by=By.XPATH,value="/html/body/div[6]/form/div[4]/div[2]/span/div[10]/div[2]").text
                                                
                                                #Verifica se é o banco do brasil e seus representantes
                                                d = True
                                                while d:
                                                    #Verifica se tem participantes
                                                    if is_element_present('xpath', f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(t)}]/div[1]"):
                                                        #Se existir é verificado se tem uma posição de relevancia
                                                        tip_pct_prc = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(t)}]/div[1]").text.upper()
                                                        if any(substring in tip_pct_prc for substring in ["REQUERIDO", "REQUERENTE", "EMBARGADO", "EMBARGANTE", "PROMOVIDO", "PROMOVENTE", "REU", "AUTOR", "REPRESENTANTE", "ESTAGIÁRIO", "EXEQUIDO", "EXEQUENTE", "TERCEITO","EXECUTADO", "EXCUTADO","ESPÓLIO","APELANTE","APELADO"]):
                                                            nm = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(t)}]/div[2]").text.upper()
                                                            nm1 = nm.replace(" ", "")
                                                            #Se for do banco do brasil deve pular até quem não é
                                                            if any(substring in nm1 for substring in ["BANCODOBRASIL", "BANCODOBRASIL", "BRANCODOBRASIL", "BBLEASING", "BBADMINISTRADORA","BANCOBRASIL", "BANCOCOBRASIL","BANCODOBARSIL","BANCOBARSIL","BANCOBRSIL","BANCODOBRSIL","BANCOSOBRASIL","BANDODOBRASIL", "BACODOBRASIL","BACOBRASIL","BBFINANCEIRA","BB-FINANCEIRA","BB-ADMINISTRADORA","BB-LEASING", "B.B.", "BANCODOBRAIL","BB.","BBSEGUROS","BBCORRETORA","BANCODOBRFASIL","BANCOBRFASIL","BANCODEBRASIL","BANCOD0BRASIL","BANCODABRASIL","BBADMINISTRAÇAO","BBADMINSTRADORA","BBADMISTRADORA","BBSEGURO","BSEGURO","BCOD0BRASIL","BIMBOD0BRASIL","BANCODBRASIL","BANCODOBRASIIL","BANCODOBRASI","BANCODOBRASEL","BANCODOBRANSIL","BANCODOBRAISL","BANCODIBRASIL","BANCODUBRASIL","BANCODOBRASL"]):
                                                                t += 1
                                                                a = True
                                                                while a: 
                                                                    if is_element_present('xpath', f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(t)}]/div[1]"):
                                                                        tip_pct_prc = browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(t)}]/div[1]").text.upper()
                                                                        if ((tip_pct_prc.find("REPRESENTANTE") > 0) or ("REPRESENTANTE" in tip_pct_prc)):
                                                                            if is_element_present('xpath', f"/html/body/div[6]/form/div[5]/div[2]/span/div[{str(t + 1)}]/div[1]"):
                                                                                t += 1
                                                                            else:
                                                                                a = False
                                                                        else: 
                                                                            a = False
                                                                    else:
                                                                        a = False
                                                            #Salva aqueles que não são do banco
                                                            else: 
                                                                atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}", "tip_pct_prc":f"{tip_pct_prc}","nm":f"{nm}"}
                                                                dbs.criarRegistro(row['numeroProcesso'],atributos,'tjce_partes')
                                                                t += 1
                                                        else: 
                                                            d = False
                                                    else: 
                                                        d = False
                                                
                                                #Salva todos os dados da capa
                                                atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}", "dt_ptl":f"{dt_ptl}","dt_dist":f"{dt_dist}","cmr":f"{cmr}","org_julgador":f"{org_julgador}",
                                                                "cls":f"{cls}","asnt_ppl":f"{asnt_ppl}","situacao":f"{situacao}","sis":f"{sis}"}
                                                dbs.criarRegistro(row['numeroProcesso'],atributos,'tjce1')
                                                
                                                #Salva todos os dados das movimentações
                                                k = 1
                                                #dados da movimentação 1
                                                if is_element_present("xpath","/html/body/div[6]/form/div[6]/div[2]/span/div[2]/div[1]"):
                                                    dt_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[2]/div[1]").text
                                                    dt_mvtc1 = datetime.strptime(dt_mvtc1, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
                                                    tit_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[2]/div[2]").text
                                                    mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[2]/div[4]").text
                                                    resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc1":f"{dt_mvtc1}","tit_mvtc1":f"{tit_mvtc1}","mvtc1":f"{mvtc1}"}
                                                    dbs.criarRegistro(row['numeroProcesso'],resultado_mvtc, 'tjce_movimentações1')
                                                    k += 1
                                                    #dados da movimentação 2
                                                    if is_element_present("xpath","/html/body/div[6]/form/div[6]/div[2]/span/div[3]/div[1]"):
                                                        dt_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[3]/div[1]").text
                                                        dt_mvtc1 = datetime.strptime(dt_mvtc1, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
                                                        tit_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[3]/div[2]").text
                                                        mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[3]/div[4]").text
                                                        resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc1":f"{dt_mvtc1}","tit_mvtc1":f"{tit_mvtc1}","mvtc1":f"{mvtc1}"}
                                                        dbs.criarRegistro(row['numeroProcesso'],resultado_mvtc, 'tjce_movimentações1')
                                                        k += 1
                                                        #dados da movimentação 3
                                                        if is_element_present("xpath","/html/body/div[6]/form/div[6]/div[2]/span/div[4]/div[1]"):
                                                            dt_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[4]/div[1]").text
                                                            dt_mvtc1 = datetime.strptime(dt_mvtc1, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
                                                            tit_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[4]/div[2]").text
                                                            mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[4]/div[4]").text
                                                            resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc1":f"{dt_mvtc1}","tit_mvtc1":f"{tit_mvtc1}","mvtc1":f"{mvtc1}"}
                                                            dbs.criarRegistro(row['numeroProcesso'],resultado_mvtc, 'tjce_movimentações1')
                                                            k += 1
                                                            #dados da movimentação 4
                                                            if is_element_present("xpath","/html/body/div[6]/form/div[6]/div[2]/span/div[5]/div[1]"):
                                                                dt_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[5]/div[1]").text
                                                                dt_mvtc1 = datetime.strptime(dt_mvtc1, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
                                                                tit_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[5]/div[2]").text
                                                                mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[5]/div[4]").text
                                                                resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc1":f"{dt_mvtc1}","tit_mvtc1":f"{tit_mvtc1}","mvtc1":f"{mvtc1}"}
                                                                dbs.criarRegistro(row['numeroProcesso'],resultado_mvtc, 'tjce_movimentações1')
                                                                k += 1
                                                                #dados da movimentação 5
                                                                if is_element_present("xpath","/html/body/div[6]/form/div[6]/div[2]/span/div[6]/div[1]"):
                                                                    dt_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[6]/div[1]").text
                                                                    dt_mvtc1 = datetime.strptime(dt_mvtc1, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
                                                                    tit_mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[6]/div[2]").text
                                                                    mvtc1 =  browser.find_element(by=By.XPATH,value=f"/html/body/div[6]/form/div[6]/div[2]/span/div[6]/div[4]").text
                                                                    resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}", "dt_mvtc1":f"{dt_mvtc1}","tit_mvtc1":f"{tit_mvtc1}","mvtc1":f"{mvtc1}"}
                                                                    dbs.criarRegistro(row['numeroProcesso'],resultado_mvtc, 'tjce_movimentações1')
                                                #Se não tiver dados, deixa a mensagem que não a movimentações
                                                else:
                                                    tit_mvtc1 = "Não encontrado"
                                                    resultado_mvtc = {"tx_nr_ivt":f"{tx_nr_ivt}({k})","dt_cla":f"{dt_cla}","tit_mvtc1":f"{tit_mvtc1}"}
                                                    dbs.criarRegistro(row['numeroProcesso'],resultado_mvtc, 'tjce_movimentações1')
                                                    #Volta a pagina inicial
                                                    browser.close()
                                                    browser.switch_to.window(original_window)
                                                    break
                                                #Volta a pagina inicial
                                                browser.close()
                                                browser.switch_to.window(original_window)
                                                break
                                            #Se não for processo principal é desconsiderado
                                            else:
                                                if is_element_present( 'xpath', f'/html/body/div[6]/form/div[3]/div[2]/table/tbody/tr[{j+1}]/td[1]'):
                                                    j += 1
                                                else:
                                                    tx_nr_ivt = row['numeroProcesso']
                                                    situacao = "Nenhum processo principal/primario encontrado"
                                                    atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                                                    dbs.criarRegistro(row['numeroProcesso'],atributos,'tjce1')
                                                    break                                       
                                    #Se não existir é segredo de justiça
                                    else:
                                        tx_nr_ivt = row['numeroProcesso']
                                        situacao = "Segredo de justiça"
                                        atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                                        dbs.criarRegistro(row['numeroProcesso'],atributos,'tjce1')
                                        break
                                
                                #Se não for verifica na proxima aba
                                else:
                                    break
                        else:
                            #Se não tiver resultados, retorna não encontrado
                            if is_element_present( 'xpath', '/html/body/div[6]/form/span/span/h4'):
                                tx_nr_ivt = row['numeroProcesso']
                                situacao = "Nenhum processo encontrado"
                                atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                                dbs.criarRegistro(row['numeroProcesso'],atributos,'tjce1')

                            #Se não tiver a mensagem de erro, pesquisa se novo
                            else:
                                Take_information()
                    #Se não foi digitado certo, tenta de novo
                    else:
                        Take_information()
                #Se não tiver o tamanho necessario, é inválido
                else:
                    tx_nr_ivt = row['numeroProcesso']
                    situacao = "Numero de processo inválido"
                    atributos = {"tx_nr_ivt":f"{tx_nr_ivt}","dt_cla":f"{dt_cla}","situacao":f"{situacao}"}
                    dbs.criarRegistro(row['numeroProcesso'],atributos,'tjce1')
            #Se não clicou, tenta de novo
            else:
                Take_information()


#Inicio do código
if os.path.exists('./manipular.py'):
      #Abrir internamente a página
      browser = webdriver.Edge()
      browser.implicitly_wait(1) # seconds
      browser.maximize_window()
      browser.set_page_load_timeout(500)
      db = MySQLDatabase()
      dbs = ManipulacaoMySQL()
      
      #função para abrir a pagina
      browser.get('https://consultaprocesso.tjce.jus.br/scpu-web/pages/administracao/consultaProcessual.jsf?pesquisaparte')

      time.sleep(1)
      
      #definicao do numero de processo
      numero_unico = dbs.getProcessosPesquisar()
            
        #Função que pega os dados
      for row in reversed(numero_unico):
            Take_information()
            