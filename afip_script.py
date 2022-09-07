#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bs4
import requests
import re
from selenium import webdriver
from datetime import date
import openpyxl
from openpyxl.styles import Font

# def extraer_datos():
# del excel

def login(browser, cuit, clave_fiscal):
  try:
    browser.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')
    browser.find_element_by_id('F1:username').send_keys(cuit)
    browser.find_element_by_id('F1:btnSiguiente').click()
    browser.find_element_by_id('F1:password').send_keys(clave_fiscal)
    browser.find_element_by_id('F1:btnIngresar').click()
  except:
    print('Error en login')

#def siper():
# sacar el riesgo

if __name__ == '__main__':
  cuit = input('Ingrese el CUIT: ')
  clave_fiscal = input('Ingrese la clave fiscal: ')
  browser = webdriver.Chrome()
  login(browser, cuit, clave_fiscal)
