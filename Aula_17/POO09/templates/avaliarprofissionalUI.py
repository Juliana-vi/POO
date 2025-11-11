import streamlit as st
from views import View

class AvaliarProfissionalUI:
    @staticmethod
    def main():
        st.header("Avaliar Profissional")
        
        if "usuario_id" not in st.session_state:
            st.info("Faça login para avaliar profissionais.")
            return

        id_cliente = st.session_state["usuario_id"]
        atendimentos = View.listar_atendimentos_cliente(id_cliente)
        
        if not atendimentos:
            st.info("Você ainda não teve nenhum atendimento para avaliar.")
            return
        
        # Evita repetições de profissionais
        profissionais_mostrados = set()

        for atd in atendimentos:
            prof = View.profissional_listar_id(atd.get_id_profissional())
            if not prof:
                continue
            if prof.get_id() in profissionais_mostrados:
                continue  # já mostrado esse profissional
            profissionais_mostrados.add(prof.get_id())

            st.subheader(f"Avaliar: {prof.get_nome()} ({prof.get_especialidade()})")

            avaliacoes = prof.get_avaliacoes() or []
            # aceita chaves "cliente_id" ou "id_cliente"
            ja_avaliou = any(
                (av.get("cliente_id") == id_cliente) or (av.get("id_cliente") == id_cliente)
                for av in avaliacoes
            )

            st.caption(f"Média atual: ⭐ {prof.get_media_avaliacoes():.1f} ({len(avaliacoes)} avaliações)")

            if ja_avaliou:
                st.info("✅ Você já avaliou este profissional.")
                continue

            # chave única por profissional/atendimento
            key_base = f"prof_{prof.get_id()}_atd_{atd.get_id()}"

            nota = st.slider(
                f"Nota para {prof.get_nome()}",
                0.0, 5.0, 5.0, 0.5,
                key=f"{key_base}_nota"
            )
            comentario = st.text_area(
                f"Comentário sobre {prof.get_nome()}",
                key=f"{key_base}_comentario"
            )

            btn_key = f"{key_base}_btn"
            clicked = st.button(f"Enviar Avaliação para {prof.get_nome()}", key=btn_key)

            if clicked:
                sucesso = View.avaliar_profissional(
                    prof.get_id(),
                    id_cliente,
                    nota,
                    comentario
                )

                if sucesso:
                    prof_atualizado = View.profissional_listar_id(prof.get_id())
                    media = prof_atualizado.get_media_avaliacoes()
                    qtd = len(prof_atualizado.get_avaliacoes() or [])
                    st.success(
                        f"Avaliação enviada com sucesso! ⭐ Média atual: {media:.1f} ({qtd} avaliações)."
                    )
                    st.experimental_rerun()
                else:
                    st.error("Erro ao enviar avaliação. Tente novamente.")