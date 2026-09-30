from app.repositories.login_repository import LoginRepository
from app.models.login_model import UserNexus

class LoginService:
    def __init__(self):
        self.repository = LoginRepository()

    def validar_usuario(self, dadosUsuario: UserNexus):
        if dadosUsuario.username is None or dadosUsuario.password is None:
            ValueError("Dados do usuário é obrigatório.")
        dados_usuario = self.repository.dados_usuario(dadosUsuario)
        valido_user = self.repository.validar_usuario(dadosUsuario)



        if not valido_user and not dados_usuario:
            return False

        if valido_user is False:
            return valido_user

        dados_usuario = dados_usuario[0]
        return {"empresa_id": dados_usuario['empresa_id'],
                "usuario_id": dados_usuario['id'],
                "nome": dados_usuario['nome'],
                "email": dados_usuario['email']
                }

        #self.repository.validar_usuario(dadosUsuario)

if __name__ =='__main__':
    repository = LoginService()

    body_user = UserNexus(
        username="vitor.pereira@nexuscrm.com.br",
        password="123456"
    )
    print(repository.validar_usuario(body_user))