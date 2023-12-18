import random
participantes = {}
while True:
    menu = input(f"digite 'adicionar' para adicionar um participante, \n tecle 'exit' para enserrar o programa").lower()
    if menu == 'adicionar':
        nome = input("Digite o nome do participantes a ser adicionado ao sorteio:").lower().strip()
        numero = int(input(f"digite o número escolhido por {nome}"))
        participantes[nome] = [numero]
    elif menu == 'mostrar':
        for name, nun in participantes.items():
            print(f'{name} {nun}')
    elif menu == 'exit':
        break
    elif menu == 'sortear':
        vencedor_nome = random.choice(list(participantes.keys()))
        vencedor_numero = participantes[vencedor_nome]
        print(f'O vencedor é: \n {vencedor_nome} com o número {vencedor_numero}!')
    else:
        print('opção inválida.')