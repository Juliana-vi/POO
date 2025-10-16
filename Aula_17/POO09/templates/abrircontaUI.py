import streamlit as st
from views import View

class AbrirContaUI:
    @staticmethod
    def main():
        st.title("Abrir Conta")
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        fone = st.text_input("Fone")
        senha = st.text_input("Senha", type="password")

        if st.button("Criar Conta"):
            if not nome or not email or not senha:
                st.error("Nome, email e senha são obrigatórios.")
            else:
                View.cliente_inserir(nome, email, fone, senha)
                st.success("Conta criada com sucesso!")
                st.rerun()