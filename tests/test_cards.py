import pytest
from conftest import load_card_colors, save_card_image
import allure

"""
------------------------- Reemplazar ruta al CSV aquí: ------------------------- 
card_colors = load_card_colors('.../rutaArchivo.csv')

"""

# Carga los colores de las cartas desde un CSV y los almacena en un diccionario.
card_colors = load_card_colors('tests/EjemploCubo.csv')

# Obtiene los nombres de las cartas.
card_names = list(card_colors.keys())

# Parametriza el test para cada carta.
@pytest.mark.parametrize("card_name", card_names)
@allure.feature("Card Retrieval")
@allure.story("Get Specific Card")
def test_get_specific_card(api_client, card_name):

    #Verifica que la carta se puede recuperar por nombre y guarda la imagen en PNG.
    # Llama a la API para obtener la carta.
    response_data = api_client.get_card_by_name(card_name)

    # Verifica los campos necesarios en la respuesta.
    assert "name" in response_data
    assert "image_uris" in response_data
    assert "png" in response_data["image_uris"]

    # Obtiene la URL de la imagen PNG.
    image_url = response_data["image_uris"]["png"]
    
    # Recupera la categoría de color de la carta.
    color_category = card_colors.get(card_name, "unknown")

    # Guarda y adjunta la imagen al reporte de Allure.
    image_path = save_card_image(card_name, image_url, color_category)
    if image_path:
        allure.attach.file(image_path, name=f"Imagen de {card_name}", attachment_type=allure.attachment_type.PNG)