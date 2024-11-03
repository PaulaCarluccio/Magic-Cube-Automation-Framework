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

def load_card_names(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error al cargar nombres de cartas: {e}")
        return []

def save_card_image(card_name, image_url, save_directory="images"):
    os.makedirs(save_directory, exist_ok=True)
    image_path = os.path.join(save_directory, f"{card_name}.png")
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

def save_pie_chart(passed_tests, failed_tests):
    sizes = [passed_tests, failed_tests]
    labels = ['Passed', 'Failed']
    colors = ['green', 'red']
    
    if sizes and any(sizes):
        plt.pie(sizes, explode=(0, 0.1), labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.savefig('reports/test_results.png')
    else:
        print("No hay datos para generar el gráfico de pastel.")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    global passed_tests, failed_tests
    if report.when == "call":
        if report.passed:
            passed_tests += 1
        elif report.failed:
            failed_tests += 1

def pytest_sessionfinish(session, exitstatus):
    save_pie_chart(passed_tests, failed_tests)

def pytest_terminal_summary(terminalreporter, exitstatus):
    terminalreporter.write_sep("=", "Resultados de las pruebas")
    terminalreporter.write(f'Gráfico de resultados guardado en: reports/test_results.png')

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    allure.dynamic.title(item.name)
    allure.dynamic.description(f"Ejecutando {item.name}")