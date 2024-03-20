import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def cargar_credenciales():
    with open('credenciales.json', 'r') as archivo:
        credenciales = json.load(archivo)
    return credenciales

# Definición de funciones
def control_0():
    # código para control 0
    pass

def control_1():
    # código para control 1
    pass

def control_2():
    # código para control 2
    pass

def control_3():
    # código para control 3
    pass

def control_4():
    # código para control 4
    pass

def control_5():
    # código para control 5
    pass

# diccionario de funciones para el # control
switch = {
    '0': control_0,
    '1': control_1,
    '2': control_2,
    '3': control_3,
    '4': control_4,
    '5': control_5
}


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

#Espera 2 segundos
time.sleep(2)

# ingresa el usuario y la clave e ingresa
usuario=driver.find_element(By.XPATH,'//*[@id="UserName"]')
usuario.send_keys(usuario_x)

clave=driver.find_element(By.XPATH,'//*[@id="Password"]')
clave.send_keys(clave_x)

boton_usuario=driver.find_element(By.XPATH,'//*[@id="LoginButton"]')
boton_usuario.click()

rub_online=driver.find_element(By.XPATH,'//*[@id="ulMenuPrincipal"]/li[1]/ul/li/a')
rub_online.click()

time.sleep(1)

seg_nuticional=driver.find_element(By.XPATH,'//*[@id="ulMenuPrincipal"]/li[1]/ul/li/ul/li[6]/a')
seg_nuticional.click()

time.sleep(40)

#Crea un df para consultar los datos
df = pd.read_excel('db.xlsx')
df

#Ingresa a cada registro y sube los datos y los guarda
for i in range(0,20):

    #sacar los datos de la pagina 'primer nombre + segundo nombre'
    wb_primer_nombre = 'LUCIANA'
    wb_primer_apellido = 'ROJAS'
    
    # busca en la db el nombre y el apellido
    mascara = (df['primer_nombre'] == wb_primer_nombre) & (df['primer_apellido'] == wb_primer_apellido)
    df_filtrado = df[mascara]
    
    #revisa si hay datos si no hay datos pasa al siguiente ciclo del for
    if df_filtrado.empty:
        print('No se encontraron registros de ' + wb_primer_nombre + ' ' + wb_primer_apellido)
        continue
    
    #si hay datos los guarda en variables
    db_regimen =    df_filtrado['regimen'].iloc[0]
    db_eps =        df_filtrado['eps'].iloc[0]
    db_controles =  df_filtrado['controles'].iloc[0]
    db_peso =       df_filtrado['peso'].iloc[0]
    db_talla =      df_filtrado['talla'].iloc[0]
    db_meses_lactantes = df_filtrado['meses_lactantes'].iloc[0]


    #presionar agregar

    #lista contributivo (si no esta afiliado aparece un aviso)
    
    #lista eps

    #if tiene eps
    if db_eps == 'NO': #cambiar
        
        #en caso de no tener eps entonces pondra las siguientes opciones en no
        selc_no=driver.find_element(By.XPATH,'')
        selc_no.click()

        selc_no=driver.find_element(By.XPATH,'')
        selc_no.click()

        selc_no=driver.find_element(By.XPATH,'')
        selc_no.click()

    else:
        #si tiene eps entonces selecciona las 3 en si
        selc_si=driver.find_element(By.XPATH,'')
        selc_si.click()

        selc_si=driver.find_element(By.XPATH,'')
        selc_si.click()

        selc_si=driver.find_element(By.XPATH,'')
        selc_si.click()

    #poner la fecha de revision vacuna
        
    #lista numero de controles
        switch[db_controles]()

    #poner misma fecha de revison de vacunas
        
    #poner peso
        
    #poner talla
        
    #NO tiene desnutricion aguda
        
    #NO tiene desnutricion aguda
        
    #NO programa icbf
        
    #poner 6 mesess de lactancia
        
    #poner el valor de lactancia total
        
    #boton de guardar
        
    #darle a seguimiento nutricion