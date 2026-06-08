import base64
import os
import io
import time
import openai
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from dotenv import load_dotenv
#from picamera2 import Picamera2

load_dotenv()
cliente = OpenAI()
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)

def text_to_speech(elevenlabs, name):
    audio_stream = elevenlabs.text_to_speech.stream(
        text = name,
        voice_id = 'YPQYiDk4YwegwaZcMMWE',
        model = 'eleven_multilingual_v2',
    )

    stream(audio_stream)
    return f'Audio finalizado'

# def capture_image():
#     stream = io.BytesIO()
#     try:
#         with Picamera2() as camera:
#             camera.resolution = (1024,768)
#             time.sleep(2)
#             camera.capture(stream, format='jpeg')
#         stream.seek(0)
#         return stream
    
#     except Exception as e:
#         print(f'Error en la cámara\n [-] {e}')
#         return None
    
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
                        {'type':'text', 'text': """Identifica el nombre del objeto de la imagen y devuelve el siguiente texto si lo reconoce:
                         <text>Objeto reconocido: [nombre del objeto]</text>"""},
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
        return f'OpenAI API devolvió un error:\n [-]{e}'
    except openai.APIConnectionError as e:
        return f'OpenAI API tuvo un error de conexión:\n [-]{e}'
    except openai.RateLimitError as e:
        return f'Tu cuota de la API de OpenAI se excedió\n [-]{e}'

# image = capture_image()
image = None #Para prueba si es None

if image is None:
    print('Error: No se pudo capturar la imagen')
else:
    image_base64 = encode_image(image)
    name = obtener_nombre(image_base64)
    text_to_speech()