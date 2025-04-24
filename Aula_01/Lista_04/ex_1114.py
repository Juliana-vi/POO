senha_correta = 2002
while True:
    senha = int(input())
    if senha == senha_correta:
        print("Acesso Permitido")
        break
    else:
        print("Senha Invalida")