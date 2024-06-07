# StarSecurity Backend

StarSecurity Backend es el componente servidor de la aplicación StarSecurity, desarrollado en Python con Flask. Proporciona una API RESTful para gestionar la identificación de usuarios en el proceso de contratación. Además, utiliza técnicas de web scraping para conectarse a la página de la Procuraduría y realizar verificaciones.

## Características principales

- API RESTful construida con Flask para operaciones CRUD.
- Integración con bases de datos PostgreSQL mediante SQLAlchemy.
- Autenticación y autorización con Flask-JWT-Extended.
- Web scraping de la página de la Procuraduría utilizando bibliotecas como requests y BeautifulSoup.
- Procesamiento de imágenes y verificación de identidad con OpenCV y TensorFlow.

## Tecnologías utilizadas

- Python: Lenguaje de programación principal.
- Flask: Micro-framework web para construir la API RESTful.
- SQLAlchemy: Herramienta de mapeo objeto-relacional (ORM) para interactuar con bases de datos.
- Flask-JWT-Extended: Extensión de Flask para implementar autenticación JWT.
- requests y BeautifulSoup: Bibliotecas para realizar web scraping.
- OpenCV: Biblioteca de visión artificial para el procesamiento de imágenes.
- TensorFlow: Biblioteca de aprendizaje automático para la verificación de identidad.

## Requisitos

- Python 3.x
- Las dependencias listadas en el archivo `requirements.txt`

## Instalación y configuración

1. Clona este repositorio: `git clone https://github.com/tu-usuario/starsecurity-backend.git`
2. Navega al directorio del proyecto: `cd starsecurity-backend`
3. Crea un entorno virtual: `python -m venv env`
4. Activa el entorno virtual: `source env/bin/activate` (en Windows, `env\Scripts\activate`)
5. Instala las dependencias: `pip install -r requirements.txt`
6. Configura las variables de entorno necesarias (cadena de conexión a la base de datos, claves de seguridad, etc.).
7. Inicia el servidor: `python app.py`

## Licencia

StarSecurity Backend está licenciado bajo la Licencia Propietaria. Esta licencia es adecuada para proyectos comerciales o de código cerrado, ya que restringe la distribución, modificación y uso del software sin autorización expresa del propietario.

Al utilizar esta licencia, se protege el código fuente y se evita que el software se distribuya o se modifique sin el consentimiento del propietario. Esta opción es recomendable si se planea mantener el código cerrado y no se desea que otros puedan acceder, copiar o modificar el software sin permiso.
