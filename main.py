from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.produto_router import router as produto_router
from app.routes.login_router import router as login_router
from app.routes.cliente_route import router as cliente_router
from app.routes.permissao_router import router as permissao_router
from app.routes.lead_router import router as leads_router
from app.routes.venda_router import router as vendas_router
from app.routes.agendamento_router import router as agendamento_router
from app.routes.alertas_router import router as alerta_router
from app.routes.wppMensagem_router import router as wppMensagem_router
from app.routes.email_router import router as email_router
from app.routes.postagem_router import router as postagem_router
from app.routes.webhook_router import router as webhook_router

app = FastAPI(
    title="Nexus CRM API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "http://127.0.0.1:5502",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost:5501",
        "http://127.0.0.1:56529",
        "http://127.0.0.1:65361",
        "http://127.0.0.1:63731",
        "http://127.0.0.1:63774",
        "http://127.0.0.1:64556"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produto_router)
app.include_router(login_router)
app.include_router(cliente_router)
app.include_router(permissao_router)
app.include_router(leads_router)
app.include_router(vendas_router)
app.include_router(agendamento_router)
app.include_router(alerta_router)
app.include_router(wppMensagem_router)
app.include_router(email_router)
app.include_router(postagem_router)
app.include_router(webhook_router)

@app.get("/")
def home():
    return {
        "mensagem": "API Nexus CRM funcionando!"
    }