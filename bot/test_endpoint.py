import requests
import base64


with open("../get-menu-script/images/menu.png", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')


url = "http://127.0.0.1:5000/api/upload_menu"
data = {"menu_base64": base64_image}
response = requests.post(url, json=data)

# Stampa la risposta grezza per debug
print("Status Code:", response.status_code)
print("Raw Response:", response.text)  # <-- Qui vediamo cosa arriva

# Prova a convertire in JSON solo se la risposta non è vuota
try:
    json_response = response.json()
    print("JSON Response:", json_response)
except requests.exceptions.JSONDecodeError:
    print("Errore: La risposta non è un JSON valido.")