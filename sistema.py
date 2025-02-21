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
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == '1':
        print(Fore.GREEN + '\n\n↑ ↑ ↑ ↑ ↑ Depósito ↑ ↑ ↑ ↑ ↑\n' + Fore.RESET)

        deposito = float(input('Informe o valor do depósito: '))
        
        if deposito > 0:
            saldo += deposito
            extrato  += f'Depósito: R$ {deposito:.2f}\n'

        else:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + 'Valor inválido! Tente novamente' + Fore.RED + ' X X X X X' + Fore.RESET)

    elif opcao == '2':
        print(Fore.RED + '\n\n↓ ↓ ↓ ↓ ↓ Saque ↓ ↓ ↓ ↓ ↓\n' + Fore.RESET)
        saque = float(input('Informe o valor do saque: '))

        passou_saldo = saque > saldo

        passou_limite = saque > limite

        passou_qtde_saque = numero_saques >= LIMITE_SAQUES

        if passou_saldo:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + f'Não há saldo suficiente! - seu saldo atual: R$ {saldo:.2f}' + Fore.RED + ' X X X X X' + Fore.RESET)

        elif passou_limite:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + f'Não foi possível realizar o saque! - valor máximo por transação R$ {limite:.2f}' + Fore.RED + ' X X X X X' + Fore.RESET)

        elif passou_qtde_saque:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + f'Saque não realizado! Você excedeu o limite de {LIMITE_SAQUES} saques diários' + Fore.RED + ' X X X X X' + Fore.RESET)

        elif saque > 0:
            saldo -= saque
            extrato += f'Saque: R$ {saque:.2f}\n'
            numero_saques += 1

        else:
            print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + 'Valor inválido! Tente novamente' + Fore.RED + ' X X X X X' + Fore.RESET)       

    elif opcao == '3':
        print(Fore.YELLOW + '\n\n░ ░ ░ ░ ░ Extrato ░ ░ ░ ░ ░\n' + Fore.RESET)
        print('Não há movimentações na conta' if not extrato else extrato)
        print(f'Saldo: R$ {saldo:.2f}')
        print(Fore.YELLOW + '\n░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░ ░' + Fore.RESET)
    

    elif opcao == '0':
        break

    else:
        print(Fore.RED + '\n\nX X X X X ' + Fore.RESET + 'Operação inválida! Favor selecionar operação do menu' + Fore.RED + ' X X X X X' + Fore.RESET)

