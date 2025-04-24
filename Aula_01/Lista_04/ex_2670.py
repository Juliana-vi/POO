A1 = int(input())
A2 = int(input())
A3 = int(input())

tempo_andar1 = A2 * 2 + A3 * 4
tempo_andar2 = A1 * 2 + A3 * 2
tempo_andar3 = A1 * 4 + A2 * 2
menor_tempo = min(tempo_andar1, tempo_andar2, tempo_andar3)
print(menor_tempo)