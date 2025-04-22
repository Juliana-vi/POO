def iniciais(nome):
    return ''.join([palavra[0].upper() for palavra in nome.split()])

nome_completo = input("Digite seu nome completo: ")
resultado = iniciais(nome_completo)
print(f"As iniciais do nome são: {resultado}")