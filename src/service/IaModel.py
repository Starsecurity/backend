import cv2
from flask import jsonify
from skimage.metrics import structural_similarity as ssim

class IaModel():
    
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