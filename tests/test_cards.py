import pytest
from conftest import load_card_colors, save_card_image
import allure

card_colors = load_card_colors('tests/ThePauperCube.csv')
card_names = list(card_colors.keys())

@pytest.mark.parametrize("card_name", card_names)
@allure.feature("Card Retrieval")
@allure.story("Get Specific Card")
def test_get_specific_card(api_client, card_name, request):
    """Prueba que obtiene una carta específica por nombre y guarda la imagen en PNG."""
    response_data = api_client.get_card_by_name(card_name)

    assert "name" in response_data, f"El campo 'name' no está presente en la respuesta de {card_name}"
    assert "image_uris" in response_data, f"El campo 'image_uris' no está presente en la respuesta de {card_name}"
    assert "png" in response_data["image_uris"], f"La imagen PNG no está disponible para {card_name}"

    image_url = response_data["image_uris"]["png"]
    
    # Obtener la categoría de color desde el archivo CSV
    color_category = card_colors.get(card_name, "unknown")  # Usamos "unknown" si no se encuentra el color

    image_path = save_card_image(card_name, image_url, color_category)

    if image_path:
        allure.attach.file(image_path, name=f"Imagen de {card_name}", attachment_type=allure.attachment_type.PNG)
