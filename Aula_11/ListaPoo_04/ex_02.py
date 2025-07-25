class Contato:
    def __init__(self, i, n, e, f):
        self.__id = i
        self.__nome = n
        self.__email = e
        self.__fone = f
    def get_id(self):
        return self.__id
    def get_nome(self):
        return self.__nome    
    def set_nome(self, n):
        self.__nome = n
    def set_email(self, e):
        self.__email = e
    def set_fone(self, f):
        self.__fone = f
    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__email} - {self.__fone}"

class ContatoUI:
    __contatos = []
    __next_id = 1
    
    @classmethod    
    def main(cls):
        op = 0
        while op != 6:
            op = ContatoUI.menu()
            if op == 1: ContatoUI.inserir()
            if op == 2: ContatoUI.listar()
            if op == 3: ContatoUI.atualizar()
            if op == 4: ContatoUI.excluir()
            if op == 5: ContatoUI.pesquisar()
    @classmethod    
    def menu(cls):
        print("1-Inserir, 2-Listar, 3-Atualizar, 4-Excluir, 5-Pesquisar, 6-Fim")
        return int(input("Escolha uma opção: "))
    @classmethod    
    def inserir(cls):
        nome = input("Informe o nome: ")
        email = input("Informe o e-mail: ")
        fone = input("Informe o fone: ")
        c = Contato(cls.__next_id, nome, email, fone)
        cls.__contatos.append(c)
        cls.__next_id += 1
        print("Contato inserido com sucesso!")
    @classmethod    
    def listar(cls):
        for c in cls.__contatos:
            print(c)
    @classmethod    
    def atualizar(cls):
        id = int(input("Informe o id do contato a ser atualizado: "))
        for c in cls.__contatos:
            if c.get_id() == id:
                nome = input("Novo nome: ")
                email = input("Novo e-mail: ")
                fone = input("Novo fone: ")
                c.set_nome(nome)
                c.set_email(email)
                c.set_fone(fone)
                print("Contato atualizado")
                return
        print("Contato não encontrado")
    @classmethod    
    def excluir(cls):
        id = int(input("Informe o id do contato a ser excluído: "))
        for c in cls.__contatos:
            if c.get_id() == id:
                cls.__contatos.remove(c)
                print("Contato excluído")
                return
        print("Contato não encontrado")
    @classmethod    
    def pesquisar(cls):
        nome = input("Informe o nome: ")
        for c in cls.__contatos:
            if c.get_nome().startswith(nome): print(c)

ContatoUI.main()