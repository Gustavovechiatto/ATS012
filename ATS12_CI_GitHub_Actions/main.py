from fastapi import FastAPI

app = FastAPI(title="API ATS12 - CI com GitHub Actions")


@app.get("/")
def inicio():
    return {"mensagem": "API funcionando"}


@app.get("/somar/{a}/{b}")
def somar(a: int, b: int):
    return {"resultado": a + b}


@app.get("/multiplicar/{a}/{b}")
def multiplicar(a: int, b: int):
    return {"resultado": a * b}
