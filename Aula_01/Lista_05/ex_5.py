def formatar_nome(nome):
    return nome.title()

nome = input("Digite seu nome completo: ")
nome_formatado = formatar_nome(nome)
print(f"Nome formatado: {nome_formatado}")