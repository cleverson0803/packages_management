# importando os módulos necessários
import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return textwrap.dedent(
                f"""
                Agência: {conta.agencia}
                Número: {conta.numero}
                Titular: {conta.cliente.nome}
                Saldo: R$ {conta.saldo:.2f}
                """
            )
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return

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
        self._agencia = "0001"
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

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor do depósito deve ser positivo. @@@")

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            print(f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! Saldo insuficiente ou valor inválido. @@@")

    def exibir_saldo(self):
        print(f"\n=== Saldo atual: R$ {self._saldo:.2f} ===")


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite, limite_saques):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_diarios = 0

    @classmethod
    def nova_conta(cls, cliente, numero, limite=500, limite_saques=3):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        if self._saques_diarios >= self._limite_saques:
            print("\n@@@ Operação falhou! Limite de saques diários excedido. @@@")
        elif valor > self._saldo + self._limite:
            print("\n@@@ Operação falhou! Limite de crédito excedido. @@@")
        else:
            super().sacar(valor)
            self._saques_diarios += 1


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def transacoes_do_dia(self):
        hoje = datetime.now().date()
        return [t for t in self.transacoes if t["data"].date() == hoje]


def log_transacao(func):
    def wrapper(*args, **kwargs):
        print(f"\n=== Log: Iniciando a operação {func.__name__} ===")
        resultado = func(*args, **kwargs)
        print(f"=== Log: Operação {func.__name__} finalizada ===")
        return resultado

    return wrapper


def menu():
    opcoes = """
    Escolha uma das opções a seguir:
    [d] Depositar
    [s] Sacar
    [e] Exibir Saldo
    [nu] Novo Cliente
    [nc] Nova Conta
    [lc] Listar Contas
    [q] Sair
    => """
    return input(textwrap.dedent(opcoes))


def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta = int(input("Informe o número da conta: "))
    conta = next((c for c in cliente.contas if c.numero == numero_conta), None)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    valor = float(input("Informe o valor a ser depositado: "))
    conta.depositar(valor)
    conta.historico.adicionar_transacao({"tipo": "depósito", "valor": valor, "data": datetime.now()})


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta = int(input("Informe o número da conta: "))
    conta = next((c for c in cliente.contas if c.numero == numero_conta), None)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    valor = float(input("Informe o valor a ser sacado: "))
    conta.sacar(valor)
    conta.historico.adicionar_transacao({"tipo": "saque", "valor": valor, "data": datetime.now()})


@log_transacao
def exibirExtrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta = int(input("Informe o número da conta: "))
    conta = next((c for c in cliente.contas if c.numero == numero_conta), None)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    conta.exibir_saldo()
    print("\n=== Extrato ===")
    for transacao in conta.historico.transacoes:
        print(f"{transacao['data']}: {transacao['tipo']} de R$ {transacao['valor']:.2f}")


@log_transacao
def criarCliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


@log_transacao
def criarConta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    # NOTE: O valor padrão de limite de saques foi alterado para 50 saques
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, limite=500, limite_saques=50)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listarContas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibirExtrato(clientes)

        elif opcao == "nu":
            criarCliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criarConta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listarContas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Executando o programa
if __name__ == "__main__":
    main()
