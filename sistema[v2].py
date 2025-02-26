# Versão 2 do Sistema Bancário

from datetime import datetime
from colorama import init, Fore, Back
init()

menu = '''
$ $ $ $ $ Bem vindo(a), ao SUZANO BANK $ $ $ $ $

                    [1] Depósito
                    [2] Saque
                    [3] Extrato
                    [0] Sair

Digite uma opção para iniciar: '''    


saldo = 0
limite = 500
extrato = ''
LIMITE_TRANSACOES = 10
numero_transacoes = 0

while True:

    opcao = input(menu)

    if opcao == '1':
        print(Fore.GREEN + '\n\n↑ ↑ ↑ ↑ ↑ Depósito ↑ ↑ ↑ ↑ ↑\n' + Fore.RESET)

        deposito = float(input('Informe o valor do depósito: '))
        passou_qtde_transacoes = numero_transacoes >= LIMITE_TRANSACOES

        if passou_qtde_transacoes:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + f'Transação não realizada! Você excedeu o limite de {LIMITE_TRANSACOES} transações diárias' + Fore.RED + ' X X X X X' + Fore.RESET)

        
        elif deposito > 0:
            data = datetime.now()
            saldo += deposito
            extrato  += f'{data} - Depósito: R$ {deposito:.2f}\n' 
            numero_transacoes += 1

        else:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + 'Valor inválido! Tente novamente' + Fore.RED + ' X X X X X' + Fore.RESET)

    elif opcao == '2':
        print(Fore.RED + '\n\n↓ ↓ ↓ ↓ ↓ Saque ↓ ↓ ↓ ↓ ↓\n' + Fore.RESET)
        saque = float(input('Informe o valor do saque: '))

        passou_saldo = saque > saldo

        passou_limite = saque > limite

        passou_qtde_transacoes = numero_transacoes >= LIMITE_TRANSACOES

        if passou_saldo:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + f'Não há saldo suficiente! - seu saldo atual: R$ {saldo:.2f}' + Fore.RED + ' X X X X X' + Fore.RESET)

        elif passou_limite:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + f'Não foi possível realizar o saque! - valor máximo por transação R$ {limite:.2f}' + Fore.RED + ' X X X X X' + Fore.RESET)

        elif passou_qtde_transacoes:
           print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + f'Transação não realizada! Você excedeu o limite de {LIMITE_TRANSACOES} transações diárias' + Fore.RED + ' X X X X X' + Fore.RESET)

        elif saque > 0:
            data = datetime.now()
            saldo -= saque
            extrato += f'{data} - Saque: R$ {saque:.2f}\n'
            numero_transacoes += 1

        else:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + 'Valor inválido! Tente novamente' + Fore.RED + ' X X X X X' + Fore.RESET)       

    elif opcao == '3':
        passou_qtde_transacoes = numero_transacoes >= LIMITE_TRANSACOES
        if passou_qtde_transacoes:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + f'Transação não realizada! Você excedeu o limite de {LIMITE_TRANSACOES} transações diárias' + Fore.RED + ' X X X X X' + Fore.RESET)

        else:
            data = datetime.now()
            print(Fore.YELLOW + f'\n\n░ ░ ░ ░ ░ Extrato ░ ░ ░ ░ ░ Gerado: {data} \n' + Fore.RESET)
            print('Não há movimentações na conta' if not extrato else extrato)
            print(f'Saldo: R$ {saldo:.2f}')
            print(Fore.YELLOW + '\n░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░' + Fore.RESET)

            numero_transacoes += 1
    

    elif opcao == '0':
        break

    else:
        print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + 'Operação inválida! Favor selecionar operação do menu' + Fore.RED + ' X X X X X' + Fore.RESET)




