from app.repositories.base_repository import BaseRepository
from app.models.email_model import ConfiguracaoEmpresaModel

class EmailRepository(BaseRepository):

    def obter_empresa(self, empresa_id: str):
        query = """
            SELECT 
                id,
                nome,
                nome_fantasia,
                cnpj,
                email,
                telefone,
                logo_url
            FROM public.empresas
            WHERE id = %s::uuid
            LIMIT 1
        """
        resultado = self.execute_query(query, (empresa_id,))
        if resultado and len(resultado) > 0:
            return resultado[0]
        return None

    def obter_configuracao_empresa(self, empresa_id: str):
        query = """
            SELECT 
                id,
                empresa_id,
                key_api,
                data_inicio,
                data_final,
                key_api_pagamento,
                data_inicio_pagamento,
                data_final_pagamento,
                url_servidor_smtp,
                porta_smtp,
                key_api_email_smtp,
                usuario_smtp,
                api_key_brevo
            FROM public.configuracao_empresa
            WHERE empresa_id = %s::uuid
            LIMIT 1
        """
        resultado = self.execute_query(query, (empresa_id,))
        if resultado and len(resultado) > 0:
            return resultado[0]
        return None

    def salvar_configuracao_empresa(self, config: ConfiguracaoEmpresaModel):
        config_existente = self.obter_configuracao_empresa(config.empresa_id)

        if config_existente:
            query = """
                UPDATE public.configuracao_empresa
                SET 
                    key_api = COALESCE(%s, key_api),
                    data_inicio = COALESCE(%s, data_inicio),
                    data_final = COALESCE(%s, data_final),
                    key_api_pagamento = COALESCE(%s, key_api_pagamento),
                    data_inicio_pagamento = COALESCE(%s, data_inicio_pagamento),
                    data_final_pagamento = COALESCE(%s, data_final_pagamento),
                    url_servidor_smtp = COALESCE(%s, url_servidor_smtp),
                    porta_smtp = COALESCE(%s, porta_smtp),
                    key_api_email_smtp = COALESCE(%s, key_api_email_smtp)
                WHERE empresa_id = %s::uuid
                RETURNING id;
            """
            return self.execute_query(
                query,
                (
                    config.key_api,
                    config.data_inicio,
                    config.data_final,
                    config.key_api_pagamento,
                    config.data_inicio_pagamento,
                    config.data_final_pagamento,
                    config.url_servidor_smtp,
                    config.porta_smtp,
                    config.key_api_email_smtp,
                    config.empresa_id
                )
            )
        else:
            query = """
                INSERT INTO public.configuracao_empresa (
                    empresa_id,
                    key_api,
                    data_inicio,
                    data_final,
                    key_api_pagamento,
                    data_inicio_pagamento,
                    data_final_pagamento,
                    url_servidor_smtp,
                    porta_smtp,
                    key_api_email_smtp
                ) VALUES (
                    %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id;
            """
            return self.execute_query(
                query,
                (
                    config.empresa_id,
                    config.key_api,
                    config.data_inicio,
                    config.data_final,
                    config.key_api_pagamento,
                    config.data_inicio_pagamento,
                    config.data_final_pagamento,
                    config.url_servidor_smtp,
                    config.porta_smtp,
                    config.key_api_email_smtp
                )
            )
