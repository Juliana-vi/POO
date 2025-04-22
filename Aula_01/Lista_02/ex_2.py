nota1 = int(input("Digite a nota do primeiro bimestre da disciplina: "))
nota2 = int(input("Digite a nota do segundo bimestre da disciplina: "))
peso1 = 2
peso2 = 3
media_parcial = (nota1 * peso1 + nota2 * peso2) / (peso1 + peso2)
print(f"Média parcial = {int(media_parcial)}")