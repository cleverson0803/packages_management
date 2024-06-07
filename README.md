# Sistema Bancário em Python

Este é um projeto de um sistema bancário simples desenvolvido em Python. O sistema permite a criação de clientes e contas bancárias, bem como a realização de operações bancárias básicas, como depósitos, saques e exibição de saldo.

## Funcionalidades

- **Clientes**:
  - Criar novo cliente.
  - Associar contas a clientes existentes.

- **Contas**:
  - Criar nova conta bancária.
  - Listar contas existentes.

- **Operações**:
  - Depositar em uma conta.
  - Sacar de uma conta.
  - Exibir extrato de uma conta.

## Estrutura do Código

### Classes Principais

- **ContasIterador**: Classe iteradora para listar contas bancárias.
- **Cliente**: Classe base para clientes.
- **PessoaFisica**: Classe derivada de `Cliente` para representar pessoas físicas.
- **Conta**: Classe base para contas bancárias.
- **ContaCorrente**: Classe derivada de `Conta` para representar contas correntes.
- **Historico**: Classe para gerenciar o histórico de transações de uma conta.

### Funções Principais

- **menu**: Exibe o menu de opções para o usuário.
- **filtrar_cliente**: Filtra um cliente a partir do CPF.
- **log_transacao**: Decorador para logar transações.
- **depositar**: Realiza depósito em uma conta.
- **sacar**: Realiza saque de uma conta.
- **exibirExtrato**: Exibe o extrato de uma conta.
- **criarCliente**: Cria um novo cliente.
- **criarConta**: Cria uma nova conta bancária.
- **listarContas**: Lista todas as contas existentes.
- **main**: Função principal para executar o sistema bancário.

