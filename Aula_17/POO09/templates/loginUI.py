import streamlit as st
from views import View

class LoginUI:
    def cliente():
        st.header("Entrar como Cliente")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")
        if st.button("Entrar"):
            c = View.cliente_autenticar(email, senha)
            if c == None: st.write("E-mail ou senha inválidos")
            else:
                st.session_state["usuario_id"] = c["id"]
                st.session_state["usuario_nome"] = c["nome"]
                st.session_state["usuario_tipo"] = c
                st.rerun()
    
    def profissional():
        st.header("Entrar como Profissional")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")
        if st.button("Entrar"):
            p = View.profissional_autenticar(email, senha)
            if p == None: st.write("E-mail ou senha inválidos")
            else:
                st.session_state["usuario_id"] = p["id"]
                st.session_state["usuario_nome"] = p["nome"]
                st.session_state["usuario_tipo"] = "p"
                st.rerun()