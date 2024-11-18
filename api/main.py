from fastapi import FastAPI
from .routes.procedure import router as chat_router
from .routes.atendimento_proximo import router as atendimento_proximo_router
from .routes.direcionador_investimento import router as direcionador_investimento_router


app = FastAPI()

app.include_router(chat_router)
app.include_router(atendimento_proximo_router)
app.include_router(direcionador_investimento_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}