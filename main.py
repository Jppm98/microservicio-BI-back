# App principal con GraphQL

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from schema import schema

# Crear app FastAPI
app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Frontend en Angular
    allow_credentials=True,
    allow_methods=["*"],  # Muy importante para aceptar OPTIONS
    allow_headers=["*"],
)

# Crear GraphQL router
graphql_app = GraphQLRouter(schema)

# Registrar endpoint de GraphQL
app.include_router(graphql_app, prefix="/graphql")

# Ejecutar servidor
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
