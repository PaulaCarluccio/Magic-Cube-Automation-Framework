# Magic-Cube-Automation-Framework
### **ByPauna**

## 🔧 **Comando para ejecutar los tests:**
```bash
python -m pytest -v tests/test_cards.py
```

## 📊 **Comando para ver el reporte:**
```bash
allure serve reports/allure_results
```

## 📌 Descripción:
Este framework está diseñado para automatizar pruebas de cartas, obtener información sobre ellas y generar reportes visuales usando Allure.

## 🚀 Flujo de trabajo:
1. Ejecuta las pruebas con el siguiente comando:
    ```bash
    python -m pytest -v tests/test_cards.py
    ```
2. Una vez que las pruebas se hayan ejecutado, puedes ver los resultados interactivos con el siguiente comando:
    ```bash
    allure serve reports/allure_results
    ```

## 📦 **Requisitos para ejecutar el proyecto:**

Asegúrate de tener instalados los siguientes paquetes y herramientas:

1. **Python**: Asegúrate de tener instalada una versión de Python compatible (3.6 o superior).
   - Para instalar Python: [python.org](https://www.python.org/)

2. **pytest**: Framework para pruebas.
    ```bash
    pip install pytest
    ```

3. **Allure**: Herramienta para generar reportes visuales interactivos.
    - Windows:
    - Descarga e instala Allure desde [aquí](https://github.com/allure-framework/allure2/releases).
    - Agrega la carpeta de Allure a tu variable de entorno PATH.

4. **Requests**: Librería para hacer solicitudes HTTP.
    ```bash
    pip install requests
    ```
5. **pytest-allure-adaptor**: Plugin que integra Allure con pytest.
    ```bash
    pip install allure-pytest
    ```