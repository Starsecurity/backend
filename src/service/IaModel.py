import cv2
from flask import jsonify
import numpy as np
import requests
from skimage.metrics import structural_similarity as ssim

class IaModel():
    @classmethod
    def transforma_en_imagen(self, url):
        # Comprobar si la solicitud fue exitosa
        response = requests.get(url)
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



    @classmethod
    def comparar_rostros(cls,img1_path, img2_path):
        # Cargar el clasificador preentrenado para detectar rostros
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Cargar las imágenes a comparar
        img1 = img1_path
        img2 = img2_path

        # Verificar que las imágenes se han cargado correctamente
        if img1 is None or img2 is None:
            print("Error: No se pudieron cargar las imágenes")
            return None

        # Convertir las imágenes a escala de grises
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en ambas imágenes
        faces1 = face_cascade.detectMultiScale(gray1, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        faces2 = face_cascade.detectMultiScale(gray2, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        '''if len(faces1) == 0:
            print("Error: No se detectaron rostros en la primera imagen")
        return None'''

        # Inicializar el reconocedor
        recognizer = cv2.face.EigenFaceRecognizer_create()

        # Variables para el entrenamiento
        face_images = []
        labels = []

        # Comparar los rostros en la segunda imagen con los rostros en la primera imagen
        matches = 0
        total_faces = 0

        # Procesar los rostros en la primera imagen y entrenar el reconocedor
        for (x, y, w, h) in faces1:
            roi_gray = gray1[y:y+h, x:x+w]
            face_images.append(cv2.resize(roi_gray, (100, 100)))  # Redimensionar las imágenes para el entrenamiento
            labels.append(1)  # Etiqueta para la imagen de referencia
            
        '''if len(face_images) == 0:
            print("Error: No se encontraron rostros en la primera imagen para entrenar el reconocedor")
        return None'''
            
        #recognizer.train(face_images, np.array(labels))
            # Comparar los rostros en la segunda imagen
        for (x2, y2, w2, h2) in faces2:
            total_faces += 1
            roi_gray_resized = cv2.resize(gray2[y2:y2+h2, x2:x2+w2], (100, 100))  # Redimensionar la imagen de prueba                recognizer.update([roi_gray_resized], np.array([1]))  # Actualizar el reconocedor con cada rostro
            label, confidence = recognizer.predict(roi_gray_resized)
            
            # Incrementar el contador de coincidencias si el reconocimiento es exitoso
            if confidence < 2000:  # Ajustar este umbral según sea necesario
                matches += 1
        # Mostrar las imágenes con los rectángulos dibujados
        cv2.imshow('Rostros en la primera imagen', img1)
        cv2.imshow('Rostros en la segunda imagen', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Calcular el porcentaje de compatibilidad
        compatibility_percentage = (matches / total_faces) * 100 if total_faces > 0 else 0
        return compatibility_percentage

