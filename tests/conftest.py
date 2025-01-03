import os
import requests
import pytest
import matplotlib.pyplot as plt
import allure

# URL base de la API
BASE_URL = "https://api.scryfall.com/"
HEADERS = {
    "Content-Type": "application/json",
}
TIMEOUT = 10

class APIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS

    def get_card_by_name(self, name):
        url = f"{self.base_url}cards/named?fuzzy={name}"
        response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
        response.raise_for_status()  # Lanza un error si la solicitud falla
        return response.json()

@pytest.fixture
def api_client():
    return APIClient()

def load_card_colors(file_path):
    """Carga los nombres de cartas y sus categorías de color desde un archivo CSV."""
    try:
        with open(file_path, 'r') as file:
            card_colors = {}
            for line in file:
                if line.strip():
                    name, color = line.strip().split(',')
                    card_colors[name.strip()] = color.strip()
            return card_colors
    except Exception as e:
        print(f"Error al cargar colores de cartas: {e}")
        return {}

def save_card_image(card_name, image_url, color_category, base_directory="images"):
    # Crear directorio por color
    color_directory = os.path.join(base_directory, color_category)
    os.makedirs(color_directory, exist_ok=True)

    image_path = os.path.join(color_directory, f"{card_name}.png")
    try:
        response = requests.get(image_url, timeout=TIMEOUT)
        response.raise_for_status()
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"Imagen guardada en: {image_path}")
        return image_path
    except Exception as e:
        print(f"Error al descargar la imagen para {card_name}: {e}")
        return None

# Variables globales para contar resultados
total_tests = 0
passed_tests = 0
failed_tests = 0

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    global passed_tests, failed_tests
    if report.when == "call":
        if report.passed:
            passed_tests += 1
        elif report.failed:
            failed_tests += 1

def pytest_terminal_summary(terminalreporter, exitstatus):
    terminalreporter.write_sep("=", "Resultados de las pruebas")
    terminalreporter.write(f'Gráfico de resultados guardado en: reports/test_results.png')

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    allure.dynamic.title(item.name)
    allure.dynamic.description(f"Ejecutando {item.name}")
