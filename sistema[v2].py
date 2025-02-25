# Versão 2 do Sistema Bancário

import textwrap
from colorama import init, Fore, Back
init()


def menu():
    menu = '\n\n🏛  Bem vindo(a), ao SUZANO BANK' + """\n
    
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tCadastrar Conta
    [5]\tListar Contas
    [6]\tCadastrar Cliente
    [0]\tSair
    => \t"""
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print('\n✅ Depósito realizado com sucesso!')
    else:
        print('\n❌ Valor inválido! Tente novamente')

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print(f'\n❌ Não há saldo suficiente! - seu saldo atual: R$ {saldo:.2f}')

    elif excedeu_limite:
        print(f'\n❌ Não foi possível realizar o saque! - valor máximo por transação R$ {limite:.2f}')

    elif excedeu_saques:
        print(f'\n❌ Saque não realizado! Você excedeu o limite de saques diários')

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n✅ Saque realizado com sucesso!")

    else:
        print('❌ Valor inválido! Tente novamente')

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n📃 EXTRATO\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('\n❌ Já existe cadastro para o CPF informado!')
        return

    nome = input("Nome Completo: ")
    data_nascimento = input("Data de Nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    clientes.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print('\n✅ Cliente cadastrado com sucesso!')


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente["cpf"] == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def cadastrar_conta(agencia, numero_conta, clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('\n✅ Conta cadastrada com sucesso!')
        return {"agencia": agencia, "numero_conta": numero_conta, "cliente": cliente}

    print('\n❌ Cliente não encontrado, fluxo de criação de conta encerrado!')


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['cliente']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            print('\n📩  DEPÓSITO\n')
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            print('\n💵  SAQUE\n')
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "6":
            print('\n👤 CADASTRO DE CLIENTE\n')
            cadastrar_cliente(clientes)

        elif opcao == "4":
            print('\n💰 CADASTRO DE CONTA\n')
            numero_conta = len(contas) + 1
            conta = cadastrar_conta(AGENCIA, numero_conta, clientes)

            if conta:
                contas.append(conta)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print("\n❌ Operação inválida, por favor selecione novamente a operação desejada.")


main()