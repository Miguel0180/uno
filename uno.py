import random
from time import sleep

# Definição de cores e valores das cartas
colors = ['\033[0;31;11m', '\033[0;36;11m', '\033[0;32;11m', '\033[0;33;11m']
numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

# Criação do baralho principal
cartas = ['\033[m+4', '\033[m+4', '\033[m⊞', '\033[m⊞']
for c in range(4):
    for _ in range(2):  # Adicionar cartas especiais (inverso, bloqueio, +2)
        cartas.append(colors[c] + '↪')  # Inverso
        cartas.append(colors[c] + 'Ø')  # Bloqueio
        cartas.append(colors[c] + '+2')  # Comprar 2
    for numero in numeros:
        cartas.append(colors[c] + numero)

# Função para gerar baralhos
def gerarBaralhos(num_jogadores, cartas_por_baralho):
    baralhos = {}
    baralho_principal = cartas.copy()

    for jogador in range(1, num_jogadores + 1):
        baralho_jogador = []
        for _ in range(cartas_por_baralho):
            escolha = random.choice(baralho_principal)
            baralho_principal.remove(escolha)
            baralho_jogador.append(escolha)
        baralhos[f'Jogador {jogador}'] = baralho_jogador

    return baralhos, baralho_principal

# Função para verificar se há carta jogável
def verificaBaralho(baralho, ultimacarta):
    for carta in baralho:
        if verificaCarta(carta, ultimacarta):
            return True
    return False

# Função para verificar se uma carta é jogável
def verificaCarta(realJogada, ultimacarta):
    return (
        realJogada in ['\033[m+4', '\033[m⊞'] or
        realJogada[5] == ultimacarta[5] or
        realJogada[10] == ultimacarta[10]
    )

# Função para escolher a primeira carta
def escolherPrimeiraCarta(baralho_principal):
    while True:
        primeira_carta = random.choice(baralho_principal)
        if primeira_carta not in ['\033[m+4', '\033[m⊞']:
            baralho_principal.remove(primeira_carta)
            return primeira_carta

# Função para mostrar cartas
def mostrarCartas(baralho):
    print("\nSuas cartas:")
    for i, carta in enumerate(baralho, start=1):
        print(f"{carta}", end=' ')
    print('\033[m')

# Função de compra de cartas
def compra(numero_de_compra, baralho_jogadores, jogador, baralho_principal):
    for _ in range(numero_de_compra):
        if not baralho_principal:
            print("O baralho principal está vazio! Não é possível comprar mais cartas.")
            break
        carta = random.choice(baralho_principal)
        baralho_principal.remove(carta)
        baralho_jogadores[jogador].append(carta)
    print(f"{jogador} comprou {numero_de_compra} carta(s).")


def jogadaBot(baralho, ultimacarta, baralho_principal, baralhos):
    if not verificaBaralho(baralho, ultimacarta):
        if baralho_principal:
            carta = random.choice(baralho_principal)
            baralho.append(carta)
            print(f"Bot comprou uma carta")
        else:
            print("Baralho principal vazio! Bot não pode comprar cartas.")
        return ultimacarta
    while True:
        jogada = random.randint(0, len(baralho) - 1)
        realJogada = baralho[jogada]
        if verificaCarta(realJogada, ultimacarta):
            baralho.remove(realJogada)
            baralho_principal.append(realJogada)
            print(f"Bot jogou: {realJogada}")
            print('\033[m')
            if '+2' in realJogada:
                for _ in range(2):
                    if not baralho_principal:
                        print("O baralho principal está vazio! Não é possível comprar mais cartas.")
                        break
                    carta = random.choice(baralho_principal)
                    baralho_principal.remove(carta)
                    baralhos['Jogador 1'].append(carta)
                print(f"Você comprou 2 carta(s).")


            elif '+4' in realJogada or '⊞' in realJogada:
                cor = random.randint(0, 3)
                cores_nomes = ["vermelho", "azul", "verde", "amarelo"]
                realJogada = realJogada.replace('\033[m', colors[cor])
                print(f"Bot escolheu a cor: {cores_nomes[cor]}")
                if '+4' in realJogada:
                    for _ in range(4):
                        if not baralho_principal:
                            print("O baralho principal está vazio! Não é possível comprar mais cartas.")
                            break
                        carta = random.choice(baralho_principal)
                        baralho_principal.remove(carta)
                        baralhos['Jogador 1'].append(carta)
                    print(f"Você comprou 4 carta(s).") 
                
            return realJogada


def jogada_Player(baralho, ultimacarta, baralho_principal, baralhos):
    mostrarCartas(baralho)
    if not verificaBaralho(baralho, ultimacarta):
        if baralho_principal:
            carta = random.choice(baralho_principal)
            baralho.append(carta)
            print(f"Você comprou uma carta: {carta}")
        else:
            print("Baralho principal vazio! Não é possível comprar cartas.")
        return ultimacarta
    while True:

        jogada = int(input(f"Escolha a posição da carta para jogar (1 a {len(baralho)}): ")) - 1
        if jogada < 0 or jogada >= len(baralho):
            print("Escolha inválida! Tente novamente.")
            continue
        realJogada = baralho[jogada]
        if verificaCarta(realJogada, ultimacarta):
            baralho.remove(realJogada)
            baralho_principal.append(realJogada)
            print(f"Você jogou: {realJogada}")
            print('\033[m')
            if '+2' in realJogada:  # Verifica "+2" sem acessar índice fixo
                for _ in range(2):
                    if not baralho_principal:
                        print("O baralho principal está vazio! Não é possível comprar mais cartas.")
                        break
                    carta = random.choice(baralho_principal)
                    baralho_principal.remove(carta)
                    baralhos['Jogador 2'].append(carta)
                print(f"Bot comprou 2 carta(s).")
            elif '+4' in realJogada or '⊞' in realJogada:
                cor = int(input("Escolha a cor (1-Vermelho, 2-Azul, 3-Verde, 4-Amarelo): ")) - 1
                if cor in range(4):
                    cores_nomes = ["vermelho", "azul", "verde", "amarelo"]
                    realJogada = realJogada.replace('\033[m', colors[cor])
                    print(f"Você escolheu a cor: {cores_nomes[cor]}")
                    if realJogada[11] == '4': 
                        for _ in range(4):
                            if not baralho_principal:
                                print("O baralho principal está vazio! Não é possível comprar mais cartas.")
                                break
                            carta = random.choice(baralho_principal)
                            baralho_principal.remove(carta)
                            baralhos['Jogador 2'].append(carta)
                        print(f"Bot comprou 4 carta(s).")
            return realJogada
        else:
            print("Carta inválida! Escolha outra.")




# Função principal
def iniciar():
    baralhos, baralho_principal = gerarBaralhos(2, 7)
    ultima_carta = escolherPrimeiraCarta(baralho_principal)
    print(f"\nPrimeira carta: {ultima_carta}\033[m")
    while True:
        ultima_carta = jogada_Player(baralhos['Jogador 1'], ultima_carta, baralho_principal, baralhos)
        print(f"A última carta agora é: {ultima_carta}")
        print('\033[m')
        sleep(1)
        ultima_carta = jogadaBot(baralhos['Jogador 2'], ultima_carta, baralho_principal, baralhos)
        print(f"A última carta agora é: {ultima_carta}")
        print('\033[m')
        sleep(1)

        if not baralhos['Jogador 1']:
            print('Você Venceu!!')
        
        if not baralhos['Jogador 2']:
            print('Bot Venceu!!')

# Iniciar o jogo
iniciar()
