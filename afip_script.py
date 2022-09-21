#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import date
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import time

# def extraer_datos():
# del excel

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

def siper(browser):
  try:
    return browser.find_elements(By.TAG_NAME, "p")[2].text
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
    browser.find_element(By.ID, 'F1:btnSiguiente').click()
    browser.find_element(By.ID, 'F1:password').send_keys(clave_fiscal)
    browser.find_element(By.ID, 'F1:btnIngresar').click()
    print('Login exitoso.\n')
    # desplegable 
    cuits = Select(browser.find_element(By.NAME,'$PropertySelection'))
    total = {}
    for i, cuit in enumerate(cuits.options):
      cant_imp, saldo = 0, 0
      num_cuit = cuit.text
      print(f'Leyendo info de CUIT: {num_cuit}')
      total[num_cuit] = []
      time.sleep(3)
      cuits.select_by_index(i)
      time.sleep(3)
      conceptos = browser.find_elements(By.CSS_SELECTOR, 'tr[class="group"]')
      print(f'Conceptos encontrados: {len(conceptos)}')
      for concepto in conceptos:
        elemento_cant_imp = concepto.find_element(By.CSS_SELECTOR, 'span[class="cant-impuesto"]').text
        cant_imp += int(elemento_cant_imp[1:-1])
        print('Cantidad de impuestos encontrados')
        elemento_saldo = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_saldo"]').text
        saldo += str_a_saldo(elemento_saldo)
        print('Elem saldo encontrado')
        elemento_int_r = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_int_res"]').text
        saldo += str_a_saldo(elemento_int_r)
        print('Elem saldo encontrado')
        elemento_int_p = concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_int_pun"]').text
        saldo += str_a_saldo(elemento_int_p)
        print('Elem saldo encontrado')
      total.update({num_cuit: [cant_imp, saldo]})
    return total
  except:
    print('No se encontro elemento deuda.\n')

if __name__ == '__main__':
  cuit = input('Ingrese el CUIT: ')
  clave_fiscal = input('Ingrese la clave fiscal: ')
  browser = webdriver.Chrome()
  login(browser, cuit, clave_fiscal)
  #print(siper(browser))
  print(deuda(browser, cuit, clave_fiscal))
