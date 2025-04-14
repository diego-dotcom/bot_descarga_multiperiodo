##########################################

# Autor: Diego Mendizábal

# Este software fue creado exclusivamente para fines educativos, el autor se desliga de toda
# responsabilidad relacionada con el uso del mismo.

# Software bajo licencia GPL-3, más información en https://www.gnu.org/licenses/gpl-3.0.html

##########################################

import pandas
import time
from selenium import webdriver
import random
from fechas import obtener_rangos_meses_completos
from selenium.webdriver.common.by import By
from tkinter import messagebox
from datetime import datetime

excel_claves = r'.\contribuyentes.xlsx'

df = pandas.read_excel(excel_claves, engine='openpyxl')


def descarga(excel_flag, csv_flag):

    if not excel_flag and not csv_flag:
        messagebox.showerror("Error", "Debe seleccionar al menos un formato para descargar (Excel y/o CSV)")
        return  # Sale de la función y no sigue ejecutando
    
    # Se recorre cada fila de la planilla de cálculo
    for i in df.index:

        # Obtengo los datos de la fila para ese contribuyente
        cuit = int(df['cuit'][i])
        clave = str(df['clave'][i])
        contribuyente = str(df['contribuyente'][i])

        # Convierto el formato de pandas en datetime y luego en str
        fecha_inicio = df['desde'][i].to_pydatetime()
        fecha_fin = df['hasta'][i].to_pydatetime()
        fecha_inicio = fecha_inicio.strftime('%d/%m/%Y')
        fecha_fin = fecha_fin.strftime('%d/%m/%Y')

        # Si la diferencia de meses entre fecha_inicio y fecha_fin es <= 12, uso el rango completo
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d/%m/%Y')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%d/%m/%Y')
        diferencia_meses = (fecha_fin_dt.year - fecha_inicio_dt.year) * 12 + (fecha_fin_dt.month - fecha_inicio_dt.month)

        if diferencia_meses <= 12:
            lista_periodos = [(fecha_inicio, fecha_fin)]  # Un solo período
        else:
            lista_periodos = obtener_rangos_meses_completos(fecha_inicio, fecha_fin)  # Como antes

        # Comienza el programa abriendo el login en la web de AFIP
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=option)
        driver.maximize_window()
        url = "https://auth.afip.gob.ar/contribuyente_/login.xhtml"
        driver.get(url)

        # Borra el campo CUIT e introduce el CUIT
        campo_cuit = driver.find_element(By.ID, "F1:username")
        campo_cuit.clear()
        campo_cuit.send_keys(cuit)

        boton_cuit = driver.find_element(By.ID, "F1:btnSiguiente")
        boton_cuit.click()

        # Borra el campo clave e introduce la clave

        campo_clave = driver.find_element(By.ID, "F1:password")
        campo_clave.clear()
        campo_clave.send_keys(clave)

        boton_clave = driver.find_element(By.ID, "F1:btnIngresar")
        boton_clave.click()

        driver.implicitly_wait(8)

        # Busca el servicio Mis Comprobantes y hace click

        buscador = driver.find_element(By.ID, 'buscadorInput')
        buscador.send_keys('Mis Comprobantes')
        mis_comprobantes = driver.find_element(By.CLASS_NAME, 'search-item')
        mis_comprobantes.click()

        time.sleep(2)

        driver.switch_to.window(driver.window_handles[1])

        # Hace click en el contribuyente que está en el excel, si no lo encuentra no hace nada

        try:
            driver.find_element(
                By.XPATH, f"//h2[contains(text(), '{contribuyente}')]").click()
        except:
            try:
                driver.find_element(
                    By.XPATH, f"//h3[contains(text(), '{contribuyente}')]").click()
            except:
                pass

        # Descarga los comprobantes recibidos

        driver.find_element(By.ID, "btnEmitidos").click()

        for periodo in lista_periodos:
            string_periodo = f"{periodo[0]} - {periodo[1]}"

            campo_fecha = driver.find_element(By.ID, "fechaEmision")
            campo_fecha.clear()
            campo_fecha.send_keys(string_periodo)
            driver.find_element(
                By.XPATH, f"//button[text()='Aplicar']").click()
            time.sleep(2)
            driver.find_element(By.ID, "buscarComprobantes").click()
            time.sleep(3)
            if excel_flag:
                driver.find_element(
                    By.XPATH, "//button[@class='btn btn-default buttons-excel buttons-html5 btn-defaut btn-sm sinborde']").click()
            if csv_flag:
                driver.find_element(
                    By.XPATH, "//button[@class='btn btn-default btn-defaut btn-sm sinborde']").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//a[@href='#tabConsulta']").click()

        driver.find_element(By.XPATH, "//a[@href='menuPrincipal.do']").click()

        # Descarga los comprobantes recibidos

        driver.find_element(By.ID, "btnRecibidos").click()

        for periodo in lista_periodos:
            string_periodo = f"{periodo[0]} - {periodo[1]}"

            campo_fecha = driver.find_element(By.ID, "fechaEmision")
            campo_fecha.clear()
            campo_fecha.send_keys(string_periodo)
            driver.find_element(
                By.XPATH, f"//button[text()='Aplicar']").click()
            time.sleep(2)
            driver.find_element(By.ID, "buscarComprobantes").click()
            time.sleep(3)
            if excel_flag:
                driver.find_element(
                    By.XPATH, "//button[@class='btn btn-default buttons-excel buttons-html5 btn-defaut btn-sm sinborde']").click()
            if csv_flag:
                driver.find_element(
                    By.XPATH, "//button[@class='btn btn-default btn-defaut btn-sm sinborde']").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//a[@href='#tabConsulta']").click()

        driver.find_element(By.XPATH, "//a[@href='menuPrincipal.do']").click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(random.randint(1, 3))

        # Sale de Mis Comprobantes
        driver.find_element(By.XPATH, "//a[@title='Salir...']").click()

        # Confirma el alert
        alert = driver.switch_to.alert
        alert.accept()

        driver.switch_to.window(driver.window_handles[0])

        # Se desloguea
        driver.find_element(By.ID, 'contenedorContribuyente').click()
        driver.find_element(By.XPATH, '//button[@title="Salir"]')

        driver.close()

    messagebox.showinfo("Información del bot", "Ejecución finalizada")
