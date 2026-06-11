import base64
import os
import io
import time
import openai
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import stream, BadRequestError, UnauthorizedError, ForbiddenError
from dotenv import load_dotenv
from picamera2 import Picamera2

load_dotenv()
cliente = OpenAI()
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)


def text_to_speech(elevenlabs, name):
    if name is None:
        name = "No reconocí el objeto"

    try:
        audio_stream = elevenlabs.text_to_speech.stream(
            text = name,
            voice_id = 'YPQYiDk4YwegwaZcMMWE',
            model = 'eleven_multilingual_v2',
        )

        stream(audio_stream)
        return f'Audio finalizado'
    except BadRequestError as e:
        return f' [-] Error en la solciitud (400): {e}'
    except UnauthorizedError:
        return f' [-] Error de autenticación (401): API Key Inválida'
    except ForbiddenError:
        return f' [-] Acceso denegado (403): Verifica tu plan o permisos de la voz'

def capture_image():
    stream = io.BytesIO()
    try:
        with Picamera2() as camera:
            camera.resolution = (1024,768)
            time.sleep(2)
            camera.capture(stream, format='jpeg')
        stream.seek(0)
        return stream
    
    except Exception as e:
        print(f'Error en la cámara\n [-] {e}')
        return None
    
def encode_image(stream):
    if stream is None:
        return None
    
    return base64.b64encode(stream.read()).decode('utf-8')

def obtener_nombre(base64_image):
    if base64_image is None:
        return None

    try:
        responses = cliente.chat.completions.create(
            model='gpt-4o-mini',
            messages = [
                {
                    'role':'user',
                    'content': [
                        {'type':'text', 'text': 'Identifica el nombre del objeto de la imagen y devuelve el siguiente texto: <text>Objeto físico identificado [nombre del objeto]'},
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/jpeg;base64,{base64_image}'
                            }
                        }
                    ]
                }
            ],
            max_tokens=50,
        )
        return responses.choices[0].message.content
    except openai.APIError as e:
        print(f'OpenAI API devolvió un error:\n [-]{e}')
        return None
    except openai.APIConnectionError as e:
        print(f'OpenAI API tuvo un error de conexión:\n [-]{e}')
        return None
    except openai.RateLimitError as e:
        print(f'Tu cuota de la API de OpenAI se excedió\n [-]{e}')
        return None

if __name__ == '__main__':
    image = capture_image()

    if image:
        image_base64 = encode_image(image)
        if image_base64:
            nombre = obtener_nombre(image_base64)
            if nombre:
                text_to_speech(elevenlabs, nombre)