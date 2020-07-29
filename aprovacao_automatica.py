from selenium import webdriver
import time
import datetime
from dotenv import load_dotenv
import os
load_dotenv()

username = os.getenv('ADP_USER')
password = os.getenv('ADP_PASSWORD')

options = webdriver.ChromeOptions()

options.add_argument('window-size=1920x1080')
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('http://www.adpexpert.com.br')
time.sleep(1)


def login():
    # Preencher dados para Loging
    element_login = driver.find_element_by_id('login')
    element_password = driver.find_element_by_id('login-pw')

    element_login.send_keys(username)
    element_password.send_keys(password)

    # Fazer o Login
    loggin_button = driver.find_element_by_xpath('//form//button')
    loggin_button.click()
    time.sleep(2)


def ir_para_inconsistencias():
    # Clicar no botao colaborador para exibir o botão Gerente
    element_colaborado = driver.find_element_by_xpath("//button[@data-testid='btn_navigation_side_bar-employee-selected-desktop']").click()
    element_colaborado = driver.find_element_by_xpath("//button[@data-testid='btn_navigation_side_bar-manager-desktop']").click()
    time.sleep(2)

def obter_inconsistencias():
    return driver.find_elements_by_xpath("//tr[contains(@data-testid,'table-tr_management_inconsistency')]")

def to_datetime(str_date):
    return datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.%f")

def calcular_horas(str_entrada, str_saida):
    datetime_entrada = to_datetime(str_entrada)
    datetime_saida = to_datetime(str_saida)

    periodo_de_trabalho =  datetime.timedelta(hours=9, minutes=15)
    periodo_trabalhado = datetime_saida - datetime_entrada
    
    list_final_de_semana =  [5,6]
    eh_final_de_semana = True if list_final_de_semana.count(datetime_entrada.weekday()) else False

    horas_extras = datetime.timedelta(hours=0)
    possui_horas_extras = False
    
    horas_extras = periodo_trabalhado - periodo_de_trabalho
    
    if (eh_final_de_semana):
        horas_extras = periodo_trabalhado
        possui_horas_extras = True
    elif (periodo_trabalhado > periodo_de_trabalho):
        possui_horas_extras = True
    return  (datetime_entrada, datetime_saida, periodo_trabalhado, eh_final_de_semana, horas_extras, possui_horas_extras)

def obter_nome_colaborador(tr_inconsistencia):
    return tr_inconsistencia.find_element_by_xpath(".//div[starts-with(@data-testid, 'txt_management_inconsistency') and contains(@data-testid,'colaborator-name')]").text    

def obter_siblig(tr_inconsistencia):
    element_button_ajustes = tr_inconsistencia.find_element_by_xpath(".//button[@data-testid='btn_management_inconsistency-suggestion-adjust']").click()
    time.sleep(1)
    element_sibling =  tr_inconsistencia.find_element_by_xpath("following-sibling::tr")    
    return element_sibling

def obter_horarios(element_sibling):
    str_entrada = element_sibling.find_element_by_xpath(".//time[@data-testid='txt_timesheet_exp_receipt-in-out-0-type']").get_attribute("datetime")
    str_saida = element_sibling.find_element_by_xpath(".//time[@data-testid='txt_timesheet_exp_receipt-in-out-1-type']").get_attribute("datetime")
    return (str_entrada, str_saida)

def aprovar(element_sibling):
    element_sibling.find_element_by_xpath(".//button[@data-testid='btn_timesheet_exp_approve']").click()
    time.sleep(1)

login()
ir_para_inconsistencias()
element_inconsistencias = obter_inconsistencias()
dados = []
for inconsistencia in element_inconsistencias:

    element_sibling = obter_siblig(inconsistencia)
    str_entrada, str_saida = obter_horarios(element_sibling)
    datetime_entrada, datetime_saida, periodo_trabalhado, eh_final_de_semana, horas_extras, possui_horas_extras = calcular_horas(str_entrada,str_saida)
    
    colaborador = {}
    colaborador['nome'] = obter_nome_colaborador(inconsistencia)
    colaborador['entrada'] = datetime_entrada
    colaborador['saida'] = datetime_saida
    colaborador['final_de_semana'] = eh_final_de_semana
    colaborador['periodo_trabalhado'] = str(periodo_trabalhado)
    colaborador['possui_horas_extras'] = possui_horas_extras
    colaborador['horas_extras'] = str(horas_extras)
    dados.append(colaborador)

    if not possui_horas_extras: 
        aprovar(element_sibling)
    else:
        print (f"Entrada: {colaborador['entrada']} - Saída: {colaborador['saida']} Final de semana {colaborador['final_de_semana']} - Período Trabalhado: {colaborador['periodo_trabalhado']} - Horas Extras: {colaborador['horas_extras']} - Colaborador: {colaborador['nome']} ")
        print("Aprovar? s/n")
        acao = input()
        if acao.lower() == 's':
            print("Aprovando...")
            aprovar(element_sibling)
        else:
            print("Não aprovando...")

for item in dados:
    print(f"Entrada: {item['entrada']} - Saída: {item['saida']} Final de semana {item['final_de_semana']} - Período Trabalhado: {item['periodo_trabalhado']} - Horas Extras: {item['horas_extras']} - Colaborador: {item['nome']} ")
driver.quit()
