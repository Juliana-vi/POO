import streamlit as st
from paciente import Paciente

class PacienteUI:
    def main():
        st.header("Dados do Paciente")
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        fone = st.text_input("Fone")
        nasc = st.text_input("Nascimento")

        if st.button("Idade"):
            p = Paciente(nome, cpf, fone, nasc)
            st.write(p)
            st.write(p.calc_idade())