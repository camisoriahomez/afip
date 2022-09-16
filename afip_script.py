#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import openpyxl
from openpyxl.styles import Font
import time

#Depurar errores de selenium en windows
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])

def extraer_cuil(i, sheet_obj,path):
  #del excel
  cell_obj = sheet_obj.cell(row = i, column = 2)
  return cell_obj.value

def extraer_clave(i, sheet_obj, path):
  # del excel
  cell_obj = sheet_obj.cell(row = i, column = 3)
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

def deuda(browser, cuit, clave_fiscal):
  try:
    browser.get('https://ctacte.cloud.afip.gob.ar/contribuyente/externo')
    re_login(browser, clave_fiscal)
    time.sleep(5)
    return browser.find_element(By.CLASS_NAME, 'value').text
  except:
    print("No se encontro elemento deuda.\n")

def e_servicios(browser):
  try:
    browser.get('https://eservicios.srt.gob.ar/home/Default.aspx')
    re_login(browser, clave_fiscal)
    return browser.find_element(By.CSS_SELECTOR, 'span.label.label-danger.badge-mensajes').text
  except:
    print("No se encontraron notificaciones juridicas. \n")

def e_servicios_personal(browser):
  try:
    browser.get('https://eservicios.srt.gob.ar/home/Default.aspx')
    re_login(browser, clave_fiscal)
    return browser.find_element(By.XPATH, '//*[@id="formPrincipal"]/div[3]/section/div/aside/nav/ul/div[2]/div[1]/a[2]/span').text
  except:
    print("No se encontraron notificaciones personales. \n")    

if __name__ == '__main__':
  #extraccion de datos del excel
  path = r"C:\Users\Administrator\Desktop\AFIP\afip\AFIP.xlsx"
  wb_obj = openpyxl.load_workbook(path)  
  sheet_obj = wb_obj.active
  max_row = sheet_obj.max_row
  #extrae cada usuario del excel
  for i in range(2, max_row - 1):
    cuit = extraer_cuil(i, sheet_obj, path)
    clave_fiscal = extraer_clave(i, sheet_obj, path)
    browser = webdriver.Chrome(options=options)
    login(browser, cuit, clave_fiscal)
    #A partir de aca solo realizar si el login fue exitoso IMPLEMENTAR!!
    riesgo = siper(browser)
    #Escribir siper en excel
    c1 = sheet_obj.cell(row = i, column = 4)
    c1.value = riesgo
    wb_obj.save(path)
    # deuda
    deuda_var = deuda(browser, cuit, clave_fiscal)
    c2 = sheet_obj.cell(row = i, column = 5)
    c2.value = deuda_var
    wb_obj.save(path)
    # e-Servicios SRT
    notificaciones_personales = e_servicios_personal(browser)
    c3 = sheet_obj.cell(row = i, column = 6)
    c3.value = notificaciones_personales
    notificaciones_juridicas = e_servicios(browser)
    c4 = sheet_obj.cell(row = i, column = 7)
    c4.value = notificaciones_juridicas
    wb_obj.save(path)