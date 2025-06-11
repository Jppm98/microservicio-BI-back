# Conexión a MongoDB (conecta la app con la base de datos Mongo y deja disponible la variable db para usarla.)

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables desde .env

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
