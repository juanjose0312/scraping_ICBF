import time
import json
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def cargar_credenciales():

    # esta funcion carga las credenciales desde un archivo json

    with open('credenciales.json', 'r') as archivo:
        credenciales = json.load(archivo)
    return credenciales

def dar_click(direccion):
    objeto=driver.find_element(By.XPATH, direccion)
    objeto.click()

def ingresar_texto(direccion, texto):
    objeto=driver.find_element(By.XPATH, direccion)
    objeto.send_keys(texto)

def limpiar_df(texto):

    # esta funcion toma un texto y lo convierte en un dataframe
    # y hace una depuracion con algunas excepciones

    df = texto
    df = df.replace('   ', ' N/A ')
    df = df.replace('DE JE', 'DE_JE')
    df = df.replace('DE LA R', 'DE_LA_R')
    df = df.replace('DE LA C', 'DE_LA_C')
    df = df.split('\n')
    df = [i.split(" ") for i in df]
    df = pd.DataFrame(df)
    df = df.iloc[1:21, 0:11]
    df.columns = ['tipo_documento', 'documento', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'tomas', 'estado','aux','aux','aux']    
    return df

#URL de la pagina que se va a abrir
url         ='https://rubonline.icbf.gov.co/'

#Cargar las credenciales
credenciales = cargar_credenciales()

usuario_x = credenciales['usuario']
clave_x =   credenciales['clave']
unidad_x =  credenciales['unidad']

#Abrir el navegador
driver=webdriver.Chrome()
driver.maximize_window()
driver.get(url)

# ingresar credenciales
ingresar_texto('//*[@id="UserName"]', usuario_x)    #usuario

ingresar_texto('//*[@id="Password"]', clave_x)      #clave

dar_click('//*[@id="LoginButton"]')                 #boton ingresar

# navegar a la seccion de seguimiento nutricional

dar_click('//*[@id="ulMenuPrincipal"]/li[1]/ul/li/a') # seguimiento nutricional

time.sleep(1)

dar_click('//*[@id="ulMenuPrincipal"]/li[1]/ul/li/ul/li[6]/a') # seguimiento nutricional

# Cambia al contenido del frame
driver.switch_to.frame('frameContent')

dar_click('//*[@id="cphCont_btnFiltrar"]') # boton busqueda de registro

# Obtiene el nombre de la ventana original
ventana_original = driver.current_window_handle

# Cambia a la nueva ventana
for ventana in driver.window_handles:
    if ventana != ventana_original:
        driver.switch_to.window(ventana)
        break

ingresar_texto('//*[@id="cphCont_TxtCodigoUnidadServicio"]', unidad_x)  # ingresa la unidad

dar_click('//*[@id="cphCont_DdlIdDepartamento"]') # abrir lista de ciudad

dar_click('/html/body/form/table[2]/tbody/tr/td[3]/div/table/tbody/tr[4]/td[1]/select/option[6]') # seleccionar ciudad

dar_click('/html/body/form/table[2]/tbody/tr/td[3]/table/tbody/tr/td[2]/a/img') # boton buscar

dar_click('//*[@id="cphCont_GvUnidadServicio_btnInfo_0"]') # seleccionar la unidad

# Cambia de nuevo a la ventana original
driver.switch_to.window(ventana_original)

# cambiar al contenido del frame
driver.switch_to.frame('frameContent')

# Recopilador de datos en fortmato texto
wb_db = driver.find_element(By.XPATH,'/html/body/form/table/tbody/tr/td[3]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody').text

# procesamiento de la base para extraer el numero de paginas
num_pag_df = wb_db.split('\n')
num_pag_df = [i.split(" ") for i in num_pag_df]
num_pag_df = pd.DataFrame(num_pag_df)

# determinar el numero de paginas
numero_pagians = num_pag_df.iloc[-1:,:]
numero_pagians = int(numero_pagians.apply(pd.to_numeric).max().max())

# crear un dataframe vacio para recopilar los datos
wb_db_conglomerado = pd.DataFrame()

for i in range(numero_pagians):

    # Recopilador de datos en fortmato texto
    wb_db = driver.find_element(By.XPATH,'/html/body/form/table/tbody/tr/td[3]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody').text
    wb_db = limpiar_df(wb_db)

    # hace un conglomerado de los datos de las paginas
    wb_db_conglomerado = wb_db_conglomerado.reset_index(drop=True)
    wb_db = wb_db.reset_index(drop=True)
    wb_db_conglomerado = pd.concat([wb_db_conglomerado, wb_db], axis=0)
    
    # click siguiente pagina
    if i<4:
        boton_siguiente=driver.find_element(By.XPATH,'/html/body/form/table/tbody/tr/td[3]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[22]/td/table/tbody/tr/td['+str(i+2)+']/a')
        boton_siguiente.click()

# borra los archivos si existen
try:
    os.remove("info.csv")
    os.remove("info.xlsx")
except:
    print('no se pudo remover los documentos')

# Guardar el DataFrame 'wb_db_conglomerado' en un archivo CSV
wb_db_conglomerado.to_csv('info.csv', index=False)

# Guardar el DataFrame 'wb_db_conglomerado' en un archivo Excel con modificaciones para que este listo para ser llenado
db_xlsx = wb_db_conglomerado.iloc[:-1, 1:5]
db_xlsx = db_xlsx.drop(['segundo_nombre'], axis=1)

columns = ['regimen','eps','controles','peso','talla','canalizado','recibio_tratamiento','meses_lactantes']

for i in range(8):
    db_xlsx[columns[i]] = None

db_xlsx.to_excel('info.xlsx', index=False)