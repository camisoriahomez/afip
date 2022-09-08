#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import requests
import re
from selenium import webdriver
from datetime import date
import openpyxl
from openpyxl.styles import Font
import time

#para extraer_datos de un excel
import pandas as pd

# depuracion de errores de Selenium con Chrome para Windows
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
# to supress the error messages/logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def extraer_datos():
  # del excel
  data = pd.read_excel (r'C:\Users\Administrator\Desktop\AFIP\AFIP.xlsx')
  df = pd.DataFrame(data, columns= ['CUIL', 'Clave']) # es necesario que las palabras clave sean exactas
  print (df)

def login(browser, cuit, clave_fiscal):
  try:
    browser.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')
    browser.find_element_by_id('F1:username').send_keys(cuit)
    browser.find_element_by_id('F1:btnSiguiente').click()
    browser.find_element_by_id('F1:password').send_keys(clave_fiscal)
    browser.find_element_by_id('F1:btnIngresar').click()
    print('Login exitoso.\n')
  except:
    print('Error en login.\n')

def siper(browser):
  try:
    return browser.find_elements_by_tag_name("p")[2].text
  except:
    print('No se encontro elemento siper.\n')

if __name__ == '__main__':
  cuit = input('Ingrese el CUIT: ')
  clave_fiscal = input('Ingrese la clave fiscal: ')
  browser = webdriver.Chrome(options=options)
  login(browser, cuit, clave_fiscal)
  riesgo = siper(browser)