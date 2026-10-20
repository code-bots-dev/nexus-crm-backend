import json
from app.repositories.base_repository import BaseRepository
from app.models.postagem_model import PostagemInsert

class PostagemRepository(BaseRepository):
    def retorna_postagens(self,
                          empresa_id: str,
                          usuario_id: str | None = None,
                          tipo_postagem: str | None = None,
                          categoria: str | None = None,
                          ativo: bool | None = None):
        query = """
            select id as postagem_id,
                   tipo_postagem, 
                   data_postagem, 
                   data_validade, 
                   url_postagem, 
                   descricao, 
                   ativo, 
                   categoria
            from public.postagens
            where 1=1
            and empresa_id = %s
        """
        params = [empresa_id]

        if usuario_id:
            query += " and usuario_id = %s"
            params.append(usuario_id)

        if tipo_postagem:
            query += " and tipo_postagem = %s"
            params.append(tipo_postagem)

        if categoria:
            query += " and categoria = %s"
            params.append(categoria)

        if ativo is not None:
            query += " and ativo = %s"
            params.append(ativo)

        query += " order by data_postagem desc"

        registros = self.execute_query(query, tuple(params))

        if registros:
            for item in registros:
                # Tenta converter descricao de string JSON para dicionário/objeto caso esteja armazenado como JSON
                if isinstance(item.get("descricao"), str):
                    try:
                        item["descricao"] = json.loads(item["descricao"])
                    except (json.JSONDecodeError, TypeError):
                        pass

        return registros or []

    def inserir_postagem(self, postagem: PostagemInsert):
        descricao_formatada = postagem.descricao
        if isinstance(descricao_formatada, (dict, list)):
            descricao_formatada = json.dumps(descricao_formatada, ensure_ascii=False)

        query = """
            insert into public.postagens (
                empresa_id,
                usuario_id,
                tipo_postagem,
                data_postagem,
                data_validade,
                url_postagem,
                descricao,
                ativo,
                categoria
            ) values (%s, %s, %s, coalesce(%s, now()), %s, %s, %s, coalesce(%s, true), %s)
            returning id as postagem_id
        """
        params = (
            postagem.empresa_id,
            postagem.usuario_id,
            postagem.tipo_postagem,
            postagem.data_postagem,
            postagem.data_validade,
            postagem.url_postagem,
            descricao_formatada,
            postagem.ativo,
            postagem.categoria
        )
        return self.execute_query(query, params)
