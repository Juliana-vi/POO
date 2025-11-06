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
            "Minhas Avaliações ⭐",
            "Alterar Senha"
        ])

        # =============================
        # 📅 ABRIR AGENDA
        # =============================
        if menu == "Abrir Agenda":
            st.subheader("Abrir Minha Agenda")
            st.write("Informe a data e os horários de atendimento que deseja disponibilizar:")

            data = st.date_input("Informe a data no formato dd/mm/aaaa")
            hora_inicial = st.time_input("Horário inicial")
            hora_final = st.time_input("Horário final")
            intervalo = st.number_input(
                "Intervalo entre horários (min)",
                min_value=10, max_value=180, value=30, step=5
            )

            if st.button("Abrir Agenda"):
                try:
                    inicio = datetime.combine(data, hora_inicial)
                    fim = datetime.combine(data, hora_final)

                    if inicio >= fim:
                        st.error("O horário inicial deve ser anterior ao final.")
                    else:
                        atual = inicio
                        count = 0
                        while atual < fim:
                            View.horario_inserir(atual, False, None, None, id_profissional)
                            atual += timedelta(minutes=intervalo)
                            count += 1
                        st.success(f"Agenda aberta com sucesso! {count} horários criados para o dia {data.strftime('%d/%m/%Y')}.")
                except ValueError as e:
                    st.error(f"Erro: {e}")

        # =============================
        # 📋 VISUALIZAR AGENDA
        # =============================
        elif menu == "Visualizar Agenda":
            st.subheader("Minha Agenda")
            try:
                horarios = View.filtrar_horarios_profissional(id_profissional)
                if not horarios:
                    st.info("Nenhum horário cadastrado.")
                else:
                    tabela = []
                    for h in horarios:
                        cliente = View.cliente_listar_id(h.get_id_cliente())
                        servico = View.servico_listar_id(h.get_id_servico())
                        tabela.append({
                            "ID": h.get_id(),
                            "Data": h.get_data().strftime("%d/%m/%Y %H:%M"),
                            "Confirmado": "✅" if h.get_confirmado() else "☐",
                            "Cliente": cliente.get_nome() if cliente else "—",
                            "Serviço": servico.get_descricao() if servico else "—"
                        })
                    st.dataframe(tabela, use_container_width=True)
            except ValueError as e:
                st.error(f"Erro: {e}")

        # =============================
        # ✅ CONFIRMAR SERVIÇOS
        # =============================
        elif menu == "Confirmar Serviço":
            st.subheader("Confirmar Serviço")
            try:
                horarios = [h for h in View.filtrar_horarios_profissional(id_profissional) if h.get_id_cliente()]
                if not horarios:
                    st.info("Nenhum serviço pendente de confirmação.")
                else:
                    op = st.selectbox(
                        "Selecione o horário:",
                        [f"{h.get_id()} - {h.get_data().strftime('%d/%m/%Y %H:%M')} - {h.get_confirmado()}" for h in horarios]
                    )

                    id_horario = int(op.split(" - ")[0])
                    h = View.horario_listar_id(id_horario)

                    cliente = View.cliente_listar_id(h.get_id_cliente())
                    if cliente:
                        st.markdown(f"**Cliente:** {cliente.get_nome()}  \n**Email:** {cliente.get_email()}  \n**Fone:** {cliente.get_fone()}")

                    if st.button("Confirmar"):
                        try:
                            View.confirmar_servico_profissional(id_horario)
                            st.success("Serviço confirmado com sucesso!")
                            st.rerun()
                        except ValueError as e:
                            st.error(f"Erro: {e}")
            except ValueError as e:
                st.error(f"Erro: {e}")

        # =============================
        # ⭐ MINHAS AVALIAÇÕES (ANÔNIMAS)
        # =============================
        elif menu == "Minhas Avaliações ⭐":
            st.subheader("Minhas Avaliações de Clientes")

            try:
                prof = View.profissional_listar_id(id_profissional)
                avaliacoes = prof.get_avaliacoes() if prof else []

                if not avaliacoes:
                    st.info("Você ainda não recebeu nenhuma avaliação.")
                else:
                    st.markdown(
                        f"### ⭐ Média geral: **{prof.get_media_avaliacoes():.1f}** "
                        f"({len(avaliacoes)} avaliações)"
                    )
                    st.caption("⚠️ As avaliações são anônimas para preservar a privacidade dos clientes.")
                    st.divider()

                    for i, av in enumerate(sorted(avaliacoes, key=lambda x: -x["nota"]), start=1):
                        nome_cli = f"Cliente Anônimo #{i}"  # 🔒 Nome oculto
                        st.markdown(
                            f"**{nome_cli}** — ⭐ **{av['nota']:.1f}**  \n"
                            f"💬 *{av['comentario']}*"
                        )
                        st.markdown("---")

            except Exception as e:
                st.error(f"Erro ao carregar avaliações: {e}")


        # =============================
        # 🔒 ALTERAR SENHA
        # =============================
        elif menu == "Alterar Senha":
            st.subheader("Alterar Senha")
            nova = st.text_input("Digite a nova senha", type="password")
            if st.button("Salvar"):
                try:
                    if not nova:
                        raise ValueError("A senha não pode ser vazia.")
                    if View.alterar_senha(id_profissional, nova, "p"):
                        st.success("Senha alterada com sucesso!")
                    else:
                        st.error("Erro ao alterar senha.")
                except ValueError as e:
                    st.error(f"Erro: {e}")
