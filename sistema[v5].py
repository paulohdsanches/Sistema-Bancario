# Versão 5 do Sistema Bancário

import textwrap
from datetime import datetime
from abc import ABC, abstractmethod, abstractclassmethod, abstractproperty

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
        
    @property
    def saldo(self):
        return self._saldo
        
    @property
    def numero(self):
        return self._numero
        
    @property
    def agencia(self):
         return self._agencia
        
    @property
    def cliente(self):
        return self._cliente
        
    @property
    def historico(self):
        return self._historico
        
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(f'\n❌ Não há saldo suficiente! - seu saldo atual: R$ {saldo:.2f}')

        elif valor > 0:
            self._saldo -= valor
            print("\n✅ Saque realizado com sucesso!")
            return True
            
        else:
            print('❌ Valor inválido! Tente novamente')

        return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n✅ Depósito realizado com sucesso!')

        else:
            print('\n❌ Valor inválido! Tente novamente')
            return False

        return True
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(f'\n❌ Não foi possível realizar o saque! - valor máximo por transação R$ {self._limite:.2f}')

        elif excedeu_saques:
             print(f'\n❌ Operação não realizada! Você excedeu o limite de {self._limite_saques} saques diários')

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f'''\
                Agência:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
                '''

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now(),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
   
    @classmethod
    @abstractmethod  
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            

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

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print(f'\n❌ Cliente não possui conta!')
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input('Informe CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
         print(f'\n❌ Cliente não encontrado!')
         return
    
    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f'\n❌ Cliente não encontrado!')
        return
    
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    data = datetime.now()
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f'\n❌ Cliente não encontrado!')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return  

    print(f'\n📃 EXTRATO - Gerado: {data} \n')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas transações para esta conta'

    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}:\tR${transacao['valor']:.2f}'

    print(extrato)
    print(f"\n\t\tSaldo:\t\tR$ {conta.saldo:.2f}")
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

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('\n✅ Cliente cadastrado com sucesso!')

def cadastrar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n❌ Cliente não encontrado, fluxo de criação de conta encerrado!')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n✅ Conta cadastrada com sucesso!')

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []
   
    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)
               
                           
        elif opcao == "2":
            sacar(clientes)
           
        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "6":
            cadastrar_cliente(clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            cadastrar_conta(numero_conta, clientes, contas)
            
        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "0":
            break

        else:
            print("\n❌ Operação inválida, por favor selecione novamente a operação desejada.")

main()