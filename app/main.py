from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import json

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

class Message(BaseModel):
    user_message: str

# Cargar respuestas desde un archivo externo
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

# Procesamiento de mensajes
def process_message(message: str) -> str:
    message_lower = message.lower()
    for key, response in RESPUESTAS.items():
        if key in message_lower:
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
