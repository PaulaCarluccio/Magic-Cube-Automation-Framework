# Magic-Cube-Automation-Framework

Comandos para ejecutar los tests:
pytest --alluredir=reports/allure_results
python -m pytest -v tests/test_cards.py --alluredir=allure-results

Comando para ver el reporte:
allure serve reports/allure_results