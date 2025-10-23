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
        Autentica clientes e admin.
        Esta versão é robusta: aceita que ClienteDAO.listar() retorne objetos (com métodos)
        ou dicionários (com chaves 'email'/'senha'). Retorna dict com 'id','nome','tipo'.
        """
        def extract_email_senha(obj):
            # tenta extrair email e senha do item (obj pode ser Cliente ou dict)
            if obj is None:
                return (None, None)
            # objeto com métodos
            if hasattr(obj, "get_email") and callable(getattr(obj, "get_email")):
                try:
                    return (obj.get_email(), obj.get_senha())
                except Exception:
                    return (None, None)
            # dicionário (ou similar)
            if isinstance(obj, dict):
                # vários formatos possíveis; tentamos chaves comuns
                email_key = None
                senha_key = None
                for k in ("email", "_Cliente__email", "email_cliente", "login"):
                    if k in obj:
                        email_key = k
                        break
                for k in ("senha", "_Cliente__senha", "password", "passwd"):
                    if k in obj:
                        senha_key = k
                        break
                return (obj.get(email_key) if email_key else None, obj.get(senha_key) if senha_key else None)
            # fallback: str representation — não confiável
            return (None, None)

        clientes = View.cliente_listar()

        if email == "admin":
            for c in clientes:
                em, pw = extract_email_senha(c)
                if em == "admin":
                    # confere senha
                    if pw == senha:
                        # id e nome: tenta extrair
                        id_val = None
                        nome = "admin"
                        if hasattr(c, "get_id"):
                            try:
                                id_val = c.get_id()
                            except:
                                id_val = None
                        elif isinstance(c, dict):
                            id_val = c.get("id") or c.get("_Cliente__id")
                        return {"id": id_val, "nome": nome, "tipo": "a"}
                    else:
                        return None
            return None

        for c in clientes:
            em, pw = extract_email_senha(c)
            if em == email and pw == senha:
                # extrai id e nome
                id_val = None
                nome = None
                if hasattr(c, "get_id"):
                    try:
                        id_val = c.get_id()
                    except:
                        id_val = None
                    try:
                        nome = c.get_nome()
                    except:
                        nome = None
                elif isinstance(c, dict):
                    id_val = c.get("id") or c.get("_Cliente__id")
                    nome = c.get("nome") or c.get("_Cliente__nome")
                # fallback values
                if nome is None:
                    nome = em
                return {"id": id_val, "nome": nome, "tipo": "c"}

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
        """
        Atualiza senha dependendo do tipo:
        - 'c' cliente: atualiza pelo id (se encontrado)
        - 'p' profissional: atualiza pelo id
        - 'a' admin: atualiza sempre o registro com email == 'admin'
        Retorna True se atualizou, False caso contrário.
        """
        # clientes e profissionais via DAO
        # usamos as classes já importadas no topo do arquivo (ClienteDAO, ProfissionalDAO)
        if tipo == "c":
            c = View.cliente_listar_id(id_usuario)
            if c:
                # suporta objeto ou dict
                if hasattr(c, "set_senha"):
                    c.set_senha(nova_senha)
                    ClienteDAO.atualizar(c)
                elif isinstance(c, dict):
                    c_key = c.get("id") or c.get("_Cliente__id")
                    # atualizar via lista salva inteira
                    lista = ClienteDAO.listar()
                    for item in lista:
                        if (isinstance(item, dict) and (item.get("id") == c_key or item.get("_Cliente__id") == c_key)) \
                           or (hasattr(item, "get_id") and item.get_id() == c_key):
                            # item pode ser objeto ou dict
                            if hasattr(item, "set_senha"):
                                item.set_senha(nova_senha)
                                ClienteDAO.atualizar(item)
                            else:
                                item["senha"] = nova_senha
                                # regrava lista inteira
                                try:
                                    ClienteDAO.salvar(lista)
                                except Exception:
                                    pass
                            return True
                return True
            return False

        elif tipo == "p":
            p = View.profissional_listar_id(id_usuario)
            if p:
                if hasattr(p, "set_senha"):
                    p.set_senha(nova_senha)
                    ProfissionalDAO.atualizar(p)
                else:
                    # fallback se dict
                    lista = ProfissionalDAO.listar()
                    for item in lista:
                        if (isinstance(item, dict) and (item.get("id") == id_usuario or item.get("_Profissional__id") == id_usuario)) \
                           or (hasattr(item, "get_id") and item.get_id() == id_usuario):
                            if hasattr(item, "set_senha"):
                                item.set_senha(nova_senha)
                                ProfissionalDAO.atualizar(item)
                            else:
                                item["senha"] = nova_senha
                                try:
                                    ProfissionalDAO.salvar(lista)
                                except Exception:
                                    pass
                            return True
                return True
            return False

        elif tipo == "a":
            # força atualizar o registro cujo email é "admin"
            lista = ClienteDAO.listar()
            found = False
            for item in lista:
                # item pode ser objeto ou dict
                if hasattr(item, "get_email") and item.get_email() == "admin":
                    if hasattr(item, "set_senha"):
                        item.set_senha(nova_senha)
                        ClienteDAO.atualizar(item)
                    else:
                        item_key = item.get("id") if isinstance(item, dict) else None
                        item["senha"] = nova_senha
                        try:
                            ClienteDAO.salvar(lista)
                        except Exception:
                            pass
                    found = True
                    break
                elif isinstance(item, dict) and (item.get("email") == "admin" or item.get("_Cliente__email") == "admin"):
                    item["senha"] = nova_senha
                    try:
                        ClienteDAO.salvar(lista)
                    except Exception:
                        pass
                    found = True
                    break
            return found

        return False
