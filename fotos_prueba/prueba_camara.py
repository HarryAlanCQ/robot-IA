import base64
import openai
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI()
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')

elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)

image_path = 'objeto1.jpeg'

def text_to_speech(elevenlabs, name):
    audio_stream = elevenlabs.text_to_speech.stream(
        text = name,
        voice_id = 'YPQYiDk4YwegwaZcMMWE',
        model_id = 'eleven_multilingual_v2',
    )

    stream(audio_stream)
    return 'Hablando...'

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')   
    
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
                        {'type':'text', 'text': 'Identifica el nombre del objeto de la imagen y devuelve el siguiente texto: <text>Objeto físico identificado [nombre del objeto]</text>'},
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
