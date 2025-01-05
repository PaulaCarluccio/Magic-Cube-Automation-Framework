import os
import requests
import pytest
import allure

# Url base para interactuar con la API de Scryfall
BASE_URL = "https://api.scryfall.com/"  # URL base de la API
HEADERS = {
    "Content-Type": "application/json",  # Tipo de contenido esperado
}
TIMEOUT = 10  # Tiempo máximo de espera para las solicitudes (en segundos)

class APIClient:
    """
    Cliente para interactuar con la API de Scryfall.
    Contiene métodos para realizar solicitudes y manejar la respuesta.
    """
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS

    def get_card_by_name(self, name):
        """
        Realiza una solicitud GET para obtener los datos de una carta específica por nombre.
        Usa el parámetro 'fuzzy' para buscar cartas con nombres similares.
        """
        url = f"{self.base_url}cards/named?fuzzy={name}"
        response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
        response.raise_for_status()  # Lanza un error si la solicitud falla (e.g., 404, 500)
        return response.json()  # Retorna la respuesta como un diccionario JSON

# Pytest fixture que devuelve una instancia del cliente API
@pytest.fixture
def api_client():
    return APIClient()

def load_card_colors(file_path):
    """
    Carga los nombres de las cartas y sus categorías de color desde un archivo CSV.
    El archivo debe tener formato 'nombre_de_carta,color' en cada línea.
    """
    try:
        with open(file_path, 'r') as file:
            card_colors = {}
            for line in file:
                if line.strip():  # Ignorar líneas vacías
                    name, color = line.strip().split(',')
                    card_colors[name.strip()] = color.strip()
            return card_colors
    except Exception as e:
        print(f"Error al cargar colores de cartas: {e}")
        return {}

def save_card_image(card_name, image_url, color_category, base_directory="images"):
    """
    Descarga y guarda la imagen de una carta en un directorio categorizado por colores.
    """
    # Crear un subdirectorio basado en la categoría de color
    color_directory = os.path.join(base_directory, color_category)
    os.makedirs(color_directory, exist_ok=True)

    # Ruta completa para guardar la imagen
    image_path = os.path.join(color_directory, f"{card_name}.png")
    try:
        # Realizar la solicitud GET para obtener la imagen
        response = requests.get(image_url, timeout=TIMEOUT)
        response.raise_for_status()
        with open(image_path, "wb") as file:  # Guardar la imagen en modo binario
            file.write(response.content)
        print(f"Imagen guardada en: {image_path}")
        return image_path
    except Exception as e:
        print(f"Error al descargar la imagen para {card_name}: {e}")
        return None

# Variables globales para rastrear el total de pruebas y sus resultados
total_tests = 0
passed_tests = 0
failed_tests = 0

# Hook de Pytest para capturar el resultado de cada prueba
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """
    Hook para actualizar el conteo de pruebas aprobadas y fallidas.
    """
    global passed_tests, failed_tests
    if report.when == "call":
        if report.passed:
            passed_tests += 1
        elif report.failed:
            failed_tests += 1

# Resumen final que se muestra en la terminal después de las pruebas
def pytest_terminal_summary(terminalreporter, exitstatus):
    terminalreporter.write_sep("=", "Reporte de la ejecución")
    terminalreporter.write('Para visualizar el reporte de Allure, ejecuta el siguiente comando:\n')
    terminalreporter.write('allure serve reports/allure_results\n')

# Hook para configurar dinámicamente los títulos y descripciones de Allure
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    allure.dynamic.title(item.name)  # Nombre del test
    allure.dynamic.description(f"Ejecutando {item.name}")  # Descripción breve del test
