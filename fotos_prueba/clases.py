import time
import os
from dotenv import load_dotenv
from prueba_camara import encode_image, obtener_nombre, text_to_speech
#Tengo que usar prueba_camera.py, luego main para probar con la camara real
from elevenlabs.client import ElevenLabs

load_dotenv()
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)

class Camara:
    def __init__(self, imagen):
        self.imagen = imagen

    def capturar(self):
        return self.imagen

class Pata:
    def __init__(self, id, angulo_hombro, min_hombro, max_hombro, angulo_rodilla, min_rodilla, max_rodilla):
        self.id = id
        self.angulo_hombro = angulo_hombro
        self.min_hombro = min_hombro
        self.max_hombro = max_hombro
        self.angulo_rodilla = angulo_rodilla
        self.min_rodilla = min_rodilla
        self.max_rodilla = max_rodilla

    def mover(self, angulo_hombro_nuevo, angulo_rodilla_nuevo):
        if angulo_hombro_nuevo < self.min_hombro or angulo_hombro_nuevo > self.max_hombro:
            print(f'[{self.id}] Hombro: ángulo {angulo_hombro_nuevo}º fuera de rango')
        else:
            self.angulo_hombro = angulo_hombro_nuevo
            print(f'[{self.id}] Hombro movido a {self.angulo_hombro}º')

        if angulo_rodilla_nuevo < self.min_rodilla or angulo_rodilla_nuevo > self.max_rodilla:
            print(f'[{self.id}] Rodilla: ángulo {angulo_rodilla_nuevo}º fuera de rango')
        else:
            self.angulo_rodilla = angulo_rodilla_nuevo
            print(f'[{self.id}] Rodilla movida a {self.angulo_rodilla}º')

    
class Robot:
    def __init__(self, camara, nombres=['delantera_izq','delantera_der','trasera_izq','trasera_der']):
        self.patas = [Pata(nombre, 0, 0, 90, 0, 0, 90) for nombre in nombres]
        self.camara = camara

    def caminar_id_pata(self, nombre, angulo1, angulo2):
        for x in self.patas:
            if x.id == nombre:
                x.mover(angulo1,angulo2)

    def trot(self):
        self.caminar_id_pata('delantera_der', 45, 60)
        self.caminar_id_pata('trasera_izq', 45, 60)
        time.sleep(1)
        self.caminar_id_pata('delantera_der', 0,0)
        self.caminar_id_pata('trasera_izq',0,0)
        time.sleep(1)
        self.caminar_id_pata('delantera_izq', 45, 60)
        self.caminar_id_pata('trasera_der', 45, 60)
        time.sleep(1)
        self.caminar_id_pata('delantera_izq', 0, 0)
        self.caminar_id_pata('trasera_der', 0, 0)

    def capturar_imagen(self):
        return self.camara.capturar()

camara = Camara('objeto2.jpeg')
robot = Robot(camara)

for _ in range(3):
    robot.trot()
    imagen = robot.capturar_imagen()
    image_base64 = encode_image(imagen)
    name = obtener_nombre(image_base64)
    hablar = text_to_speech(elevenlabs, name)

