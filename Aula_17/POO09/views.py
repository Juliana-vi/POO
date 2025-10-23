from models.cliente import Cliente, ClienteDAO
from models.servico import Servico, ServicoDAO
from models.horario import Horario, HorarioDAO
from models.profissional import Profissional, ProfissionalDAO
from datetime import datetime, timedelta

class View:

    def cliente_criar_admin():
        for c in View.cliente_listar():
            if c.get_email() == "admin":
                return
        View.cliente_inserir("admin", "admin", "fone", "1234")

    @staticmethod
    def cliente_autenticar(email, senha):
        """
        Autentica tanto clientes normais quanto o admin.
        O admin é identificado por email='admin'
        """
        if email == "admin":
            admin = next((c for c in View.cliente_listar() if c.get_email() == "admin"), None)
            if admin and admin.get_senha() == senha:
                return {"id": admin.get_id(), "nome": "admin", "tipo": "a"}
            else:
                return None

        for c in View.cliente_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id": c.get_id(), "nome": c.get_nome(), "tipo": "c"}
        return None



    def cliente_listar():
        r = ClienteDAO.listar()
        r.sort(key=lambda obj: obj.get_nome())
        return r

    def cliente_inserir(nome, email, fone, senha):
        cliente = Cliente(0, nome, email, fone, senha)
        ClienteDAO.inserir(cliente)

    def cliente_atualizar(id, nome, email, fone, senha):
        cliente = Cliente(id, nome, email, fone, senha)
        ClienteDAO.atualizar(cliente)

    def cliente_excluir(id):
        cliente = Cliente(id, "", "", "", "")
        ClienteDAO.excluir(cliente)

    @staticmethod
    def cliente_listar_id(id):
        clientes = View.cliente_listar()
        for cliente in clientes:
            if cliente.get_id() == id:
                return cliente
        return None

    # -------- SERVIÇO --------
    def servico_listar():
        r = ServicoDAO.listar()
        r.sort(key=lambda obj: obj.get_descricao())
        return r

    def servico_inserir(descricao, valor):
        servico = Servico(0, descricao, valor)
        ServicoDAO.inserir(servico)

    def servico_atualizar(id, descricao, valor):
        servico = Servico(id, descricao, valor)
        ServicoDAO.atualizar(servico)

    def servico_excluir(id):
        servico = Servico(id, "", 0.0)
        ServicoDAO.excluir(servico)

    @staticmethod
    def servico_listar_id(id):
        servicos = View.servico_listar()
        for servico in servicos:
            if servico.get_id() == id:
                return servico
        return None

    # -------- HORÁRIO --------
    def horario_listar():
        r = HorarioDAO.listar()
        r.sort(key=lambda obj: obj.get_data())
        return r

    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        # data pode vir como string ou datetime
        from datetime import datetime
        if isinstance(data, str):
            try:
                data = datetime.strptime(data, "%Y-%m-%d %H:%M")
            except ValueError:
                data = datetime.strptime(data, "%Y-%m-%d")
        c = Horario(0, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.inserir(c)


    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        c = Horario(id, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO.atualizar(c)

    def horario_excluir(id):
        c = Horario(id, None)
        HorarioDAO.excluir(c)

    def horario_listar_id(id):
        horario = HorarioDAO.listar_id(id)
        return horario

    def horario_agendar_horario(id_profissional):
        r = []
        agora = datetime.now()
        for h in View.horario_listar():
            if (
                h.get_data() >= agora and
                h.get_confirmado() == False and
                h.get_id_cliente() == None and
                h.get_id_profissional() == id_profissional
            ):
                r.append(h)
        r.sort(key=lambda h: h.get_data())
        return r

    def horario_filtrar_profissional(id_profissional):
        r = []
        for h in View.horario_listar():
            if h.get_id_profissional() == id_profissional:
                r.append(h)
        return r
    
    def filtrar_horarios_cliente(id_cliente, confirmado=None, data=None):
        horarios = [h for h in View.horario_listar() if h.get_id_cliente() == id_cliente]
        if confirmado is not None:
            horarios = [h for h in horarios if h.get_confirmado() == confirmado]
        if data:
            horarios = [h for h in horarios if h.get_data().date() == data]
        return sorted(horarios, key=lambda h: h.get_data())
    
    def filtrar_horarios_profissional(id_prof, confirmado=None, data=None):
        horarios = [h for h in View.horario_listar() if h.get_id_profissional() == id_prof]
        if confirmado is not None:
            horarios = [h for h in horarios if h.get_confirmado() == confirmado]
        if data:
            horarios = [h for h in horarios if h.get_data().date() == data]
        return sorted(horarios, key=lambda h: h.get_data())
    
    def confirmar_servico_profissional(id_horario):
        h = View.horario_listar_id(id_horario)
        if h:
            h.set_confirmado(True)
            HorarioDAO.atualizar(h)
            return True
        return False




    # -------- PROFISSIONAL --------
    def profissional_listar():
        r = ProfissionalDAO.listar()
        r.sort(key=lambda obj: obj.get_nome())
        return r

    def profissional_autenticar(email, senha):
        for p in View.profissional_listar():
            if p.get_email() == email and p.get_senha() == senha:
                return {"id": p.get_id(), "nome": p.get_nome()}
        return None

    def profissional_inserir(nome, especialidade, conselho, email, senha):
        profissional = Profissional(0, nome, especialidade, conselho, email, senha)
        ProfissionalDAO.inserir(profissional)

    def profissional_atualizar(id, nome, especialidade, conselho, email, senha):
        profissional = Profissional(id, nome, especialidade, conselho, email, senha)
        ProfissionalDAO.atualizar(profissional)

    def profissional_excluir(id):
        profissional = Profissional(id, '', '', '', '', '')
        ProfissionalDAO.excluir(profissional)

    @staticmethod
    def profissional_listar_id(id):
        profissionais = View.profissional_listar()
        for profissional in profissionais:
            if profissional.get_id() == id:
                return profissional
        return None

    @staticmethod
    def abrir_agenda(id_profissional, data_inicio, data_fim, hora_inicio, hora_fim, intervalo):
        data_atual = datetime.strptime(data_inicio, "%d/%m/%Y")
        data_limite = datetime.strptime(data_fim, "%d/%m/%Y")

        while data_atual <= data_limite:
            hora = datetime.strptime(hora_inicio, "%H:%M")
            fim = datetime.strptime(hora_fim, "%H:%M")

            while hora <= fim:
                data_completa = datetime.combine(data_atual.date(), hora.time())
                h = Horario(0, data_completa)
                h.set_confirmado(False)
                h.set_id_cliente(None)
                h.set_id_servico(None)
                h.set_id_profissional(id_profissional)
                HorarioDAO.inserir(h)

                hora += timedelta(minutes=intervalo)
            data_atual += timedelta(days=1)

    @staticmethod
    def visualizar_agenda(id_profissional):
        horarios = []
        for h in View.horario_filtrar_profissional(id_profissional):
            cliente = None
            servico = None
            if h.get_id_cliente():
                cliente = View.cliente_listar_id(h.get_id_cliente())
            if h.get_id_servico():
                servico = View.servico_listar_id(h.get_id_servico())

            horarios.append({
                "id": h.get_id(),
                "data": h.get_data(),
                "confirmado": h.get_confirmado(),
                "cliente": cliente.get_nome() if cliente else "—",
                "servico": servico.get_descricao() if servico else "—"
            })
        return horarios

    @staticmethod
    def visualizar_meus_servicos(id_cliente):
        servicos = []
        for h in View.horario_listar():
            if h.get_id_cliente() == id_cliente:
                profissional = View.profissional_listar_id(h.get_id_profissional())
                servico = View.servico_listar_id(h.get_id_servico())

                servicos.append({
                    "data": h.get_data(),
                    "confirmado": h.get_confirmado(),
                    "profissional": profissional.get_nome() if profissional else "—",
                    "servico": servico.get_descricao() if servico else "—"
                })
        servicos.sort(key=lambda s: s["data"])
        return servicos

    @staticmethod
    def confirmar_servico(id_horario):
        h = View.horario_listar_id(id_horario)
        if h:
            h.set_confirmado(True)
            HorarioDAO.atualizar(h)


    @staticmethod
    def profissional_abrir_agenda(id_profissional, dias=7):
        agora = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        horarios_atuais = View.horario_filtrar_profissional(id_profissional)
        datas_existentes = [h.get_data().date() for h in horarios_atuais]

        for i in range(dias):
            dia = agora + timedelta(days=i)
            for hora in range(8, 16):
                data_hora = dia.replace(hour=hora)
                if data_hora.date() not in datas_existentes:
                    View.horario_inserir(
                        data=data_hora,
                        confirmado=False,
                        id_cliente=None,
                        id_servico=None,
                        id_profissional=id_profissional
                    )

    @staticmethod
    def profissional_visualizar_agenda(id_profissional):
        return [
            h for h in View.horario_listar()
            if h.get_id_profissional() == id_profissional
        ]
    
    @staticmethod
    def listar_agenda_profissional_ordenada(id_prof, ordem="asc"):
        lista = View.profissional_visualizar_agenda(id_prof)
        return sorted(
            lista,
            key=lambda h: h.get_data(),
            reverse=(ordem == "desc")
        )


    @staticmethod
    def profissional_confirmar_servico(id_horario):
        h = View.horario_listar_id(id_horario)
        if h:
            h.set_confirmado(True)
            HorarioDAO.atualizar(h)

    @staticmethod
    def cliente_visualizar_servicos(id_cliente):
        return [
            h for h in View.horario_listar()
            if h.get_id_cliente() == id_cliente
        ]
    
    @staticmethod
    def listar_servicos_cliente_ordenado(id_cliente, ordem="asc"):
        lista = View.cliente_visualizar_servicos(id_cliente)
        return sorted(
            lista,
            key=lambda h: h.get_data(),
            reverse=(ordem == "desc")
        )

    @staticmethod
    def alterar_senha(id_usuario, nova_senha, tipo):
        # Altera senha de cliente
        if tipo == "c":
            c = View.cliente_listar_id(id_usuario)
            if c:
                c.set_senha(nova_senha)
                ClienteDAO.atualizar(c)

        # Altera senha de profissional
        elif tipo == "p":
            p = View.profissional_listar_id(id_usuario)
            if p:
                p.set_senha(nova_senha)
                ProfissionalDAO.atualizar(p)

        # 🔐 Novo bloco: altera senha do admin
        elif tipo == "a":
          admin = View.cliente_listar_id(id_usuario)
          if admin and admin.get_email() == "admin":
            admin.set_senha(nova_senha)
            ClienteDAO.atualizar(admin)

