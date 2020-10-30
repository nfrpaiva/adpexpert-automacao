from model import Inconsistencia
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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

def abrir_pagina():
    driver.maximize_window()
    driver.get('http://www.adpexpert.com.br')
    time.sleep(1)
    return driver


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
    element_colaborado = driver.find_element_by_xpath(
        "//button[@data-testid='btn_navigation_side_bar-employee-selected-desktop']").click()
    element_colaborado = driver.find_element_by_xpath(
        "//button[@data-testid='btn_navigation_side_bar-manager-desktop']").click()
    time.sleep(2)


def obter_inconsistencias():
    return driver.find_elements_by_xpath("//tr[contains(@data-testid,'table-tr_management_inconsistency')]")


def to_datetime(str_date):
    return datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.%f")


def calcular_horas(str_horarios):
    horarios = []
    periodo_de_trabalho = datetime.timedelta(hours=9, minutes=15)
    periodo_trabalhado = datetime.timedelta(hours=0)
    periodo_tolerancia = datetime.timedelta(hours=0, minutes=10)

    for str_inicio, str_fim in str_horarios:
        dt_inicio = to_datetime(str_inicio)
        dt_fim = to_datetime(str_fim)
        horarios.append((dt_inicio, dt_fim))
        periodo_trabalhado += dt_fim - dt_inicio

    datetime_entrada = horarios[0][0]

    list_final_de_semana = [5, 6]
    eh_final_de_semana = True if list_final_de_semana.count(
        datetime_entrada.weekday()) else False

    horas_extras = datetime.timedelta(hours=0)
    possui_horas_extras = False

    horas_extras = periodo_trabalhado - periodo_de_trabalho

    if (eh_final_de_semana):
        horas_extras = periodo_trabalhado
        possui_horas_extras = True
    elif (periodo_trabalhado > (periodo_de_trabalho + periodo_tolerancia)):
        possui_horas_extras = True
    return (horarios, periodo_trabalhado, eh_final_de_semana, horas_extras, possui_horas_extras)


def obter_nome_colaborador(tr_inconsistencia):
    return tr_inconsistencia.find_element_by_xpath(".//div[starts-with(@data-testid, 'txt_management_inconsistency') and contains(@data-testid,'colaborator-name')]").text


def obter_element_suggestion(tr_inconsistencia):
    element_button_ajustes = tr_inconsistencia.find_element_by_xpath(
        ".//button[@data-testid='btn_management_inconsistency-suggestion-adjust']").click()
    time.sleep(1)
    element_suggestion = tr_inconsistencia.find_element_by_xpath(
        "following-sibling::tr")
    return element_suggestion


def obter_horarios(element_suggestion):

    els = element_suggestion.find_elements_by_xpath(".//time[ contains(@data-testid,'type')]")

    gen_entradas = ( e.get_attribute("datetime") for i,e in  enumerate(els) if i % 2 == 0)
    gen_saidas = ( e.get_attribute("datetime") for i,e in  enumerate(els) if i % 2 != 0)


    str_entradas = tuple(gen_entradas)
    str_saidas = tuple(gen_saidas)

    return tuple(zip(str_entradas, str_saidas))


def aprovar(element_suggestion):
    element_suggestion.find_element_by_xpath(
        ".//button[@data-testid='btn_timesheet_exp_approve']").click()
    time.sleep(1)

def processa_inconsistencias(element_inconsistencias):
    dados = []
    for inconsistencia in element_inconsistencias:
        nome = obter_nome_colaborador(inconsistencia)
        try:
            element_suggestion = obter_element_suggestion(inconsistencia)
        except NoSuchElementException as e:
            print(f"Existe um apontamento inconsistente para {nome}, entretando não há sugestão de ajuste para ser aprovada.")
            continue
        str_horarios = obter_horarios(element_suggestion)
        horarios, periodo_trabalhado, eh_final_de_semana, horas_extras, possui_horas_extras = calcular_horas(str_horarios)

        inconsistencia = Inconsistencia(
            nome,
            horarios,
            eh_final_de_semana,
            str(periodo_trabalhado),
            possui_horas_extras,
            str(horas_extras),
            element_suggestion)

        dados.append(inconsistencia)
    return dados

def aprovar_inconsistencias(inconsistencias):
    for inconsistencia in sorted(inconsistencias, key=lambda i: i.possui_horas_extras):
        if not inconsistencia.possui_horas_extras:
            print(f"Aprovando automaticamente - {inconsistencia.nome} - {inconsistencia.str_horarios()} - Extra {inconsistencia.horas_extras} ")
            aprovar(inconsistencia.element_suggestion)
        else:
            print(f"{'Aprovação manual'.ljust(25, ' ')} - {inconsistencia.nome} - {inconsistencia.str_horarios()} - Extra {inconsistencia.horas_extras} - Aprova? s/n")
            acao = input()
            if acao.lower() == 's':
                print("Aprovando...")
                aprovar(inconsistencia.element_suggestion)
            else:
                print("Não aprovando...")


def executar():
    try:
        abrir_pagina()
        login()
        ir_para_inconsistencias()
        element_inconsistencias = obter_inconsistencias()
        inconsistencias =  processa_inconsistencias(element_inconsistencias)
        aprovar_inconsistencias(inconsistencias)
    except Exception as e:
        print(f"Ocorreu um erro ({type(e)}): ", e)
    else:
        print("Finalizado sem nenhum erro")
    finally:
        driver.quit()


if __name__ == "__main__":
    executar()
