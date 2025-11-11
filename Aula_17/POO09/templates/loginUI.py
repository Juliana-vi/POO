import streamlit as st
from views import View

class LoginUI:
    @staticmethod
    def cliente():
        st.title("Login - Cliente")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user = View.cliente_autenticar(email, senha)
            if user:
                if hasattr(user, "get_id"):
                    uid = user.get_id()
                    uname = user.get_nome() if hasattr(user, "get_nome") else getattr(user, "nome", "")
                    utype = "c"
                else:
                    uid = int(user.get("id", 0))
                    uname = user.get("nome", "")
                    utype = user.get("tipo", "c")

                try:
                    st.session_state["usuario_id"] = int(uid)
                except Exception:
                    st.session_state["usuario_id"] = uid
                st.session_state["usuario_nome"] = uname
                st.session_state["usuario_tipo"] = utype
                st.success("Login realizado!")
                if hasattr(st, "rerun"):
                    st.rerun()
                elif hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
            else:
                st.error("Credenciais inválidas.")

    @staticmethod
    def profissional():
        st.title("Login - Profissional")
        email = st.text_input("Email", key="p_email")
        senha = st.text_input("Senha", type="password", key="p_senha")
        if st.button("Entrar como Profissional"):
            profs = View.profissional_listar() or []
            user = next((p for p in profs if (p.get_email() if hasattr(p, "get_email") else p.get("email")) == email
                         and (p.get_senha() if hasattr(p, "get_senha") else p.get("senha")) == senha), None)
            if user:
                if hasattr(user, "get_id"):
                    st.session_state["usuario_id"] = user.get_id()
                    st.session_state["usuario_nome"] = user.get_nome() if hasattr(user, "get_nome") else getattr(user, "nome", "")
                else:
                    st.session_state["usuario_id"] = int(user.get("id", 0))
                    st.session_state["usuario_nome"] = user.get("nome", "")
                st.session_state["usuario_tipo"] = "p"
                st.success("Login realizado!")
                if hasattr(st, "rerun"):
                    st.rerun()
                elif hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
            else:
                st.error("Credenciais inválidas.")