from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Carga variables de entorno
load_dotenv()

app = FastAPI()

class Message(BaseModel):
    user_message: str

# Lógica simple de chatbot (modifica según necesidades)
def process_message(message: str) -> str:
    default_response = "Hola! Soy el chatbot de Destored. ¿En qué puedo ayudarte?"
    
    # Ejemplo: Detectar palabras clave
    if "producto" in message.lower():
        return "Tenemos una amplia gama de productos digitales. Visita https://www.destored.org/tienda"
    elif "contacto" in message.lower():
        return "Puedes contactarnos en contacto@destored.org"
    
    return default_response

@app.post("/chat")
async def chat_endpoint(message: Message):
    try:
        bot_response = process_message(message.user_message)
        return {"response": bot_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))