import datetime

from app.repositories.base_repository import BaseRepository
from app.models.agendamento_model import CadastroAgendamento, ListaAgenda

class AgendamentoRepository(BaseRepository):
    def consulta_agendamentos(self,
                              empresa_id,
                              page_size,
                              offset
                              ):
        query = """
            SELECT 
                agd.id,
                to_char(
                    ag.data_inicio AT TIME ZONE 'America/Sao_Paulo',
                    'DD/MM/YYYY'
                ) AS data_inicio,
                to_char(
                    ag.data_inicio AT TIME ZONE 'America/Sao_Paulo',
                    'HH24:MI'
                ) AS hora_inicio,
                to_char(
                    ag.data_fim AT TIME ZONE 'America/Sao_Paulo',
                    'DD/MM/YYYY'
                ) AS data_fim,
                to_char(
                    ag.data_fim AT TIME ZONE 'America/Sao_Paulo',
                    'HH24:MI'
                ) AS hora_fim,
                ta.nome AS tipo_agenda,
                ct.nome AS nome_cliente,
                ct.telefone AS telefone_cliente,
                ct.email AS email_cliente
            FROM public.agendamentos agd
            JOIN public.agenda ag 
                ON ag.id = agd.agenda_id
            JOIN public.tipos_agendamento ta 
                ON ta.id = ag.tipo_agendamento_id 
            JOIN public.contatos ct 
                ON ct.id = agd.cliente_id
            where 1=1
            and AGD.empresa_id = %s
            order by
                ag.data_inicio DESC,
                ct.nome ASC
            limit %s
            OFFSET %s
        """

        return self.execute_query(
            query,
            (
                empresa_id,
                page_size,
                offset
            )
        )

    def consulta_agenda(
                        self,
                        empresa_id: str,
                        data_inicio: datetime.date,
                        data_final: datetime.date
                ):
        query = """
                    select 
                        ag.id as agenda_id,
                        tag.nome as tipo_agendamento,
                        to_char(
                            ag.data_inicio AT TIME ZONE 'America/Sao_Paulo',
                            'DD/MM/YYYY'
                        ) AS data_inicio,
                        to_char(
                            ag.data_inicio AT TIME ZONE 'America/Sao_Paulo',
                            'HH24:MI'
                        ) AS hora_inicio,
                        to_char(
                            ag.data_fim AT TIME ZONE 'America/Sao_Paulo',
                            'DD/MM/YYYY'
                        ) AS data_fim,
                        to_char(
                            ag.data_fim AT TIME ZONE 'America/Sao_Paulo',
                            'HH24:MI'
                        ) AS hora_fim,
                        ag.livre
                    from public.agenda ag 
                    join public.tipos_agendamento tag 
                    on tag.id = ag.tipo_agendamento_id
                    where 1=1
                    and ag.empresa_id = %s
                    AND (ag.data_inicio AT TIME ZONE 'America/Sao_Paulo')::date
                      BETWEEN %s AND %s
                """

        return self.execute_query(query, (empresa_id,
                                          data_inicio,
                                          data_final,
                                          ))

    def inserir_agendamento(self, dagendamento: CadastroAgendamento):
        query = """
            select public.criar_agendamento_contato(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
            )
        """

        return self.execute_query(query, (
                                  dagendamento.empresa_id,
                                  dagendamento.usuario_responsavel_id,
                                  dagendamento.agenda_id,
                                  dagendamento.status_agendamento_id,
                                  dagendamento.cliente_contato_id,
                                  dagendamento.nome_contato,
                                  dagendamento.telefone_contato,
                                  dagendamento.email_contato,
                                  dagendamento.cpf_cnpj_contato,
                                  dagendamento.empresa_nome_contato,
                                  dagendamento.observacao_contato,
                                  dagendamento.e_contato_novo,
                                  dagendamento.lembrete,
                                  dagendamento.observacao_agendamento,
                                  )
                                )

    def atualizar_agendamento(self):
        pass