import datetime
import locale
import logging
import os
import random
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import schedule

#QUANTIDADE DE PONTOS 2 OU 4
__QTD_PONTOS__   = 4

#HORARIO ENTRADA/SAIDA 1
__HH_ENTRADA_1__ = 8
__HH_SAIDA_1__   = 12

#HORARIO ENTRADA/SAIDA 2
__HH_ENTRADA_2__ = 13
__HH_SAIDA_2__   = 18

#VARIAÇÃO MÁXIMA DE MINUTOS PARA ENTRADA E SAIDA
__VAR_MM__       = 15

__HORARIO__ = '00:00'
__FIRST_TIME__ = True
__N_DAILY_REG__ = 0
__DIAS_DA_SEMANA__ = [0, 1, 2, 3, 4]


__LOGGER__ = logging.getLogger(__name__)
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


def arma_rotina() -> None:

    global __FIRST_TIME__

    if not __FIRST_TIME__:

        schedule.clear()

    if check_weekday():

        check_horario()
    
        schedule.every().day.at(__HORARIO__).do(make_it)


'''
    PARA VERIFICAR SE É FERIADO:

    FAZER UMA VARIAVEL LER UM VETOR DE DATAS DE UM ARQUIVO.TXT
    PRIMEIRO IF DEVE COMPARAR O DIA ATUAL COM A VARIÁVEL PARA TESTAR SE É FERIADO
    CASO FERIADO, MESMO LOOP DO FINAL DE SEMANA ATÉ MUDAR O DIA
    MANTER AS OUTRAS CONDIÇÕES COMO ELIF
'''
def check_weekday() -> None:

    global __DIAS_DA_SEMANA__
    global __N_DAILY_REG__
    
    agora = datetime.datetime.now()

    if agora.weekday() in __DIAS_DA_SEMANA__ and __N_DAILY_REG__ < 4:

        return True
    
    elif agora.weekday() + 1 in __DIAS_DA_SEMANA__ and agora.weekday() != 6:

        return True

    else:

        while agora.weekday() != 0:

            time.sleep(3600)
            agora = datetime.datetime.now()
        
        return True


def write_log() -> None:

    global __LOGGER__

    agora = datetime.datetime.now()
    logging.basicConfig(filename='.logs_main', level=logging.INFO)
    __LOGGER__.info(f'{agora.strftime('%d/%m/%Y %H:%M:%S')}: {__HORARIO__}')


def registro_tela(driver) -> None:

    global __N_DAILY_REG__

    #criar string da data atual
    aux = datetime.datetime.now()
    data = (('0' + str(aux.day) + '_') if aux.day < 10 else (str(aux.day) + '_'))
    data = data + (('0' + str(aux.month) + '_') if aux.month < 10 else (str(aux.month) + '_'))
    data = data + str(aux.year)

    #cria string hora atual
    hora = (('0' + str(aux.hour)) if aux.hour < 10 else (str(aux.hour)) + '_')
    hora = hora + (('0' + str(aux.minute)) if aux.minute < 10 else (str(aux.minute)) + '_')
    hora = hora + (('0' + str(aux.second)) if aux.second < 10 else (str(aux.second)))
    #hora = hora + str(aux.second)

    main_dir = os.getcwd()
    dir_reg = '.registros'
    dir_reg_daily  = dir_reg + '_' + data
    #NUMERO REPRESENTANDO O PONTO DO DIA _ DATA _ HORA
    name_reg = str(__N_DAILY_REG__) + '_' + data + '_' + hora

    #cria o dir registros, onde ficam todas as pastas com os registros
    os.makedirs(dir_reg, exist_ok=True)
    os.chdir(dir_reg)

    #cria o dir onde será salvo os registros diários
    os.makedirs(dir_reg_daily, exist_ok=True)
    os.chdir(dir_reg_daily)
    
    #printa e salva com nome data_hora
    #pag.screenshot(name_reg)
    driver.save_screenshot(name_reg+".png")

    #voltar para o diretório principal main_dir
    os.chdir(main_dir)


def check_horario() -> None:

    global __HORARIO__
    global __N_DAILY_REG__
    
    #hora no formato string hh:mm
    agora = datetime.datetime.now()
    hora_agora = (('0' + str(agora.hour)) if agora.hour < 10 else (str(agora.hour)) + ':')
    hora_agora = hora_agora + (('0' + str(agora.minute)) if agora.minute < 10 else (str(agora.minute)))

    #apresenta a hora no formato string hh:mm
    #print(hora_agora)

    if __QTD_PONTOS__ == 4:

        #VERIFICAR COMO AUTOMIATIZAR A ESCOLHA DE HORÁRIOS CORTE
        if ((hora_agora <= '07:30' or hora_agora >= '17:45') and __N_DAILY_REG__ != 1):
            
            __N_DAILY_REG__ = 1
            hora_entra = datetime.time(hour=__HH_ENTRADA_1__, minute=0)
            hora_entra = datetime.datetime.combine(datetime.date.today(), hora_entra)
            var_horario = random.randint(0, __VAR_MM__)
            escolhe = random.randint(0, 1)

            if escolhe == 0:

                hora_entra = hora_entra - datetime.timedelta(minutes=var_horario)
                aux = ((('0' + str(hora_entra.hour)) if hora_entra.hour <10 else (str(hora_entra.hour))) + ':')
                aux = aux + (('0' + str(hora_entra.minute)) if hora_entra.minute < 10 else(str(hora_entra.minute)))
                __HORARIO__ = aux
                write_log()

            else:
                
                hora_entra = hora_entra + datetime.timedelta(minutes=var_horario)
                aux = ((('0' + str(hora_entra.hour)) if hora_entra.hour <10 else (str(hora_entra.hour))) + ':')
                aux = aux + (('0' + str(hora_entra.minute)) if hora_entra.minute < 10 else(str(hora_entra.minute)))
                __HORARIO__ = aux
                write_log()
        
        #VERIFICAR TAMBÉM COMO AUTOMATIZAR ESTE CORTE DE HORÁRIO
        elif hora_agora < '11:45' and __N_DAILY_REG__ != 2:

            __N_DAILY_REG__ = 2
            hora_sai = datetime.time(hour=__HH_SAIDA_1__, minute=0)
            hora_sai = datetime.datetime.combine(datetime.date.today(), hora_sai)
            var_horario = random.randint(0, __VAR_MM__)
            escolhe = random.randint(0, 1)

            if escolhe == 0:

                hora_sai = hora_sai - datetime.timedelta(minutes=var_horario)
                aux = ((('0' + str(hora_sai.hour)) if hora_sai.hour <10 else (str(hora_sai.hour))) + ':')
                aux = aux + (('0' + str(hora_sai.minute)) if hora_sai.minute < 10 else(str(hora_sai.minute)))
                __HORARIO__ = aux
                write_log()

            else:
                
                hora_sai = hora_sai + datetime.timedelta(minutes=var_horario)
                aux = ((('0' + str(hora_sai.hour)) if hora_sai.hour <10 else (str(hora_sai.hour))) + ':')
                aux = aux + (('0' + str(hora_sai.minute)) if hora_sai.minute < 10 else(str(hora_sai.minute)))
                __HORARIO__ = aux
                write_log()
        
        elif hora_agora < '12:45' and __N_DAILY_REG__ != 3:
            
            __N_DAILY_REG__ = 3
            hora_entra = datetime.time(hour=__HH_ENTRADA_2__, minute=0)
            hora_entra = datetime.datetime.combine(datetime.date.today(), hora_entra)
            var_horario = random.randint(0, __VAR_MM__)
            escolhe = random.randint(0, 1)

            if escolhe == 0:

                hora_entra = hora_entra - datetime.timedelta(minutes=var_horario)
                aux = ((('0' + str(hora_entra.hour)) if hora_entra.hour <10 else (str(hora_entra.hour))) + ':')
                aux = aux + (('0' + str(hora_entra.minute)) if hora_entra.minute < 10 else(str(hora_entra.minute)))
                __HORARIO__ = aux
                write_log()

            else:
                
                hora_entra = hora_entra + datetime.timedelta(minutes=var_horario)
                aux = ((('0' + str(hora_entra.hour)) if hora_entra.hour <10 else (str(hora_entra.hour))) + ':')
                aux = aux + (('0' + str(hora_entra.minute)) if hora_entra.minute < 10 else(str(hora_entra.minute)))
                __HORARIO__ = aux
                write_log()
        
        elif hora_agora < '17:45' and __N_DAILY_REG__ != 4:
            
            __N_DAILY_REG__ = 4
            hora_entra = datetime.time(hour=__HH_SAIDA_2__, minute=0)
            hora_entra = datetime.datetime.combine(datetime.date.today(), hora_entra)
            var_horario = random.randint(0, __VAR_MM__)
            escolhe = random.randint(0, 1)

            if escolhe == 0:

                hora_entra = hora_entra - datetime.timedelta(minutes=var_horario)
                aux = ((('0' + str(hora_entra.hour)) if hora_entra.hour <10 else (str(hora_entra.hour))) + ':')
                aux = aux + (('0' + str(hora_entra.minute)) if hora_entra.minute < 10 else(str(hora_entra.minute)))
                __HORARIO__ = aux
                write_log()

            else:
                
                hora_entra = hora_entra + datetime.timedelta(minutes=var_horario)
                aux = ((('0' + str(hora_entra.hour)) if hora_entra.hour <10 else (str(hora_entra.hour))) + ':')
                aux = aux + (('0' + str(hora_entra.minute)) if hora_entra.minute < 10 else(str(hora_entra.minute)))
                __HORARIO__ = aux
                write_log()


def make_it() -> None:

    login = ''
    password = ''

    #login = 'pmb14854'
    #password = '14854'
    
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Firefox(options)

    driver.get('http://sistemas08.sisponto.com.br:4000/Sispontoweb/open.do?sys=SPW')

    driver.implicitly_wait(0.5)

    time.sleep(10)      

    iframe = driver.find_element(By.NAME, 'mainform')
    driver.switch_to.frame(iframe)

    usuario   = driver.find_element(By.XPATH, '/html/body/form/div/div[4]/div[11]/input')
    senha     = driver.find_element(By.XPATH, '/html/body/form/div/div[4]/div[3]/input')
    btn_login = driver.find_element(By.XPATH, '/html/body/form/div/div[4]/div[2]/button')

    usuario.send_keys(login)
    senha.send_keys(password)
    btn_login.click()

    driver.implicitly_wait(0.5)

    time.sleep(6)

    driver.switch_to.default_content()
    iframe = driver.find_element(By.NAME, 'mainsystem')
    driver.switch_to.frame(iframe)

    iframe2 = driver.find_element(By.NAME, 'mainform')
    driver.switch_to.frame(iframe2)

    time.sleep(6)

    img = driver.find_element(By.XPATH, '/html/body/form/div/div[4]/div[12]/img')
    menu = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/ul/li[1]/a/span')
    inclusao = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/ul/li[1]/ul/li[1]/a/span')
    registro = driver.find_element(By.ID, '678483')

    ActionChains(driver) \
        .move_to_element(img) \
        .perform()

    time.sleep(1)

    ActionChains(driver) \
        .move_to_element(menu) \
        .perform()

    time.sleep(1)

    ActionChains(driver) \
        .move_to_element(inclusao) \
        .perform()

    time.sleep(1)

    registro.click()

    time.sleep(3)

    driver.switch_to.window(driver.window_handles[1])

    driver.switch_to.default_content()
    iframe_ponto = driver.find_element(By.NAME, 'mainform')
    driver.switch_to.frame(iframe_ponto)

    btn_registro = driver.find_element(By.XPATH, '/html/body/form/div/div[2]/div[2]/div[10]/button')
    btn_registro.click()

    time.sleep(5)

    #registro_tela(driver)

    time.sleep(3)

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

    driver.switch_to.default_content()
    iframe = driver.find_element(By.NAME, 'mainsystem')
    driver.switch_to.frame(iframe)
    iframe2 = driver.find_element(By.NAME, 'mainform')
    driver.switch_to.frame(iframe2)

    btn_close = driver.find_element(By.XPATH, '/html/body/div[5]/img')
    btn_close.click()

    time.sleep(2)

    driver.quit()

    arma_rotina()


def main() -> None:

    global __FIRST_TIME__

    if __FIRST_TIME__:

        __FIRST_TIME__ = False        
        arma_rotina()

    while True:

        schedule.run_pending()
        time.sleep(1)

main()
#make_it()
