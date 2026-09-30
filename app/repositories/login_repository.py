from app.repositories.base_repository import BaseRepository
from app.models.login_model import UserNexus
import bcrypt

class LoginRepository(BaseRepository):
    def dados_usuario(self, dUsuario: UserNexus):
        query = """
                    select * 
                    from public.usuarios
                    where 1=1
                    and email = %s
                """
        vUser = self.execute_query(
            query,
            (dUsuario.username,)
        )
        if not vUser:
            return False
        usuario = vUser[0]
        return vUser

    def validar_usuario(self, dUsuario: UserNexus):
        query = """
            SELECT
                id,
                email,
                encrypted_password
            FROM AUTH.USERS
            WHERE email = %s
        """

        vUser = self.execute_query(
            query,
            (dUsuario.username,)
        )
        if not vUser:
            return False
        usuario = vUser[0]
        senha_hash = usuario["encrypted_password"]

        return bcrypt.checkpw(
            dUsuario.password.encode("utf-8"),
            senha_hash.encode("utf-8")
        )

if __name__=='__main__':
    repository = LoginRepository()

    body_user = UserNexus(
        username="vitor.pereira@nexuscrm.com.br",
        password="123456"
    )
    print(repository.validar_usuario(body_user))
    print(repository.dados_usuario(body_user))