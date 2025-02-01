from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import json
from fastapi.middleware.cors import CORSMiddleware
import re

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Crear la app FastAPI
app = FastAPI()

# Agregar middleware de CORS
origins = [
    "https://www.destored.org",  # Permitimos solicitudes desde www.destored.org
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes desde los orígenes especificados
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Clase Pydantic para el mensaje del usuario
class Message(BaseModel):
    user_message: str

# Ruta del archivo de respuestas
RESPUESTAS_FILE = "respuestas.json"

def cargar_respuestas():
    try:
        with open(RESPUESTAS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Archivo de respuestas no encontrado.")
        return {}

RESPUESTAS = cargar_respuestas()

DEFAULT_RESPONSE = "Hola! Soy el chatbot de Destored. ¿En qué puedo ayudarte?"

# Función para procesar los mensajes
def process_message(message: str) -> str:
    message_lower = message.lower()
    for key, response in RESPUESTAS.items():
        if re.search(key, message_lower):  # Usa búsqueda por patrones
            return response
    return DEFAULT_RESPONSE

@app.post("/chat")
async def chat_endpoint(message: Message):
    try:
        user_input = message.user_message
        bot_response = process_message(user_input)
        logging.info(f"Usuario: {user_input} | Bot: {bot_response}")
        return {"response": bot_response}
    except Exception as e:
        logging.error(f"Error en chatbot: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocurrió un error en el chatbot.")
