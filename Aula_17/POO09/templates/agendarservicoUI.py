import streamlit as st
from views import View

class AgendarServicoUI:
    @staticmethod
    def main():
        st.title("Agendar Serviço")

        id_cliente = st.session_state["usuario_id"]

        # ============= SERVIÇOS DISPONÍVEIS =============
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

        # ============= PROFISSIONAIS DISPONÍVEIS =============
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

        # ============= MOSTRAR AVALIAÇÕES DO PROFISSIONAL =============
        st.markdown("---")
        st.subheader(f"Avaliações de {profissional.get_nome()} ⭐")

        avaliacoes = profissional.get_avaliacoes()
        media = profissional.get_media_avaliacoes()
        total = len(avaliacoes)

        if not avaliacoes:
            st.info("Este profissional ainda não recebeu avaliações.")
        else:
            st.markdown(f"**Média geral:** ⭐ {media:.1f} ({total} avaliações)")
            st.caption("Os comentários são anônimos para preservar a privacidade dos clientes.")
            st.divider()

            for i, av in enumerate(sorted(avaliacoes, key=lambda x: -x["nota"]), start=1):
                st.markdown(
                    f"**Cliente Anônimo #{i}** — ⭐ **{av['nota']:.1f}**  \n"
                    f"💬 *{av['comentario']}*"
                )
                st.markdown("---")

        # ============= HORÁRIOS DISPONÍVEIS =============
        horarios = [
            h for h in View.profissional_visualizar_agenda(id_profissional)
            if h.get_id_cliente() in (None, 0)
        ]

        if not horarios:
            st.info("Nenhum horário livre disponível para este profissional.")
            return

        op_horario = st.selectbox(
            "Escolha o horário disponível:",
            [f"{h.get_id()} - {h.get_data()}" for h in horarios]
        )
        id_horario = int(op_horario.split(" - ")[0])

        # ============= AGENDAR =============
        if st.button("Confirmar Agendamento"):
            h = View.horario_listar_id(id_horario)
            if not h:
                st.error("Erro ao localizar horário.")
                return

            h.set_id_cliente(id_cliente)
            h.set_id_servico(id_servico)
            h.set_confirmado(False)

            View.horario_atualizar(
                h.get_id(),
                h.get_data(),
                h.get_confirmado(),
                h.get_id_cliente(),
                h.get_id_servico(),
                h.get_id_profissional()
            )

            st.success(
                f"Serviço '{servico.get_descricao()}' agendado com {profissional.get_nome()} "
                f"em {h.get_data().strftime('%d/%m/%Y %H:%M')}."
            )
            st.balloons()