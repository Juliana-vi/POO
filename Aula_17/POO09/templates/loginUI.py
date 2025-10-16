import streamlit as st
from views import View

class LoginUI:
    @staticmethod
    def cliente():
        st.header("Entrar como Cliente")
        email = st.text_input("Informe o e-mail", key="email_cliente")
        senha = st.text_input("Informe a senha", type="password", key="senha_cliente")

        if st.button("Entrar como Cliente"):
            c = View.cliente_autenticar(email, senha)
            if c is None:
                st.error("E-mail ou senha inválidos.")
            else:
                st.session_state["usuario_id"] = c["id"]
                st.session_state["usuario_nome"] = c["nome"]
                st.session_state["usuario_tipo"] = "c"
                st.success(f"Bem-vindo(a), {c['nome']}!")
                st.rerun()

    @staticmethod
    def profissional():
        st.header("Entrar como Profissional")
        email = st.text_input("Informe o e-mail", key="email_profissional")
        senha = st.text_input("Informe a senha", type="password", key="senha_profissional")

        if st.button("Entrar como Profissional"):
            p = View.profissional_autenticar(email, senha)
            if p is None:
                st.error("E-mail ou senha inválidos.")
            else:
                st.session_state["usuario_id"] = p["id"]
                st.session_state["usuario_nome"] = p["nome"]
                st.session_state["usuario_tipo"] = "p"
                st.success(f"Bem-vindo(a), {p['nome']}!")
                st.rerun()
