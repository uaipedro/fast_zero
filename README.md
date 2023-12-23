# Fast Zero - Gerenciamento de Usuários com FastAPI

Fast Zero é uma aplicação baseada em FastAPI que oferece uma API RESTful para o gerenciamento de usuários.

## Pré-requisitos

Certifique-se de ter o [Poetry](https://python-poetry.org/docs/#installation) instalado em sua máquina. Você pode verificar a instalação com `poetry --version`. Se o Poetry não estiver instalado, siga as instruções na [documentação oficial](https://python-poetry.org/docs/#installation) para instalá-lo.

## Instalação

Para instalar e configurar este projeto, siga as etapas abaixo:

1. Clone o repositório para sua máquina local usando `git clone https://github.com/uaipedro/fast_zero.git`.
2. Navegue até a pasta do projeto com `cd NOME_DA_PASTA_DO_PROJETO`.
3. Instale as dependências do projeto com o comando `poetry install`.

## Uso

Para usar este projeto, siga as instruções abaixo:

1. Ative o ambiente virtual do projeto com o comando `poetry shell`.
2. As tarefas do projeto são gerenciadas pelo Taskipy. Consulte a lista de tarefas disponíveis com `poetry run task --list`.
3. Execute a aplicação com o comando `task run`.

## Executando Testes

Para executar os testes automatizados deste sistema, utilize o comando `task test` no terminal.

- Os testes e2e para este projeto estão disponíveis em [https://github.com/uaipedro/e2e-test-for-next-client].
