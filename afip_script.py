#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import requests
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date
import openpyxl
from openpyxl.styles import Font
import time

# def extraer_datos():
# del excel

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

def deuda(browser, cuit, clave_fiscal):
  try:
    browser.get('https://ctacte.cloud.afip.gob.ar/contribuyente/externo')
    browser.find_element_by_id('F1:btnSiguiente').click()
    browser.find_element_by_id('F1:password').send_keys(clave_fiscal)
    browser.find_element_by_id('F1:btnIngresar').click()
    

  except:
    print('No se encontro elemento deuda.\n')

if __name__ == '__main__':
  cuit = input('Ingrese el CUIT: ')
  clave_fiscal = input('Ingrese la clave fiscal: ')
  browser = webdriver.Chrome()
  login(browser, cuit, clave_fiscal)
  #riesgo = siper(browser)
  deuda(browser, cuit, clave_fiscal)
