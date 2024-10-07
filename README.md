# Aplicação de Avaliações com FastAPI

## Visão Geral

Esta aplicação permite a criação, consulta e geração de relatórios de avaliações de clientes. Utilizando FastAPI, SQLAlchemy e análise de sentimento, a API fornece endpoints para gerenciar avaliações, incluindo funcionalidades de criação, listagem com paginação, obtenção de avaliações específicas e geração de relatórios baseados em intervalos de datas.

## Índice

- [Visão Geral](#visão-geral)
- [Configuração e Instalação](#configuração-e-instalação)
- [Executando a Aplicação](#executando-a-aplicação)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Rodando os Testes](#rodando-os-testes)
- [Exemplos de Uso](#exemplos-de-uso)
- [Contribuição](#contribuição)
- [Licença](#licença)


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
    Caso você tenha o PostgreSQL basta criar uma database chamada 'OrganIA' e executar o script create_db.py  que o banco sera criado automaticamente
    ```bash
    uvicorn app.main:app --reload

    Caso contrario, é necessário fazer toda a instalação do PostgreSQL e realizar os passos acima. 

## Executando a Aplicação

Para iniciar a aplicação FastAPI, execute:

```bash
uvicorn app.main:app --reload
