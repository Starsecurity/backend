#Se llama antecedentes.py porque el servicio se encarga de verificar si una persona tiene antecedentes judiciales
import requests
from bs4 import BeautifulSoup
import random

class VerificationService:
    def __init__(self):
        self.URL = "https://procesos.ramajudicial.gov.co/jepms/armeniajepms/lista.asp"
        self.RequestSend = requests.session()
        self.RANDOM_AGENT = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (X11; Linux i686; rv:107.0) Gecko/20100101 Firefox/107.0',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            # Agrega más agentes de usuario si es necesario
        ]

    def verify_cedula(self, cedula):
        headers = {"Content-Type": 'application/x-www-form-urlencoded', "User-Agent": random.choice(self.RANDOM_AGENT)}
        data_encode = "cbadju=3&norad=%s&Buscar=Buscar" % str(cedula)

        response = self.RequestSend.post(self.URL, headers=headers, data=data_encode)
        soup = BeautifulSoup(response.content, "html.parser")

        if response.status_code == 200:
            try:
                cedula_encontrada = soup.find_all('td')[4].text
                if cedula_encontrada == str(cedula):
                    return True
                else:
                    return False
            except IndexError:
                return False
        else:
            print(f"Error en el servidor: {response.status_code}")
            return False