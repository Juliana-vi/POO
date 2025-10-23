import streamlit as st
from views import View
from datetime import datetime, timedelta

class PerfilProfissionalUI:
    @staticmethod
    def main():
        id_profissional = st.session_state["usuario_id"]
        nome = st.session_state["usuario_nome"]

        st.title(f"Perfil do Profissional - {nome}")

        menu = st.selectbox("Selecione uma opção:", [
            "Abrir Agenda",
            "Visualizar Agenda",
            "Confirmar Serviço",
            "Alterar Senha"
        ])

        if menu == "Abrir Agenda":
            st.subheader("Abrir Minha Agenda")
            st.write("Informe a data e os horários de atendimento que deseja disponibilizar:")

            data = st.date_input("Informe a data no formato dd/mm/aaaa")
            hora_inicial = st.time_input("Informe o horário inicial no formato HH:MM")
            hora_final = st.time_input("Informe o horário final no formato HH:MM")
            intervalo = st.number_input(
                "Informe o intervalo entre os horários (min)",
                min_value=10, max_value=180, value=30, step=5
            )

            if st.button("Abrir Agenda"):
                inicio = datetime.combine(data, hora_inicial)
                fim = datetime.combine(data, hora_final)

                if inicio >= fim:
                    st.error("O horário inicial deve ser anterior ao horário final.")
                else:
                    atual = inicio
                    count = 0
                    while atual < fim:
                        View.horario_inserir(atual, False, None, None, id_profissional)
                        atual += timedelta(minutes=intervalo)
                        count += 1
                    st.success(f"Agenda aberta com sucesso! {count} horários foram gerados para o dia {data.strftime('%d/%m/%Y')}.")

        elif menu == "Visualizar Agenda":
            st.subheader("Minha Agenda")
            horarios = View.filtrar_horarios_profissional(id_profissional)

            if not horarios:
                st.info("Nenhum horário cadastrado.")
            else:
                tabela = []
                for h in horarios:
                    cliente = View.cliente_listar_id(h.get_id_cliente())
                    servico = View.servico_listar_id(h.get_id_servico())
                    tabela.append({
                        "id": h.get_id(),
                        "data": h.get_data().strftime("%Y-%m-%d %H:%M:%S"),
                        "confirmado": "✅" if h.get_confirmado() else "☐",
                        "cliente": cliente.get_nome() if cliente else "None",
                        "serviço": servico.get_descricao() if servico else "None"
                    })
                st.dataframe(tabela, use_container_width=True)

        elif menu == "Confirmar Serviço":
            st.subheader("✅ Confirmar Serviço")
            horarios = [h for h in View.filtrar_horarios_profissional(id_profissional) if h.get_id_cliente()]

            if not horarios:
                st.info("Nenhum serviço pendente de confirmação.")
            else:
                op = st.selectbox(
                    "Informe o horário",
                    [f"{h.get_id()} - {h.get_data().strftime('%d/%m/%Y %H:%M')} - {h.get_confirmado()}" for h in horarios]
                )

                id_horario = int(op.split(" - ")[0])
                h = View.horario_listar_id(id_horario)

                clientes = View.cliente_listar()
                cliente_vinc = None
                for c in clientes:
                    if c.get_id() == h.get_id_cliente():
                        cliente_vinc = c
                        break

                if cliente_vinc:
                    st.selectbox(
                        "Cliente",
                        [f"{cliente_vinc.get_id()} - {cliente_vinc.get_email()} - {cliente_vinc.get_fone()}"],
                        disabled=True
                    )

                if st.button("Confirmar"):
                    View.confirmar_servico_profissional(id_horario)
                    st.success("Serviço confirmado com sucesso!")
                    st.rerun()

        elif menu == "Alterar Senha":
            st.subheader("Alterar Senha")
            nova = st.text_input("Digite a nova senha", type="password")
            if st.button("Salvar"):
                if View.alterar_senha(id_profissional, nova, "p"):
                    st.success("Senha alterada com sucesso!")
                else:
                    st.error("Erro ao alterar senha.")
