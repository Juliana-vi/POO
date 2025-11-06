import streamlit as st
from views import View

class AvaliarProfissionalUI:
    @staticmethod
    def main():
        st.header("Avaliar Profissional")
        
        # Lista apenas os profissionais que já atenderam o cliente
        atendimentos = View.listar_atendimentos_cliente(st.session_state["usuario_id"])
        
        if not atendimentos:
            st.info("Você ainda não teve nenhum atendimento para avaliar.")
            return

        for atd in atendimentos:
            prof = View.profissional_listar_id(atd.get_id_profissional())
            if not prof:
                continue

            st.subheader(f"Avaliar: {prof.get_nome()}")
            
            # Verifica se já avaliou
            avaliacoes = prof.get_avaliacoes()
            if any(av["cliente_id"] == st.session_state["usuario_id"] for av in avaliacoes):
                st.info("Você já avaliou este profissional")
                continue

            nota = st.slider(f"Nota para {prof.get_nome()}", 0.0, 5.0, 5.0, 0.5)
            comentario = st.text_area(f"Comentário sobre {prof.get_nome()}")

            if st.button(f"Enviar Avaliação para {prof.get_nome()}"):
                View.avaliar_profissional(
                    prof.get_id(),
                    st.session_state["usuario_id"],
                    nota,
                    comentario
                )
                st.success("Avaliação enviada com sucesso!")
                st.rerun()