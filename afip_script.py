#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager
import gspread
import time

#Depurar errores de selenium en windows
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])

def extraer_datos(i, worksheet):
  cell_cuil = worksheet.cell(i, 2)
  cell_clave = worksheet.cell(i, 3)
  return cell_cuil.value, cell_clave.value

def login(browser, cuit, clave_fiscal):
  try:
    browser.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')
    browser.find_element(By.ID, 'F1:username').send_keys(cuit)
    browser.find_element(By.ID, 'F1:btnSiguiente').click()
    browser.find_element(By.ID, 'F1:password').send_keys(clave_fiscal)
    browser.find_element(By.ID, 'F1:btnIngresar').click()
    print('Login exitoso.\n')
  except:
    print('Error en login.\n')

def re_login(browser, clave_fiscal):
  wait = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'F1:btnSiguiente')))
  browser.find_element(By.ID, 'F1:btnSiguiente').click()
  browser.find_element(By.ID, 'F1:password').send_keys(clave_fiscal)
  browser.find_element(By.ID, 'F1:btnIngresar').click()    

def siper(browser):
  try:
    wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.small.light')))
    return browser.find_elements(By.CSS_SELECTOR, 'p.small.light')[2].text
  except:
    print('No se encontro elemento siper.\n')

def str_a_saldo(string):
  new_string = ''
  for s in string[2:]:
    if s.isnumeric(): new_string += s
    if s == ',': new_string += '.'
  return float(new_string)

def deuda(browser, cuit, clave_fiscal):
  try:
    # login de nuevo
    browser.get('https://ctacte.cloud.afip.gob.ar/contribuyente/externo')
    re_login(browser, clave_fiscal)
    # desplegable
    try:
      cuits = Select(browser.find_element(By.NAME,'$PropertySelection'))    
      total = {}
      for i, cuit in enumerate(cuits.options):
        cant_imp, saldo = 0, 0
        num_cuit = cuit.text
        print(f'Leyendo info de CUIT: {num_cuit} \n')
        total[num_cuit] = []
        time.sleep(5)
        cuits.select_by_index(i)
        time.sleep(5)
        conceptos = browser.find_elements(By.CSS_SELECTOR, 'tr[class="group"]')
        print(f'Conceptos encontrados: {len(conceptos)} \n')
        for concepto in conceptos:
          elemento_cant_imp = concepto.find_element(By.CSS_SELECTOR, 'span[class="cant-impuesto"]').text
          cant_imp += int(elemento_cant_imp[1:-1])
          elemento_saldo = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_saldo"]').text
          saldo += str_a_saldo(elemento_saldo)
          elemento_int_r = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_int_res"]').text
          saldo += str_a_saldo(elemento_int_r)
          elemento_int_p = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_int_pun"]').text
          saldo += str_a_saldo(elemento_int_p)
        print(f'Cantidad de deuda total: {saldo}')   
        print(f'Cantidad de obligaciones encontradas: {cant_imp} \n')
        total.update({num_cuit: [cant_imp, saldo]})
    except:
      print('Sin persona juridica a tratar. \n')
      cuit = browser.find_element(By.CLASS_NAME, 'cuit')
      total = {}
      cant_imp, saldo = 0, 0
      num_cuit = cuit.text
      print(f'Leyendo info de CUIT: {num_cuit} \n')
      total[num_cuit] = []
      time.sleep(5)
      time.sleep(5)
      conceptos = browser.find_elements(By.CSS_SELECTOR, 'tr[class="group"]')
      print(f'Conceptos encontrados: {len(conceptos)}')
      for concepto in conceptos:
        elemento_cant_imp = concepto.find_element(By.CSS_SELECTOR, 'span[class="cant-impuesto"]').text
        cant_imp += int(elemento_cant_imp[1:-1])
        elemento_saldo = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_saldo"]').text
        saldo += str_a_saldo(elemento_saldo)
        elemento_int_r = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_int_res"]').text
        saldo += str_a_saldo(elemento_int_r)
        elemento_int_p = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_int_pun"]').text
        saldo += str_a_saldo(elemento_int_p)
      print(f'Cantidad de deuda total: {saldo} \n')   
      print(f'Cantidad de obligaciones encontradas: {cant_imp} \n')
      total.update({num_cuit: [cant_imp, saldo]})
    return total
  except:
    print('No se encontro elemento deuda.\n')    

def e_servicios(browser, clave_fiscal):
  try:
    browser.get('https://eservicios.srt.gob.ar/home/Default.aspx')
    re_login(browser, clave_fiscal)
    personal = browser.find_element(By.CSS_SELECTOR, 'span.badge.badge-light.text-right.cuit-tooltip').text
    juridico = browser.find_element(By.CSS_SELECTOR, 'span.label.label-danger.badge-mensajes').text
    return personal, juridico
  except:
    print("Error en e-servicios \n")
    return None, None

def flattenlist(l):
  flat_list = []
  for sublist in l:
    for item in sublist:
        flat_list.append(item)
  return flat_list

def retenciones(browser):
  try:
    #Ir a Mis retenciones
    browser.find_element(By.XPATH, '//*[@id="root"]/div/main/section[1]/div/ul/li[3]/a/span').click()
    time.sleep(3)
    browser.find_element(By.XPATH, '//*[@title="mis_retenciones"]').click()
    time.sleep(3)
    browser.switch_to.window(browser.window_handles[1])
    cuits = Select(browser.find_element(By.NAME,'cuitRetenido'))
    cuits.select_by_index(1)
    time.sleep(3)
    keys= ['217', '939', '787']
    SICORE, GCIAS, PAIS = 0, 0, 0 
    for key in keys:
      try:
        browser.find_element(By.NAME, 'impuesto').clear()
        browser.find_element(By.NAME, 'impuesto').send_keys(key)
        browser.find_element(By.CLASS_NAME, 'inputbutton').click()
        try:
          browser.switch_to.alert.accept()
        except:
          pass  
        time.sleep(3)
        valor = browser.find_element(By.XPATH, '//*[@id="totalgeneral"]/tbody/tr[2]/td[2]').text
        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')
        if key == '217':
          SICORE = valor
        elif key == '787':
          GCIAS = valor
        elif key == '939':
          PAIS = valor
        browser.back()
      except:
        pass  
    browser.close()    
    browser.switch_to.window(browser.window_handles[0])    
    return SICORE, GCIAS, PAIS
  except:
    print("Error en retenciones. \n")
    return None, None, None       
        
def afip_juridicos(gc):
  #Abre el excel de AFIP
  sh = gc.open_by_key('1swJFxi9ZOKf1p7F_Ni8ShFvZovcRZJEN6pc-U40qFRM')
  worksheet = sh.get_worksheet(0)
  max_row = len(worksheet.get_all_values()) +1
  #extrae cada usuario del excel
  for i in range(2, max_row):
    print(f"Trabajando con: {worksheet.cell(i, 1).value}") 
    cuit, clave_fiscal = extraer_datos(i, worksheet)
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    login(browser, cuit, clave_fiscal)
    #A partir de aca solo realizar si el login fue exitoso
    riesgo = str(siper(browser))
    worksheet.update_cell(i, 4, riesgo)
    # deuda
    deuda_dic = deuda(browser, cuit, clave_fiscal)
    if type(deuda_dic) == dict:
      deuda_list = list(deuda_dic.values())
      deuda_list = flattenlist(deuda_list)
      for j in range(len(deuda_list)):
        worksheet.update_cell(i, 7+j, deuda_list[j])
    else: 
      print("Error al encontrar elemento deuda. \n")    
    # e-Servicios SRT
    notificaciones_personales, notificaciones_juridicas = e_servicios(browser, clave_fiscal)
    worksheet.update_cell(i, 5, notificaciones_personales)
    worksheet.update_cell(i, 6, notificaciones_juridicas)   

def afip_monotributo(gc):
  sh = gc.open_by_key('1swJFxi9ZOKf1p7F_Ni8ShFvZovcRZJEN6pc-U40qFRM')
  worksheet = sh.get_worksheet(1)
  max_row = len(worksheet.get_all_values()) +1
  #extrae cada usuario del excel
  for i in range(2, max_row):
    print(f"Trabajando con: {worksheet.cell(i, 1).value}")
    cuit, clave_fiscal = extraer_datos(i, worksheet)
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    login(browser, cuit, clave_fiscal)
    riesgo = str(siper(browser))
    worksheet.update_cell(i, 4, riesgo)
    #retenciones
    sicore, gcias, pais =retenciones(browser)
    worksheet.update_cell(i, 7, sicore)
    worksheet.update_cell(i, 8, gcias)
    worksheet.update_cell(i, 9, pais)
    # deuda
    deuda_dic = deuda(browser, cuit, clave_fiscal)
    if type(deuda_dic) == dict:
      deuda_list = list(deuda_dic.values())
      deuda_list = flattenlist(deuda_list)
      for j in range(len(deuda_list)):
        worksheet.update_cell(i, 5+j, deuda_list[j])
    else: 
      print("Error al encontrar elemento deuda. \n")  

def rentas(gc):
  try:
    sh = gc.open_by_key('175_tJhY6wlb8yIYjg6Ihc3Fxz6aYtT1ysv6PUU-oFxw')
    worksheet = sh.get_worksheet(0)
    max_row = len(worksheet.get_all_values()) +1
    for i in range(2, max_row):
      print(f"Trabajando con: {worksheet.cell(i, 1).value}") 
      cuit, clave = extraer_datos(i, worksheet)
      browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
      #login a rentas
      try:
        browser.get('https://www.dgrsalta.gov.ar/rentassalta/login.jsp')
        browser.find_element(By.XPATH, '//*[@id="usuario"]').send_keys(cuit)
        browser.find_element(By.XPATH,'//*[@id="password"]').send_keys(clave)
        browser.find_element(By.XPATH, '//*[@id="enviaLogin"]/span').click()
        browser.get('https://www.dgrsalta.gov.ar/rentassalta/menuRiesgoFiscal.do')
        time.sleep(5)
        browser.find_element(By.XPATH, '//*[@id="fancybox-close"]').click()
        time.sleep(3)
        browser.find_element(By.XPATH, '//*[@id="Riesgo_Fiscal"]').click()
        time.sleep(3)
        browser.switch_to.alert.accept()
        time.sleep(5)
        riesgo_fiscal = browser.find_element(By.XPATH, '//*[@id="contenido"]/div/table/tbody/tr[2]/td').text
        print(riesgo_fiscal)
        riesgo_fiscal = riesgo_fiscal.replace('Su nivel de Riesgo Fiscal actualmente es : ', '')
        worksheet.update_cell(i, 4, riesgo_fiscal)
      except:
        print("Error de contraseña")  
    browser.close()  
  except:
    print("Error de rentas. \n")

if __name__ == '__main__':
  gc = gspread.service_account()
  afip_juridicos(gc)
  afip_monotributo(gc)
  rentas(gc)