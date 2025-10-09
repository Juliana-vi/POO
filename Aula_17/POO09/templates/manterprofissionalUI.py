import streamlit as st
from models.profissional import Profissional, ProfissionalDAO
from views import View

def main():
    st.title("Cadastro de Profissionais")
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
    with tab1:
        profissionais = View.profissional_listar()
        st.write("Profissionais cadastrados:")
        for p in profissionais:
            st.write(p)
    with tab2:
        nome = st.text_input("Nome")
        especialidade = st.text_input("Especialidade")
        conselho = st.text_input("Conselho")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        if st.button("Inserir"):
            View.profissional_inserir(nome, especialidade, conselho, email, senha)
            st.success("Profissional inserido com sucesso!")
    with tab3:
        profissionais = View.profissional_listar()
        op = st.selectbox("Selecione o profissional", profissionais)
        if op is not None:
            nome = st.text_input("Novo nome", op.get_nome())
            especialidade = st.text_input("Nova especialidade", op.get_especialidade())
            conselho = st.text_input("Novo conselho", op.get_conselho())
            email = st.text_input("Novo e-mail", op.get_email())
            senha = st.text_input("Nova senha", op.get_senha(), type="password")
            if st.button("Atualizar"):
                View.profissional_atualizar(op.get_id(), nome, especialidade, conselho, email, senha)
                st.success("Profissional atualizado com sucesso!")
        else:
            st.info("Selecione um profissional para atualizar.")
    with tab4:
        profissionais = View.profissional_listar()
        op = st.selectbox("Selecione o profissional para excluir", profissionais)
        if st.button("Excluir"):
            View.profissional_excluir(op.get_id())
            st.success("Profissional excluído com sucesso!")

if __name__ == "__main__":
    main()
