import streamlit as st
from views import View

class AgendarServicoUI:
    @staticmethod
    def main():
        st.title("Agendar Serviço")

        id_cliente = st.session_state["usuario_id"]

        servicos = View.servico_listar()
        if not servicos:
            st.warning("Nenhum serviço disponível no momento.")
            return

        servico_opcao = st.selectbox(
            "Escolha o serviço:",
            [f"{s.get_id()} - {s.get_descricao()}" for s in servicos]
        )
        id_servico = int(servico_opcao.split(" - ")[0])
        servico = View.servico_listar_id(id_servico)

        profissionais = View.profissional_listar()
        if not profissionais:
            st.warning("Nenhum profissional cadastrado no momento.")
            return

        prof_opcao = st.selectbox(
            "Escolha o profissional:",
            [f"{p.get_id()} - {p.get_nome()}" for p in profissionais]
        )
        id_profissional = int(prof_opcao.split(" - ")[0])
        profissional = View.profissional_listar_id(id_profissional)

        horarios = [
            h for h in View.profissional_visualizar_agenda(id_profissional)
            if h.get_id_cliente() is None
        ]

        if not horarios:
            st.info("Nenhum horário livre disponível para este profissional.")
            return

        op_horario = st.selectbox(
            "Escolha o horário disponível:",
            [f"{h.get_id()} - {h.get_data()}" for h in horarios]
        )
        id_horario = int(op_horario.split(" - ")[0])

        if st.button("Confirmar Agendamento"):
            h = View.horario_listar_id(id_horario)
            if h is None:
                st.error("Erro ao localizar horário.")
                return

            h.set_id_cliente(id_cliente)
            h.set_id_servico(id_servico)
            View.horario_atualizar(
            h.get_id(),
            h.get_data(),
            True,  # confirmado = True
            st.session_state["usuario_id"],  # id_cliente logado
            h.get_id_servico(),
            h.get_id_profissional()
            )
            st.success(f"Serviço '{servico.get_descricao()}' agendado com {profissional.get_nome()} em {h.get_data()}")
