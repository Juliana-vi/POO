import streamlit as st
from views import View

class AvaliarProfissionalUI:
    @staticmethod
    def main():
        st.header("Avaliar Profissional")
        
        id_cliente = st.session_state["usuario_id"]
        atendimentos = View.listar_atendimentos_cliente(id_cliente)
        
        if not atendimentos:
            st.info("Você ainda não teve nenhum atendimento para avaliar.")
            return
        
        # Evita repetições de profissionais
        profissionais_avaliados = set()

        for atd in atendimentos:
          prof = View.profissional_listar_id(atd.get_id_profissional())
          if not prof or prof.get_id() in profissionais_avaliados:
           continue  # Pula se já mostrou esse profissional

          profissionais_avaliados.add(prof.get_id())

          st.subheader(f"Avaliar: {prof.get_nome()} ({prof.get_especialidade()})")

          avaliacoes = prof.get_avaliacoes()
          ja_avaliou = any(av["cliente_id"] == id_cliente for av in avaliacoes)

          if ja_avaliou:
                st.info(f"✅ Você já avaliou este profissional.")
                st.caption(f"Média atual: ⭐ {prof.get_media_avaliacoes():.1f} ({len(avaliacoes)} avaliações)")
                continue

        # 🔑 Garantindo chaves únicas para cada atendimento do profissional
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
        
        sucesso = False

        if st.button(f"Enviar Avaliação para {prof.get_nome()}", key=f"{key_base}_btn"):
              sucesso = View.avaliar_profissional(
                prof.get_id(),
                id_cliente,
                nota,
                comentario
                )

        if sucesso:
                # Recarrega o objeto atualizado
                prof_atualizado = View.profissional_listar_id(prof.get_id())
                media = prof_atualizado.get_media_avaliacoes()
                qtd = len(prof_atualizado.get_avaliacoes())

                st.success(
                        f"Avaliação enviada com sucesso! "
                        f"⭐ Média atual: **{media:.1f}** ({qtd} avaliações)."
                    )
                st.rerun()
        else:
                 st.error("Erro ao enviar avaliação. Tente novamente.")
