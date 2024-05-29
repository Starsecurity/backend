import cv2
import numpy as np
import requests
from flask import jsonify
from skimage.metrics import structural_similarity as ssim
from deepface import DeepFace

class IaModel:
    @classmethod
    def transforma_en_imagen(cls, url):
        response = requests.get(url)
        if response.status_code == 200:
            image_bytes = response.content
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return image
        else:
            return None, 404

    @classmethod
    def comparar_bordes(cls, fingerprint, reverso_cedula):
        gray1 = cv2.cvtColor(fingerprint, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(reverso_cedula, cv2.COLOR_BGR2GRAY)

        # Detección de bordes usando el algoritmo Canny
        edges1 = cv2.Canny(gray1, 2, 50)
        edges2 = cv2.Canny(gray2, 2, 50)

        # Calcular la similitud estructural entre los bordes de las imágenes
        similarity = ssim(edges1, edges2)
        return similarity

    @classmethod
    def preprocess_image(cls, image):
        if image is None:
            raise ValueError("La imagen es None")
        if len(image.shape) != 2:
            raise ValueError("La imagen debe estar en escala de grises para ecualizar")
        image = cv2.equalizeHist(image)
        return image

    @classmethod
    def comparar_rostros(cls, profilePhoto, delante_cedula):
        # Convertir las imágenes a RGB (DeepFace requiere imágenes en formato RGB)
        img1_rgb = cv2.cvtColor(profilePhoto, cv2.COLOR_BGR2RGB)
        img2_rgb = cv2.cvtColor(delante_cedula, cv2.COLOR_BGR2RGB)

        # Usar DeepFace para verificar la coincidencia de rostros
        result = DeepFace.verify(img1_rgb, img2_rgb, model_name='VGG-Face')

        # Calcular el porcentaje de compatibilidad
        compatibility_percentage = (1 - result['distance']) * 100

        # Imprimir el resultado de la verificación
        print(f"Resultado: {result['verified']}")
        print(f"Distancia: {result['distance']}")
        print(f"Porcentaje de compatibilidad: {compatibility_percentage:.2f}%")

        return compatibility_percentage

