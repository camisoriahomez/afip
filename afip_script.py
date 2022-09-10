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

def extraer_datos():
  # del excel
  data = pd.read_excel (r'C:\Users\Administrator\Desktop\AFIP\afip\AFIP.xlsx')
  df = pd.DataFrame(data, columns= ['CUIL', 'Clave']) # es necesario que las palabras clave sean exactas
  return df

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

def mis_servicios():
  #despues del login la pagina quedara en web definida debajo y por default se encontrara en la pestaña Mi agenda
  web= 'https://portalcf.cloud.afip.gob.ar/portal/app/'
  browser.find_element_by_title('Mis Servicios').click()  

def e_servicios():
  browser.find_element_by_title('srt_eservicios').click()
  #OJO!! abre una nueva pestaña no se si eso traera problemas con selenium
  if browser.find_element_by_class('label label-danger badge-mensajes').text != 0:
    browser.find_element_by_class('m-t-0').click()
    #implementacion del guardado de los mensajes


if __name__ == '__main__':
  cuit = input('Ingrese el CUIT: ')
  clave_fiscal = input('Ingrese la clave fiscal: ')
  browser = webdriver.Chrome()
  login(browser, cuit, clave_fiscal)
  riesgo = siper(browser)
  mis_servicios()
