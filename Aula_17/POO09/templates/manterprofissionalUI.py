import streamlit as st
from views import View

class ManterProfissionalUI:
    @staticmethod
    def main():
        st.title("Cadastro de Profissionais")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])

        with tab1:
            ManterProfissionalUI.listar()
        with tab2:
            ManterProfissionalUI.inserir()
        with tab3:
            ManterProfissionalUI.atualizar()
        with tab4:
            ManterProfissionalUI.excluir()

    @staticmethod
    def listar():
        profissionais = View.profissional_listar()
        if not profissionais:
            st.info("Nenhum profissional cadastrado ainda.")
            return

        dados = [{
            "ID": p.get_id(),
            "Nome": p.get_nome(),
            "Especialidade": p.get_especialidade(),
            "Conselho": p.get_conselho(),
            "Email": p.get_email()
        } for p in profissionais]

        st.dataframe(dados, use_container_width=True)

    @staticmethod
    def inserir():
        nome = st.text_input("Nome")
        especialidade = st.text_input("Especialidade")
        conselho = st.text_input("Conselho Profissional")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        if st.button("Inserir Profissional"):
            if nome and especialidade and conselho and email and senha:
                View.profissional_inserir(nome, especialidade, conselho, email, senha)
                st.success("Profissional inserido com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha todos os campos antes de inserir.")

    @staticmethod
    def atualizar():
        profissionais = View.profissional_listar()
        if not profissionais:
            st.warning("Nenhum profissional cadastrado.")
            return

        opcao = st.selectbox("Selecione o profissional:", [f"{p.get_id()} - {p.get_nome()}" for p in profissionais])
        id = int(opcao.split(" - ")[0])
        p = View.profissional_listar_id(id)

        nome = st.text_input("Novo nome", value=p.get_nome())
        especialidade = st.text_input("Nova especialidade", value=p.get_especialidade())
        conselho = st.text_input("Novo conselho", value=p.get_conselho())
        email = st.text_input("Novo e-mail", value=p.get_email())
        senha = st.text_input("Nova senha", value=p.get_senha(), type="password")

        if st.button("Atualizar Profissional"):
            View.profissional_atualizar(id, nome, especialidade, conselho, email, senha)
            st.success("Profissional atualizado com sucesso!")
            st.rerun()

    @staticmethod
    def excluir():
        profissionais = View.profissional_listar()
        if not profissionais:
            st.warning("Nenhum profissional cadastrado.")
            return

        opcao = st.selectbox("Selecione o profissional para excluir:", [f"{p.get_id()} - {p.get_nome()}" for p in profissionais])
        id = int(opcao.split(" - ")[0])

        if st.button("Excluir Profissional"):
            View.profissional_excluir(id)
            st.success("Profissional excluído com sucesso!")
            st.rerun()
