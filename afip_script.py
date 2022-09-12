#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import openpyxl
from openpyxl.styles import Font
import time

#Depurar errores de selenium en windows
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])

def extraer_cuil(i, sheet_obj,path):
  #del excel
  cell_obj = sheet_obj.cell(row = i+1, column = 2)
  return cell_obj.value

def extraer_password(i, sheet_obj, path):
  # del excel
  cell_obj = sheet_obj.cell(row = i+1, column = 3)
  return cell_obj.value

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

def mis_servicios():
  #despues del login la pagina quedara en web definida debajo y por default se encontrara en la pestaña Mi agenda
  web= 'https://portalcf.cloud.afip.gob.ar/portal/app/'
  browser.find_element(By.CLASS_NAME, 'web-only').click()  

def e_servicios():
  browser.find_element_by_title('srt_eservicios').click()
  #OJO!! abre una nueva pestaña no se si eso traera problemas con selenium
  if browser.find_element_by_class('label label-danger badge-mensajes').text != 0:
    browser.find_element_by_class('m-t-0').click()
    #IMPLEMENTAR guardado de los mensajes


if __name__ == '__main__':
  #extraccion de datos del excel
  path = r"C:\Users\Administrator\Desktop\AFIP\afip\AFIP.xlsx"
  wb_obj = openpyxl.load_workbook(path)  
  sheet_obj = wb_obj.active
  max_row = sheet_obj.max_row
  #extrae cada usuario del excel
  for i in range(1, max_row + 1):
    cuit = extraer_cuil(i, sheet_obj, path)
    clave_fiscal = extraer_password(i, sheet_obj, path)
    browser = webdriver.Chrome(options=options)
    login(browser, cuit, clave_fiscal)
    #Solo realizar si el login fue exitoso IMPLEMENTAR
    riesgo = siper(browser)
    #mis_servicios()