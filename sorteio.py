import random
import json
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

DIRETORIO = 'files'

def carregar_participantes():
    try:
        with open(os.path.join(DIRETORIO, 'participantes.txt'), 'r') as arquivo:
            participantes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        participantes = {}
    return participantes

def salvar_participantes(participantes):
    if not os.path.exists(DIRETORIO):
        os.makedirs(DIRETORIO)

    with open(os.path.join(DIRETORIO, 'participantes.txt'), 'w') as arquivo:
        json.dump(participantes, arquivo)

def reproduzir_som(arquivo):
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()

def adicionar_participante(participantes):
    numero = int(input("Digite o número escolhido (entre 0 e 120): "))
    
    if 0 <= numero <= 120:
        if not any(numero in nums['numeros'] for nums in participantes.values()):
            nome = input("Digite o nome do participante: ").lower().strip()
            telefone = input("Digite o número de telefone do participante: ")
            
            if nome not in participantes:
                participantes[nome] = {'numeros': [numero], 'telefone': telefone}
            else:
                participantes[nome]['numeros'].append(numero)
                participantes[nome]['telefone'] = telefone

            salvar_participantes(participantes)
            print(f"numero {numero} adicionado com sucesso para o participante {nome}!")
            reproduzir_som(os.path.join(DIRETORIO, 'audios', 'sucesso.mp3'))
        else:
            print(f"O número {numero} já está sendo utilizado por outro participante.")
            reproduzir_som(os.path.join(DIRETORIO, 'audios', 'error.mp3'))
    else:
        print("Número fora do intervalo permitido. Digite um número entre 0 e 120.")
        reproduzir_som(os.path.join(DIRETORIO, 'audios', 'error.mp3'))

def excluir_participante(participantes):
    nome = input("Digite o nome do participante que deseja excluir: ").lower().strip()
    if nome in participantes:
        numero_para_excluir = int(input("Digite o número que deseja excluir: "))
        if numero_para_excluir in participantes[nome]['numeros']:
            participantes[nome]['numeros'].remove(numero_para_excluir)
            if not participantes[nome]['numeros']:
                del participantes[nome]
            salvar_participantes(participantes)
            print(f"Número {numero_para_excluir} excluído com sucesso para o participante {nome}!")
            reproduzir_som(os.path.join(DIRETORIO, 'audios', 'sucesso.mp3'))
        else:
            print(f"O número {numero_para_excluir} não pertence ao participante {nome}.")
            reproduzir_som(os.path.join(DIRETORIO, 'audios', 'error.mp3'))
    else:
        print(f"O participante {nome} não foi encontrado.")
        reproduzir_som(os.path.join(DIRETORIO, 'audios', 'error.mp3'))

def mostrar_participantes(participantes):
    for nome, dados in participantes.items():
        numeros = ', '.join(map(str, dados['numeros']))
        telefone = dados['telefone']
        print(f'{nome}: Números: {numeros}, Telefone: {telefone}')
    if not participantes:
        print('Não há participantes cadastrados.')
        reproduzir_som(os.path.join(DIRETORIO, 'audios', 'error.mp3'))

def main():
    participantes = carregar_participantes()

    while True:
        menu = input(f"Digite 'adicionar' para acrescentar um número ao sorteio, \n'excluir' para remover um número que já está na lista de sorteio, \n'mostrar' para exibir as informações já cadastradas,"
                     f"\n'sortear' para realizar o sorteio, ou 'exit' para encerrar o programa: ").lower()

        if menu == 'adicionar':
            adicionar_participante(participantes)

        elif menu == "excluir":
            excluir_participante(participantes)
        elif menu == 'mostrar':
            mostrar_participantes(participantes)

        elif menu == 'sortear':
            if participantes:
                vencedor_nome = random.choice(list(participantes.keys()))
                vencedor_dados = participantes[vencedor_nome]
                vencedor_numero = random.choice(vencedor_dados['numeros'])
                vencedor_telefone = vencedor_dados['telefone']
                print(f"O vencedor é:\nNome: {vencedor_nome}, Número: {vencedor_numero}, Telefone: {vencedor_telefone}!")
                reproduzir_som(os.path.join(DIRETORIO, 'audios', 'ganhador.mp3'))
            else:
                print("Não há participantes para realizar o sorteio.")
                reproduzir_som(os.path.join(DIRETORIO, 'audios', 'error.mp3'))

        elif menu == 'exit':
            break

        else:
            print('Opção inválida.')
            reproduzir_som(os.path.join(DIRETORIO, 'audios', 'error.mp3'))

if __name__ == "__main__":
    main()
