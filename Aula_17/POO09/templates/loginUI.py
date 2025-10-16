import streamlit as st
from views import View

class LoginUI:
    @staticmethod
    def cliente():
        st.title("Login - Cliente")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            # busca cliente por email
            clientes = View.cliente_listar()
            user = next((c for c in clientes if c.get_email() == email and c.get_senha() == senha), None)
            if user:
                st.session_state["usuario_id"] = user.get_id()
                st.session_state["usuario_nome"] = user.get_nome()
                st.session_state["usuario_tipo"] = "c"
                st.success("Login realizado!")
                st.rerun()
            else:
                st.error("Credenciais inválidas.")

    @staticmethod
    def profissional():
        st.title("Login - Profissional")
        email = st.text_input("Email", key="p_email")
        senha = st.text_input("Senha", type="password", key="p_senha")
        if st.button("Entrar como Profissional"):
            profs = View.profissional_listar()
            user = next((p for p in profs if p.get_email() == email and p.get_senha() == senha), None)
            if user:
                st.session_state["usuario_id"] = user.get_id()
                st.session_state["usuario_nome"] = user.get_nome()
                st.session_state["usuario_tipo"] = "p"
                st.success("Login realizado!")
                st.rerun()
            else:
                st.error("Credenciais inválidas.")