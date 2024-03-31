import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def cargar_credenciales():
    with open('credenciales.json', 'r') as archivo:
        credenciales = json.load(archivo)
    return credenciales

def dar_click(direccion):
    objeto=driver.find_element(By.XPATH, direccion)
    objeto.click()

def ingresar_texto(direccion, texto):
    objeto=driver.find_element(By.XPATH, direccion)
    objeto.send_keys(texto)

#URL de la pagina que se va a abrir
url         ='https://rubonline.icbf.gov.co/'

#Cargar las credenciales
credenciales = cargar_credenciales()

usuario_x = credenciales['usuario']
clave_x =   credenciales['clave']
unidad_x =  credenciales['unidad']
db_fecha_vacuna = '27/02/2024'

#Abrir el navegador
driver=webdriver.Chrome()
driver.maximize_window()
driver.get(url)

#Espera 2 segundos
time.sleep(2)

# ingresa el usuario y la clave e ingresa
ingresar_texto('//*[@id="UserName"]', usuario_x)

ingresar_texto('//*[@id="Password"]', clave_x)

dar_click('//*[@id="LoginButton"]')

rub_online=driver.find_element(By.XPATH,'//*[@id="ulMenuPrincipal"]/li[1]/ul/li/a')
rub_online.click()

time.sleep(1)

seg_nuticional=driver.find_element(By.XPATH,'//*[@id="ulMenuPrincipal"]/li[1]/ul/li/ul/li[6]/a')
seg_nuticional.click()

time.sleep(2)

# Cambia al contenido del frame
driver.switch_to.frame('frameContent')

# Haz clic en el botón que abre la nueva ventana
boton_usuario=driver.find_element(By.XPATH,'//*[@id="cphCont_btnFiltrar"]')
boton_usuario.click()

# Espera a que la nueva ventana se abra
time.sleep(2)

# Obtiene el nombre de la ventana original
ventana_original = driver.current_window_handle

# Cambia a la nueva ventana
for ventana in driver.window_handles:
    if ventana != ventana_original:
        driver.switch_to.window(ventana)
        break

# ingresa la unidad
unidad=driver.find_element(By.XPATH,'//*[@id="cphCont_TxtCodigoUnidadServicio"]')
unidad.send_keys(unidad_x)

# abrir lista de ciudad
lista_ciudad=driver.find_element(By.XPATH,'//*[@id="cphCont_DdlIdDepartamento"]')
lista_ciudad.click()

# seleccionar ciudad
ciudad=driver.find_element(By.XPATH,'/html/body/form/table[2]/tbody/tr/td[3]/div/table/tbody/tr[4]/td[1]/select/option[6]')
ciudad.click()

# boton buscar
boton_buscar=driver.find_element(By.XPATH,'/html/body/form/table[2]/tbody/tr/td[3]/table/tbody/tr/td[2]/a/img')
boton_buscar.click()

# seleccionar la unidad
unidad=driver.find_element(By.XPATH,'//*[@id="cphCont_GvUnidadServicio_btnInfo_0"]')
unidad.click()

# Cambia de nuevo a la ventana original
driver.switch_to.window(ventana_original)


#  cambia al frame
driver.switch_to.frame('frameContent')

#Crea un df para consultar los datos
df_db = pd.read_excel('info.xlsx')
wb_db = pd.read_csv('info.csv')

#Crea un contador para saber cuantos registros se han subido
contador = 0
num_registros = (len(df_db)-1)
                    
num_pag_df = wb_db.iloc[-1:,:]
num_pag_df = int(num_pag_df.apply(pd.to_numeric).max().max())

#Ingresa a cada registro y sube los datos y los guarda

for i in range(num_pag_df):

    for j in range(20):

        contador += 1

        if contador > num_registros:
            break

        # busca en la db el nombre y el apellido
        mascara = (df_db['primer_nombre'] == wb_db['primer_nombre'][j]) & (df_db['primer_apellido'] == wb_db['primer_apellido'][j])
        df_filtrado = df_db[mascara]

        #revisa si hay datos si no hay datos pasa al siguiente ciclo del for
        if df_filtrado.empty:
            print('No se encontraron registros de ' + wb_db['primer_nombre'] + ' ' + wb_db['primer_apellido'])
            continue
        
        #si hay datos los guarda en variables
        db_regimen =    df_filtrado['regimen'].iloc[0]
        db_eps =        df_filtrado['eps'].iloc[0]
        db_controles =  df_filtrado['controles'].iloc[0]
        db_peso =       df_filtrado['peso'].iloc[0]
        db_talla =      df_filtrado['talla'].iloc[0]
        db_canalizado = df_filtrado['canalizado'].iloc[0]
        db_recibio_tratamiento = df_filtrado['recibio_tratamiento'].iloc[0]
        db_meses_lactantes = df_filtrado['meses_lactantes'].iloc[0]

        #boton abrir registro 
        dar_click('//*[@id="cphCont_gvBeneficiarios_btnInfo_'+str(j)+'"]')

        #presionar agregar
        dar_click('/html/body/form/table/tbody/tr/td[3]/table[1]/tbody/tr/td[3]/a[2]/img')

        #lista contributivo (si no esta afiliado aparece un aviso)
        try:
            dar_click('//*[@id="cphCont_MsgInfo_btnAceptar"]')
        except:
            pass
        
        #lista regimen
        dropdown = Select(driver.find_element(By.XPATH,'//*[@id="ddlIdRegimenSeguridadSocial"]'))
        dropdown.select_by_visible_text(str(db_regimen))

        if db_regimen == 'NO AFILIADO(A)':
            try:
                dar_click('//*[@id="cphCont_MsgInfo_btnAceptar"]')
            except:
                pass
            else:
                dar_click('//*[@id="rbPresentaCarneVacunacion_1"]') # carnet de vacunas
                dar_click('//*[@id="rbCarneVacunacionAlDia_1"]') # carnet bien revisado
                dar_click('//*[@id="rbCarneCrecimientoDesarrollo_1"]') # carnet crecimiento y desarrollo
        else:
            #lista eps  
            dropdown = Select(driver.find_element(By.XPATH,'//*[@id="cphCont_ddlIdEPS"]'))
            dropdown.select_by_visible_text(str(db_eps))

            # 3 botones de seleccionar cuando tieene eps
            dar_click('//*[@id="rbPresentaCarneVacunacion_0"]') # carnet de vacunas
            dar_click('//*[@id="rbCarneVacunacionAlDia_0"]') # carnet bien revisado
            dar_click('//*[@id="rbCarneCrecimientoDesarrollo_0"]') # carnet crecimiento y desarrollo
            dropdown = Select(driver.find_element(By.XPATH,'//*[@id="cphCont_ddlControlesCrecimDesarrollo"]'))
            dropdown.select_by_visible_text(str(int(db_controles)))

        #poner fecha de revision de vacunas
        ingresar_texto('//*[@id="cphCont_cuwFechaVerificaVacunas_txtFecha"]',db_fecha_vacuna)
        dar_click('//*[@id="cphCont_cuwFechaVerificaVacunas_imgCalendario"]')

        #poner misma fecha de revison de vacunas
        ingresar_texto('//*[@id="cphCont_cuwFechaValoracionNuricional_txtFecha"]',db_fecha_vacuna)
        dar_click('//*[@id="cphCont_cuwFechaValoracionNuricional_imgCalendario"]')

        #poner peso
        ingresar_texto('//*[@id="cphCont_txtPeso"]',db_peso)

        #poner talla
        dar_click('//*[@id="cphCont_txtTalla"]')
        time.sleep(1)
        ingresar_texto('//*[@id="cphCont_txtTalla"]',db_talla)

        #fue canalizado en la desnutricion aguda
        dropdown = Select(driver.find_element(By.XPATH,'//*[@id="cphCont_ddlFueCanalizado"]'))
        dropdown.select_by_visible_text(db_canalizado)

        #fue tratado por desnutricion aguda
        dropdown = Select(driver.find_element(By.XPATH,'//*[@id="cphCont_ddlRecibioTratamiento"]'))
        dropdown.select_by_visible_text(db_recibio_tratamiento)

        #NO programa icbf
        dropdown = Select(driver.find_element(By.XPATH,'//*[@id="cphCont_ddlHijoMujerGestanteAtendidaServiciosICBF"]'))
        dropdown.select_by_visible_text('No')

        try:
            dar_click('//*[@id="rbAlimentadoLecheMaterna_0"]')
        except:
            pass

        #poner 6 mesess de lactancia
        driver.find_element(By.XPATH,'//*[@id="cphCont_txtLactanciaMaternaExclusiva"]').clear()
        ingresar_texto('//*[@id="cphCont_txtLactanciaMaternaExclusiva"]','6')

        #poner el valor de lactancia total
        driver.find_element(By.XPATH,'//*[@id="cphCont_txtLactanciaMaternaTotal"]').clear()
        ingresar_texto('//*[@id="cphCont_txtLactanciaMaternaTotal"]',db_meses_lactantes)

        #boton de guardar

        time.sleep(60)
        
        # vuelve a la pantalla original
        driver.switch_to.default_content()

        #darle a seguimiento nutricion
        dar_click('//*[@id="ulMenuPrincipal"]/li[1]/ul/li/ul/li[6]/a')

        #  cambia al frame
        driver.switch_to.frame('frameContent')
        
        if i != 0:
            dar_click('/html/body/form/table/tbody/tr/td[3]/div/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[22]/td/table/tbody/tr/td['+str(i+1)+']/a') 

    time.sleep(5)
   