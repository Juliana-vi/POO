class ContaBancaria:
    def __init__(self, titular, numero, saldo=0.0):
        self.titular = titular
        self.numero = numero
        self.saldo = saldo

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print(f"Depósito de R${valor:.2f} realizado com sucesso.")
        else:
            print("O valor do depósito deve ser positivo.")

    def sacar(self, valor):
        if valor > 0:
            if valor <= self.saldo:
                self.saldo -= valor
                print(f"Saque de R${valor:.2f} realizado com sucesso.")
            else:
                print("Saldo insuficiente para realizar o saque.")
        else:
            print("O valor do saque deve ser positivo.")

    def exibir_saldo(self):
        print(f"Saldo atual: R${self.saldo:.2f}")

def main():
    titular = input("Digite o nome do titular da conta: ")
    numero = input("Digite o número da conta: ")
    conta = ContaBancaria(titular, numero)

    while True:
        print("\nEscolha uma operação:")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Exibir saldo")
        print("4. Sair")
        opcao = input("Digite sua opção: ")

        if opcao == "1":
            valor = float(input("Digite o valor a ser depositado: "))
            conta.depositar(valor)
        elif opcao == "2":
            valor = float(input("Digite o valor a ser sacado: "))
            conta.sacar(valor)
        elif opcao == "3":
            conta.exibir_saldo()
        elif opcao == "4":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()