import pytest
from fastapi.testclient import TestClient
from app.main import app
# from app.db import get_db
from app.create_db import reset_database


@pytest.fixture(scope="module")
def client_fixture():
    client = TestClient(app)
    # Antes de cada teste, resetar o banco de dados para garantir um estado limpo
    reset_database()
    yield client


# Mock review data for testing
mock_reviews = [
        {
            "name": "Ana Silva",
            "date": "2024-08-07",
            "review": """O atendimento foi rápido e eficiente, mas senti que poderia
            ser mais detalhado em alguns pontos técnicos. Por exemplo, ao explicar a
            falha que ocorreu, o atendente não conseguiu detalhar a causa raiz do
            problema, o que me deixou com dúvidas sobre o que realmente aconteceu.
            No geral, foi uma experiência satisfatória, mas acredito que
            poderia ser mais completa.""",
            "sentiment": "neutra",
        },
        {
            "name": "Bruno Souza",
            "date": "2024-09-21",
            "review": """Estou extremamente satisfeito com o suporte! Resolveram
            meu problema de forma ágil e com clareza nas explicações.
            Além de resolverem o erro no sistema que estava impedindo
            a execução de uma função crítica para o meu negócio, eles
            ainda sugeriram melhorias para evitar que o problema
            ocorresse novamente. O atendimento foi muito acima do esperado!""",
            "sentiment": "positiva",
        },
        {
            "name": "Carlos Pereira",
            "date": "2024-09-10",
            "review": """O serviço foi muito demorado e o atendente parecia
            completamente despreparado. Precisei repetir meu problema
            várias vezes, e mesmo assim senti que ele não estava
            entendendo o que eu estava dizendo. Perdi muito tempo,
            e o pior de tudo é que o problema não foi resolvido ao
            final. Vou reconsiderar continuar usando esse serviço.""",
            "sentiment": "negativa",
        },
        {
            "name": "Daniela Rocha",
            "date": "2024-08-08",
            "review": """A equipe de suporte foi extremamente atenciosa e dedicada.
            Adorei o atendimento, pois desde o início até a resolução do meu
            problema fui informado de cada etapa do processo.
            Eles fizeram de tudo para que eu entendesse o que estava
            acontecendo e até me ofereceram um acompanhamento extra
            para garantir que tudo estivesse funcionando corretamente
            após a solução.""",
            "sentiment": "positiva",
        },
        {
            "name": "Eduardo Lima",
            "date": "2024-08-29",
            "review": """Infelizmente, não conseguiram resolver meu problema,
            e fiquei muito decepcionado. Além da demora para obter uma resposta
            clara, não houve um acompanhamento adequado após o primeiro contato,
            o que deixou a sensação de que meu problema não era uma prioridade.
            Esperava mais de uma empresa com uma reputação tão boa no mercado.""",
            "sentiment": "negativa",
        },
        {
            "name": "Fernanda Carvalho",
            "date": "2024-09-15",
            "review": """O sistema que utilizo tem funcionado bem, mas o suporte não
            foi tão eficiente quanto eu esperava. Tive que esperar bastante tempo
            por uma resposta e, quando ela finalmente veio, não era clara
            o suficiente para que eu pudesse seguir as instruções por conta própria.
            A experiência foi mediana, espero que melhorem essa parte do serviço.""",
            "sentiment": "neutra",
        },
        {
            "name": "Gabriel Costa",
            "date": "2024-09-15",
            "review": """Ótimo serviço! A equipe de suporte foi muito prestativa e
            realmente se dedicou a resolver o meu problema. Além de solucionarem a
            questão com rapidez, eles ainda se certificaram de que eu entendesse o
            que havia causado o erro e como evitar que ele ocorresse novamente no
            futuro. Superou completamente as minhas expectativas.""",
            "sentiment": "positiva",
        },
        {
            "name": "Helena Ribeiro",
            "date": "2024-09-29",
            "review": """O atendente foi educado e respeitoso durante todo o processo,
            mas infelizmente não conseguiu solucionar o problema técnico que eu estava
            enfrentando. Ele tentou várias abordagens, mas ao final, ainda fiquei
            sem uma solução definitiva. Agradeço pelo esforço, mas o resultado final
            me deixou frustrado.""",
            "sentiment": "neutra",
        },
        {
            "name": "Igor Almeida",
            "date": "2024-08-17",
            "review": """Não tive uma boa experiência. Precisei contatar o suporte
            diversas vezes até que uma solução adequada fosse finalmente apresentada.
            A falta de consistência nas respostas e a demora entre os contatos me
            deixaram bastante insatisfeito. Era um problema simples de configuração,
            mas o processo todo acabou tomando muito mais tempo do que o necessário.""",
            "sentiment": "negativa",
        },
        {
            "name": "Julia Martins",
            "date": "2024-09-28",
            "review": """Fui muito bem atendido desde o início, e o problema foi
            resolvido sem nenhuma complicação. O serviço foi prático, eficiente
            e me surpreendeu pela rapidez com que conseguiram resolver tudo.
            A comunicação também  foi excelente, me mantendo informado a
            cada passo. Um atendimento   realmente de qualidade.""",
            "sentiment": "positiva",
        },
]


def test_reset_db(client_fixture):
    response_reset = client_fixture.get("/reset")
    assert response_reset.status_code == 200
    assert response_reset.json() == "Sucess"
    response = client_fixture.get("/reviews")
    assert response.status_code == 200
    assert response.json()["total"] == 0


def test_create_review(client_fixture):
    for review in mock_reviews:
        response = client_fixture.post("/reviews", json=review)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == review["name"]
        assert data["date"] == review["date"]
        assert data["review"] == review["review"]
        # assert data["sentiment"] == review["sentiment"]


def test_get_all_reviews(client_fixture):
    response = client_fixture.get("/reviews")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "total_pages" in data
    assert data["total"] == len(mock_reviews)
    assert len(data["items"]) == len(mock_reviews)


def test_get_single_review_success(client_fixture):
    review = mock_reviews[0]
    post_response = client_fixture.post("/reviews", json=review)
    assert post_response.status_code == 200
    created_review = post_response.json()
    review_id = created_review["id"]

    get_response = client_fixture.get(f"/reviews/{review_id}")
    assert get_response.status_code == 200
    fetched_review = get_response.json()
    assert fetched_review["id"] == review_id
    assert fetched_review["name"] == review["name"]
    # assert fetched_review["sentiment"] == review["sentiment"]


def test_get_single_review_not_found(client_fixture):
    response = client_fixture.get("/reviews/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"


def test_pagination(client_fixture):
    response = client_fixture.get("/reviews?page=1&per_page=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["total_pages"] >= 1
    assert len(data["items"]) <= 5


def test_get_report_success(client_fixture):
    start_date = "2024-08-01"
    end_date = "2024-09-30"
    response = client_fixture.get(
        f"/reviews/report?start_date={start_date}&end_date={end_date}"
        )
    assert response.status_code == 200
    data = response.json()
    assert "reviews" in data
    assert "positiva" in data
    assert "neutra" in data
    assert "negativa" in data


def test_get_report_invalid_dates(client_fixture):
    start_date = "2024-13-01"  # Mês inválido
    end_date = "2024-09-31"    # Dia inválido
    response = client_fixture.get(
        f"/reviews/report?start_date={start_date}&end_date={end_date}"
        )
    assert response.status_code == 500
    assert "Erro ao gerar relatório" in response.json()["detail"]


def test_create_review_invalid_data(client_fixture):
    invalid_review = {
        "name": "Test User",
        # "date" está faltando
        "review": "Este é um review de teste.",
        "sentiment": "positiva",
    }
    response = client_fixture.post("/reviews", json=invalid_review)
    assert response.status_code == 422  # Unprocessable Entity


def test_sentiment_analysis(client_fixture):
    review = {
        "name": "Test Sentiment",
        "date": "2024-10-01",
        "review": "Este é um review muito bom!",
        "sentiment": "positiva",
    }
    response = client_fixture.post("/reviews", json=review)
    assert response.status_code == 200
    # data = response.json()
    # assert data["sentiment"] == "positiva"

    review_negativo = {
        "name": "Test Sentiment Negative",
        "date": "2024-10-02",
        "review": "Este é um review muito ruim!",
        "sentiment": "negativa",
    }
    response_neg = client_fixture.post("/reviews", json=review_negativo)
    assert response_neg.status_code == 200
    data_neg = response_neg.json()
    assert data_neg["sentiment"] == "negativa"


def test_reset_database(client_fixture):
    response = client_fixture.post("/reviews", json=mock_reviews[0])
    assert response.status_code == 200
    response = client_fixture.post("/reviews", json=mock_reviews[1])
    assert response.status_code == 200

    reset_response = client_fixture.get("/reset")
    assert reset_response.status_code == 200
    assert reset_response.json() == "Sucess"

    get_response = client_fixture.get("/reviews")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0
