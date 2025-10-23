import streamlit as st
from views import View
from datetime import date

class PerfilClienteUI:
    @staticmethod
    def main():
        id_cliente = st.session_state["usuario_id"]
        nome = st.session_state["usuario_nome"]

        st.title(f"Perfil do Cliente - {nome}")

        menu = st.selectbox("Selecione uma opção:", [
            "Meus Dados",
            "Meus Serviços",
            "Alterar Senha"
        ])

        if menu == "Meus Dados":
            c = View.cliente_listar_id(id_cliente)
            st.write(f"**Nome:** {c.get_nome()}")
            st.write(f"**E-mail:** {c.get_email()}")
            st.write(f"**Telefone:** {c.get_fone()}")

        if menu == "Meus Serviços":
            st.subheader("Meus Serviços")

            horarios = View.filtrar_horarios_cliente(id_cliente)

            if not horarios:
                st.info("Nenhum serviço agendado encontrado.")
            else:
                tabela = []
                for h in horarios:
                    servico = View.servico_listar_id(h.get_id_servico())
                    profissional = View.profissional_listar_id(h.get_id_profissional())
                    tabela.append({
                        "id": h.get_id(),
                        "data": h.get_data().strftime("%Y-%m-%d %H:%M:%S"),
                        "confirmado": "✅" if h.get_confirmado() else "☐",
                        "serviço": servico.get_descricao() if servico else "None",
                        "profissional": profissional.get_nome() if profissional else "None"
                    })
                st.dataframe(tabela, use_container_width=True)

        elif menu == "Alterar Senha":
            st.subheader("Alterar Senha")
            nova = st.text_input("Digite a nova senha", type="password")
            if st.button("Salvar"):
                if View.alterar_senha(id_cliente, nova, "c"):
                    st.success("Senha alterada com sucesso!")
                else:
                    st.error("Erro ao alterar senha.")