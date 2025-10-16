import streamlit as st
from views import View

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

        elif menu == "Meus Serviços":
            servicos = View.cliente_visualizar_servicos(id_cliente)
            if servicos:
                for s in servicos:
                    data = s.get_data()
                    profissional = View.profissional_listar_id(s.get_id_profissional())
                    nome_prof = profissional.get_nome() if profissional else "(desconhecido)"
                    status = "Confirmado" if s.get_confirmado() else "Pendente"
                    st.write(f"- {data} com {nome_prof} — {status}")
            else:
                st.info("Nenhum serviço agendado ainda.")

        elif menu == "Alterar Senha":
            nova = st.text_input("Digite a nova senha", type="password")
            if st.button("Salvar nova senha"):
                View.alterar_senha(id_cliente, nova, "c")
                st.success("Senha alterada com sucesso!")
