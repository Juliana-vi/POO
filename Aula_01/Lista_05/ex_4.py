def aprovado(nota1, nota2):
    media = (nota1 + nota2) / 2
    return media >= 60

nota1 = float(input("Digite a nota do primeiro bimestre: "))
nota2 = float(input("Digite a nota do segundo bimestre: "))
if aprovado(nota1, nota2):
    print("O aluno foi aprovado.")
else:
    print("O aluno está em prova final.")