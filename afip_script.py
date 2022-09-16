#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import date
import openpyxl
from openpyxl.styles import Font
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

def deuda(browser, cuit, clave_fiscal):
  try:
    # login de nuevo
    browser.get('https://ctacte.cloud.afip.gob.ar/contribuyente/externo')
    browser.find_element(By.ID, 'F1:btnSiguiente').click()
    browser.find_element(By.ID, 'F1:password').send_keys(clave_fiscal)
    browser.find_element(By.ID, 'F1:btnIngresar').click()
    # desplegable 
    cuits = Select(browser.find_element(By.NAME,'$PropertySelection'))
    total = {}
    for i, cuit in enumerate(cuits.options):
      info = {}
      info['Concepto'] = []
      info['Cant Impuesto'] = []
      info['Saldo'] = []
      info['Intereses'] = []
      print(i)
      cuits.select_by_index(i)
      #time.wait(3)
      conceptos = browser.find_elements(By.CSS_SELECTOR, 'tr[class="group"]')
      for concepto in conceptos:
        detalle = concepto.find_element(By.CSS_SELECTOR, 'div[class="value"]')
        print(detalle.text)
        info['Concepto'].append(detalle.text)
        print(concepto.find_element(By.CSS_SELECTOR, 'span[class="cant-impuesto"]').text)
        print(concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_saldo"]').text)
        #info['Cant Impuesto'].append(concepto.find_element(By.CSS_SELECTOR, 'span[class="cant-impuesto"]').text)
        #info['Saldo'].append(concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_saldo"]').text)
        #info['Intereses'].append(concepto.find_element(By.CSS_SELECTOR, 'td[class="subtotales sb_int_res"]').text)
      #total[cuit.text] = info 
    return total
  except:
    print('No se encontro elemento deuda.\n')

if __name__ == '__main__':
  cuit = input('Ingrese el CUIT: ')
  clave_fiscal = input('Ingrese la clave fiscal: ')
  browser = webdriver.Chrome()
  login(browser, cuit, clave_fiscal)
  #riesgo = siper(browser)
  deuda(browser, cuit, clave_fiscal)
