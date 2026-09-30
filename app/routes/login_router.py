from fastapi import HTTPException, APIRouter, Depends
from app.models.login_model import UserNexus
from app.services.login_service import LoginService
from components import tokenAcess

router = APIRouter(
    prefix="/v1/login",
    tags=["Login"]
)

service = LoginService()

@router.post("/")
def valida_usuario(dadosUser: UserNexus):
    dUser = service.validar_usuario(dadosUser)

    if not dUser:
        raise HTTPException(
            status_code=404,
            detail="Nenhum usuário encontrado."
        )
    else:
        token = tokenAcess.token.create_access_token(
            data={"sub": dadosUser.username
            }
        )

        return {"access_token": token,
                "empresa_id": dUser['empresa_id'],
                "usuario_id": dUser['usuario_id'],
                "user_name": dUser['nome'],
                "email_user": dUser['email'],
                "token_type": "bearer"
                }
    # return {
    #     "dados": dUser
    # }