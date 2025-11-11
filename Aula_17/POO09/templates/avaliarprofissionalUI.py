import streamlit as st
from views import View

class AvaliarProfissionalUI:
    @staticmethod
    def _try_rerun():
        """Tenta reiniciar/atualizar a execução de forma compatível com várias versões do Streamlit."""
        if hasattr(st, "experimental_rerun"):
            try:
                st.experimental_rerun()
                return
            except Exception:
                pass
        if hasattr(st, "rerun"):
            try:
                st.rerun()
                return
            except Exception:
                pass
        st.session_state["_needs_rerun"] = True

    @staticmethod
    def _get_prof_id_from_atd(atd):
        if hasattr(atd, "get_id_profissional"):
            return atd.get_id_profissional()
        if isinstance(atd, dict):
            return atd.get("id_profissional") or atd.get("id_prof")
        return None

    @staticmethod
    def _prof_get(field, prof):

        if prof is None:
            return None
        if hasattr(prof, field):
            try:
                return getattr(prof, field)() 
            except Exception:
                pass
        if hasattr(prof, f"get_{field}"):
            try:
                return getattr(prof, f"get_{field}")()
            except Exception:
                pass
        if isinstance(prof, dict):
            return prof.get(field) or prof.get(f"_{prof.__class__.__name__}__{field}")
        return None

    @staticmethod
    def main():
        st.header("Avaliar Profissional")

        if "usuario_id" not in st.session_state:
            st.info("Faça login para avaliar profissionais.")
            return

        id_cliente = st.session_state["usuario_id"]
        atendimentos = View.listar_atendimentos_cliente(id_cliente) or []

        if not atendimentos:
            st.info("Você ainda não teve nenhum atendimento para avaliar.")
            return

        prof_map = {}  
        for atd in atendimentos:
            pid = AvaliarProfissionalUI._get_prof_id_from_atd(atd)
            if pid is None:
                continue
            prof = View.profissional_listar_id(pid)
            if prof is None:
                continue
            prof_map[int(pid)] = prof

        if not prof_map:
            st.warning("Nenhum profissional válido encontrado nos seus atendimentos.")
            return

        labels = [f"{AvaliarProfissionalUI._prof_get('nome', p)} ({AvaliarProfissionalUI._prof_get('especialidade', p) or ''})" for p in prof_map.values()]
        ids = list(prof_map.keys())
        selection_index = st.selectbox("Selecione o profissional:", range(len(labels)), format_func=lambda i: labels[i])
        prof_id = ids[selection_index]
        prof = prof_map[prof_id]

        # verificar se já avaliou
        avals = []
        try:
            avals = prof.get_avaliacoes() if hasattr(prof, "get_avaliacoes") else (prof.get("avaliacoes") if isinstance(prof, dict) else [])
        except Exception:
            avals = []
        ja_avaliou = any((av.get("cliente_id") == id_cliente or av.get("id_cliente") == id_cliente) for av in (avals or []))

        st.subheader(f"Avaliar: {AvaliarProfissionalUI._prof_get('nome', prof)}")
        media = 0.0
        try:
            media = prof.get_media_avaliacoes() if hasattr(prof, "get_media_avaliacoes") else (float(prof.get("media", 0)) if isinstance(prof, dict) else 0.0)
        except Exception:
            media = 0.0
        st.caption(f"Média atual: ⭐ {media:.1f} ({len(avals or [])} avaliações)")

        if ja_avaliou:
            st.info("✅ Você já avaliou este profissional.")
            return

        nota = st.slider("Nota", 0.0, 5.0, 5.0, 0.5, key=f"nota_{prof_id}")
        comentario = st.text_area("Comentário", key=f"comentario_{prof_id}")

        if st.button("Enviar Avaliação"):
            if comentario is None or not comentario.strip():
                st.warning("Digite um comentário antes de enviar a avaliação.")
            else:
                sucesso = View.avaliar_profissional(prof_id, id_cliente, nota, comentario.strip())
                if sucesso:
                    st.success("Avaliação enviada com sucesso.")
                    AvaliarProfissionalUI._try_rerun()
                    return
                else:
                    avals_now = []
                    try:
                        p2 = View.profissional_listar_id(prof_id)
                        avals_now = p2.get_avaliacoes() if hasattr(p2, "get_avaliacoes") else (p2.get("avaliacoes") if isinstance(p2, dict) else [])
                    except Exception:
                        avals_now = []
                    if any((av.get("cliente_id") == id_cliente or av.get("id_cliente") == id_cliente) for av in (avals_now or [])):
                        st.info("Você já avaliou este profissional.")
                    else:
                        st.error("Erro ao enviar avaliação. Verifique se todos os dados estão corretos e tente novamente.")