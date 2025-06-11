 # Funciones para calcular KPIs

import pandas as pd
from db import db

def cargar_csv_en_mongo(nombre_archivo: str, nombre_coleccion: str):
    df = pd.read_csv(nombre_archivo)
    data = df.to_dict(orient="records")
    db[nombre_coleccion].delete_many({})  # Limpia antes de insertar nuevos
    db[nombre_coleccion].insert_many(data)
    return f"{len(data)} registros insertados en {nombre_coleccion}"
