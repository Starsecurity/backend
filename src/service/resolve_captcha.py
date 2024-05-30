import re
import time
import json
from playwright.sync_api import Page, expect, sync_playwright


class VerificacionAntecedentes():
    def __init__(self):
        with open('src/data/captcha_questions.json', 'r', encoding='utf-8') as file:
            self.captcha_questions = json.load(file)

    def captcha_answer(self, captcha_question):
        if captcha_question in self.captcha_questions:
            return self.captcha_questions[captcha_question]

    def get_judicial_data(self, cedula):
        try:
            with sync_playwright() as p:
                tipo_cedula = "Cédula de ciudadanía - NUIP"

                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                url = "https://apps.procuraduria.gov.co/webcert/inicio.aspx"
                page.goto(url)

                # Asegurándonos de seleccionar correctamente el tipo de documento y rellenar el número
                page.select_option('#ddlTipoID', value=tipo_cedula)
                page.wait_for_selector("#txtNumID").fill(cedula)

                while True:  # Añadir un bucle para reintento
                    # Capturando y respondiendo al captcha
                    pregunta = page.query_selector(
                        "#lblPregunta").text_content()
                    answer = self.captcha_answer(pregunta)

                    if answer:
                        page.wait_for_selector(
                            "#txtRespuestaPregunta").fill(answer)
                        break  # Salir del bucle si se encuentra una respuesta
                    else:
                        # Suponiendo que este es el ID del botón para refrescar el captcha
                        page.click('#ImageButton1')
                        # Un pequeño retardo para permitir la carga de una nueva pregunta
                        time.sleep(2)

                # Esperar un tiempo antes de finalizar la navegación
                page.wait_for_timeout(500)
                page.click('#btnConsultar')

                try:
                    validation = page.wait_for_selector("#ValidationSummary1",timeout=1500).text_content()
                    print(validation)
                except:
                    validation = ""
                    
                try:
                    validation2 = page.wait_for_selector("#ValidationSummary2",timeout=1500).text_content()
                except:
                    validation2 = ""
                
                if validation2 != "":
                    return None,None,None
                if validation != "":
                    return None, None, None                

                personal_data = page.locator(".datosConsultado").text_content()
                pattern = r'Señor\(a\)\s+([\w]+)\s+identificado\(a\) con\s+Cédula de ciudadanía\s+Número\s+(\d+).'
                match = re.search(pattern, personal_data)

                if match:
                    nombre = match.group(1)
                    numero_id = match.group(2)
                else:
                    nombre = None
                    numero_id = None

                judicial_status = page.locator(".datosConsultado+h2").text_content()

                if judicial_status == "El ciudadano no presenta antecedentes":
                    judicial_status_bolean = False
                else:
                    judicial_status_bolean = True

                return nombre, numero_id, judicial_status_bolean

        except Exception as error:
            print(f"Hubo un error: {error}")
            return None, None, None

