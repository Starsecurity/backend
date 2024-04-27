import cv2
import requests
import numpy as np
from skimage.metrics import structural_similarity as ssim

class IaModel():
    
    @classmethod
    def transforma_en_imagen(self, url):
        
        # Comprobar si la solicitud fue exitosa
        headers = {'Origin': 'https://localhost:3000/'}
        response = requests.get(url,headers=headers)
        
        if response.status_code == 200:
            # Leer los datos de la respuesta como bytes
            image_bytes = response.content
            # Convertir los bytes a un objeto numpy para OpenCV
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return image
        else:
            return None, 404

    @classmethod
    def comparar_bordes(self, fingerprint, reverso_cedula):
        # Convertir imágenes a escala de grises
        gray1 = cv2.cvtColor(fingerprint, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(reverso_cedula, cv2.COLOR_BGR2GRAY)
        
        # Detección de bordes usando el algoritmo Canny
        edges1 = cv2.Canny(gray1, 100, 200)
        edges2 = cv2.Canny(gray2, 100, 200)
        
        # Calcular la similitud estructural entre los bordes de las imágenes
        similarity = ssim(edges1, edges2)
        
        return similarity