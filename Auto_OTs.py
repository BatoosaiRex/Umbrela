import pandas as pd
from playwright.sync_api import sync_playwright
import time
from playwright.sync_api import TimeoutError

df = pd.read_excel(r"D:\Doc\OneDrive\Nokia\Archivo Carga.xlsx", dtype={'ID OTM': str, 'Link OTM': str})

print(df.columns.tolist())

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    #Login Claro
    page = browser.new_page()
    
    page.goto("https://claro.lavenir.com.co/es/login")

    page.wait_for_selector("[data-pc-section='closebutton']")
    page.click("[data-pc-section='closebutton']")

    page.wait_for_selector("[placeholder='Usuario']")
    page.fill("input[placeholder='Usuario']", "46395701")
    page.fill("input[placeholder='Contraseña']", "Nokia192++")
    print("Pausa: resuelve el captcha en la ventana del navegador. Cuando termines, pulsa 'Resume' en el Playwright Inspector.")
    page.pause()

    page.click("input[value='Iniciar sesión']")

    # Inciar bucle para llenar datos desde el DataFrame
    for idx, row in df.iterrows():

         # saltar filas vacías y OTM ya creadas
        if row.isna().all():
            continue
        
        time.sleep(3) 

        #Navegar a Flujo de servicios

        page.goto("https://claro.lavenir.com.co/es/user/task/jobsflow")

        try:
            page.wait_for_selector("[placeholder='Buscar']", timeout=30000)
            page.wait_for_selector("[title='Crear']", state="visible", timeout=10000)
            page.click("[title='Crear']")
        except TimeoutError as e:
            print("No se encontró el elemento 'Crear' dentro del timeout:", e)
            page.screenshot(path="error_crear_not_found.png")

        #Crear OT
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[4]/div[4]/div[1]/div[1]/div[1]/div[2]/p[1]", timeout=30000)
        page.click("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[4]/div[4]/div[1]/div[1]/div[1]/div[2]/p[1]",timeout=10000)

        #Fechas de inicio y fin
        page.wait_for_selector("[placeholder='dd/mm/yyyy']", state="visible")
        page.click("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/form[1]/div[1]/div[1]/div[1]/input[1]", timeout=30000)
        page.click("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]", timeout=30000)
        page.click("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/form[1]/div[2]/div[1]/div[1]/input[1]", timeout=30000)
        page.click("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]", timeout=30000)
        page.click("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/form[1]/div[3]/input[1]", timeout=30000)
   
        print(f"Procesando fila {idx + 1}")

        #SiteName
        page.fill(
            "xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/span[1]/input[1]",
            row['siteName'])
        page.wait_for_selector("div.p-3", timeout=50000)
        page.click(f"div.p-3[title='{row['siteName'].upper()}']")

        #Lider GI
        page.fill("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[4]/span[1]/input[1]", 
            row['Lider GI'])
        page.wait_for_selector("div.p-3", timeout=50000)
        page.click(f"div.p-3[title*='{row['Lider GI'].upper()}']")
        time.sleep(0.5)

        #Diseñador OT
        page.fill("xpath=//html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[7]/span[1]/input[1]", 
            row['Diseñador'])
        page.wait_for_selector("div.p-3", timeout=50000)
        page.click(f"div.p-3[title*='{row['Diseñador'].upper()}']")

        #Actividad OT
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[8]/div[2]/div[3]/*[name()='svg'][1]", timeout=50000, state="visible")
        page.click("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[8]/div[2]/div[3]/*[name()='svg'][1]", timeout=10000)
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[8]/div[2]", timeout=50000, state="visible")
        page.wait_for_selector("xpath=/html/body/div[5]/div/ul/li[3]/span", timeout=50000, state="visible")
        page.click("xpath=/html/body/div[5]/div/ul/li[3]", timeout=50000)

        #ID_SMP
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[9]/input[1]", timeout=50000, state="visible")
        page.fill("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[9]/input[1]",row['ID_SMP'])

        #Proyecto
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[10]/input[1]", timeout=50000, state="visible")
        page.fill("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[10]/input[1]",row['proyecto'])
       
        #ODH
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[8]/div[2]/div[3]/*[name()='svg'][1]/*[name()='path'][1]", timeout=50000, state="visible")
        page.click("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[11]/div[2]", timeout=10000)
        page.wait_for_selector("xpath=/html/body/div[5]/div/ul/li[1]", timeout=50000, state="visible")
        page.click("xpath=/html/body/div[5]/div/ul/li[3]/span", timeout=50000)

        #SMP
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[12]/input[1]", timeout=50000, state="visible")
        page.fill("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[12]/input[1]",row['SMP Amparador del Servicio'])
        
        #Obaservaciones
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[13]/textarea[1]", timeout=50000)
        page.fill("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[13]/textarea[1]",row['Observaciones'])
        
        #Guardar OT
        page.wait_for_selector("xpath=//html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/button[1]", timeout=50000)
        page.click("xpath=//html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/button[1]", timeout=10000)

        #esperar a que se cree la OT
        page.wait_for_selector("xpath=/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]", timeout=50000)
        link = page.url

        #Extraer OTM
        page.wait_for_selector("xpath=/html/body/div[4]/div/div/div[1]/h2/span", timeout=50000)
        print(f"OT creada para la fila {idx + 1}: {link}")
        time.sleep(2)
        texto = page.locator("xpath=/html/body/div[4]/div/div/div[1]/h2/span").text_content()
        print(f"esto es texto: {texto}")
        partes = texto.split()
        print(partes[1])
        print(partes[2])
        print(partes[3])

        OTMsimbol = partes[3]
        print(OTMsimbol)
        OTM = OTMsimbol.replace("[", "").replace("]", "")

        print(f"OT creada para la fila {idx + 1}: {link} - {OTM}")

        # Guardar OTM, ID y Link en DataFrame
        
        df.loc[idx, 'ID OTM'] = OTM
        df.loc[idx, 'Link OTM'] = link

        # Guardar en Excel después de procesar todas las filas
        df.to_excel(r"D:\Doc\OneDrive\Nokia\Archivo Carga.xlsx", index=False)

    # Imprimir resumen de los resultados
    print("Resumen de OT creadas:")
    for idx in range(len(df)):
        if pd.notna(df.loc[idx, 'ID OTM']):
            print(f"Fila {idx + 1}: ID OTM = {df.loc[idx, 'ID OTM']}, Link OTM = {df.loc[idx, 'Link OTM']}")

browser.close()
