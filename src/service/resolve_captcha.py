import re, time, json
from playwright.sync_api import Page, expect, sync_playwright

with open('captcha_questions.json', 'r', encoding='utf-8') as file:
    captcha_questions = json.load(file)

class VerificacionAntecedentes():
    @classmethod
    def captcha_answer(captcha_question):
        if captcha_question in captcha_questions:
            return captcha_questions[captcha_question]
        
    @classmethod
    def get_judicial_data(self,cedula):
        try:
            with sync_playwright() as p:
                tipo_cedula = "Cédula de ciudadanía - NUIP"
                
                browser = p.chromium.launch()
                page = browser.new_page()
                url = "https://apps.procuraduria.gov.co/webcert/inicio.aspx"
                page.goto(url)
                
                # Asegurándonos de seleccionar correctamente el tipo de documento y rellenar el número
                page.select_option('#ddlTipoID', value=tipo_cedula)
                page.wait_for_selector("#txtNumID").fill(cedula)
                
                while True:  # Añadir un bucle para reintento
                    # Capturando y respondiendo al captcha
                    pregunta = page.query_selector("#lblPregunta").text_content()
                    print(pregunta)
                    answer = self.captcha_answer(pregunta)
                    
                    if answer:
                        page.wait_for_selector("#txtRespuestaPregunta").fill(answer)
                        break  # Salir del bucle si se encuentra una respuesta
                    else:
                        page.click('#ImageButton1')  # Suponiendo que este es el ID del botón para refrescar el captcha
                        time.sleep(2)  # Un pequeño retardo para permitir la carga de una nueva pregunta
                
                # Esperar un tiempo antes de finalizar la navegación
                page.wait_for_timeout(1000)
                page.click('#btnConsultar')
                
                personal_data = page.locator(".datosConsultado").text_content()
                judicial_status = page.locator(".datosConsultado+h2").text_content()
                
                return personal_data, judicial_status
                
        except Exception as error:
            print(f"An error occurred: {error}")