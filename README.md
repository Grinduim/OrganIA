# Aplicação de Avaliações com FastAPI

## Visão Geral

Esta aplicação permite a criação, consulta e geração de relatórios de avaliações de clientes. Utilizando FastAPI, SQLAlchemy e análise de sentimento, a API fornece endpoints para gerenciar avaliações, incluindo funcionalidades de criação, listagem com paginação, obtenção de avaliações específicas e geração de relatórios baseados em intervalos de datas.

## Índice

- [Visão Geral](#visão-geral)
- [Configuração e Instalação](#configuração-e-instalação)
- [Executando a Aplicação](#executando-a-aplicação)
- [Acessando a API e Documentação](#acessando-a-api-e-documentação)
- [Rodando os Testes](#rodando-os-testes)
- [Endpoints Disponíveis](#endpoints-disponíveis)

## Configuração e Instalação

1. **Clone o Repositório**:

    ```bash
    git clone https://github.com/Grinduim/OrganIA.git
    cd OrganIA
    ```

2. **Crie um Ambiente Virtual**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. **Instale as Dependências**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o Banco de Dados**:

    Certifique-se de que o banco de dados está configurado corretamente. A aplicação utiliza PostgreSQL por padrão.  
    Caso você já tenha o PostgreSQL instalado, crie um banco de dados chamado 'OrganIA' e execute o script `create_db.py` para criar automaticamente as tabelas:

    ```bash
    python app/create_db.py
    ```

    Caso contrário, é necessário instalar o PostgreSQL e realizar os passos acima.

## Executando a Aplicação

Para iniciar a aplicação FastAPI, execute:

1. Certifique-se de que o ambiente virtual está ativado:
```bash
    venv\Scripts\activate
```
2. Execute a aplicação
```bash

    uvicorn app.main:app --reload
```
A aplicação estará disponível em http://127.0.0.1:8000.

## Acessando a API e Documentação

A FastAPI fornece automaticamente uma documentação interativa para a API utilizando o Swagger UI. Você pode acessá-las através dos seguintes URLs:

Swagger UI: http://127.0.0.1:8000/docs – Uma interface interativa para testar os endpoints da API.

**Importante** : O modelo utilizado atualmente é nlptown/bert-base-multilingual-uncased-sentiment,e com isso a primeira vez pode demorar um pouco, porem você pode alterar para um de sua preferencia e realizar as adaptações necessárias.

Além disso, a string de conexão com o Postgres está hard coded, sendo usuário postgres e senha root, caso você queira alterar alguma informação sobre, você pode alterar em app/db.py


## Rodando os Testes

Os testes foram implementados utilizando pytest. Para garantir que a aplicação funcione corretamente, é importante rodar os testes. Siga os passos abaixo:

**Importante**: Antes de iniciar os testes, é necessário ressaltar que a validação dos resultados da análise de sentimento não está sendo realizada no momento, pois o modelo utilizado pode não estar 100% coerente com os dados disponíveis. No entanto, isso pode ser facilmente corrigido ao remover os comentários no arquivo `test_main.py`.

1. Certifique-se de que o ambiente virtual está ativado:
   ```bash
   venv\Scripts\activate  # No Windows
    ```

2. Execute os testes com o comando:
```bash
    pytest ./test
```
Esse comando irá rodar todos os testes localizados no diretório de testes. Certifique-se de que o banco de dados esteja configurado corretamente, pois os testes irão utilizar o banco de dados padrão da aplicação.

Verifique a saída do pytest para garantir que todos os testes passaram. Se algum teste falhar, verifique o código e faça as correções necessárias.
