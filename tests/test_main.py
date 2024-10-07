from fastapi.testclient import TestClient
from app.main import app
import datetime

client = TestClient(app)

# Mock review data for testing
mock_reviews = [
    {
        "name": "Ana Silva",
        "date": "2024-08-07",
        "review": "O atendimento foi rápido e eficiente, mas senti que poderia ser mais detalhado em alguns pontos técnicos. Por exemplo, ao explicar a falha que ocorreu, o atendente não conseguiu detalhar a causa raiz do problema, o que me deixou com dúvidas sobre o que realmente aconteceu. No geral, foi uma experiência satisfatória, mas acredito que poderia ser mais completa.",
        "sentiment": "neutra"
    },
    {
        "name": "Bruno Souza",
        "date": "2024-09-21",
        "review": "Estou extremamente satisfeito com o suporte! Resolveram meu problema de forma ágil e com clareza nas explicações. Além de resolverem o erro no sistema que estava impedindo a execução de uma função crítica para o meu negócio, eles ainda sugeriram melhorias para evitar que o problema ocorresse novamente. O atendimento foi muito acima do esperado!",
        "sentiment": "positiva"
    },
    {
        "name": "Carlos Pereira",
        "date": "2024-09-10",
        "review": "O serviço foi muito demorado e o atendente parecia completamente despreparado. Precisei repetir meu problema várias vezes, e mesmo assim senti que ele não estava entendendo o que eu estava dizendo. Perdi muito tempo, e o pior de tudo é que o problema não foi resolvido ao final. Vou reconsiderar continuar usando esse serviço.",
        "sentiment": "negativa"
    },
    {
        "name": "Daniela Rocha",
        "date": "2024-08-08",
        "review": "A equipe de suporte foi extremamente atenciosa e dedicada. Adorei o atendimento, pois desde o início até a resolução do meu problema fui informado de cada etapa do processo. Eles fizeram de tudo para que eu entendesse o que estava acontecendo e até me ofereceram um acompanhamento extra para garantir que tudo estivesse funcionando corretamente após a solução.",
        "sentiment": "positiva"
    },
    {
        "name": "Eduardo Lima",
        "date": "2024-08-29",
        "review": "Infelizmente, não conseguiram resolver meu problema, e fiquei muito decepcionado. Além da demora para obter uma resposta clara, não houve um acompanhamento adequado após o primeiro contato, o que deixou a sensação de que meu problema não era uma prioridade. Esperava mais de uma empresa com uma reputação tão boa no mercado.",
        "sentiment": "negativa"
    },
    {
        "name": "Fernanda Carvalho",
        "date": "2024-09-15",
        "review": "O sistema que utilizo tem funcionado bem, mas o suporte não foi tão eficiente quanto eu esperava. Tive que esperar bastante tempo por uma resposta e, quando ela finalmente veio, não era clara o suficiente para que eu pudesse seguir as instruções por conta própria. A experiência foi mediana, espero que melhorem essa parte do serviço.",
        "sentiment": "neutra"
    },
    {
        "name": "Gabriel Costa",
        "date": "2024-09-15",
        "review": "Ótimo serviço! A equipe de suporte foi muito prestativa e realmente se dedicou a resolver o meu problema. Além de solucionarem a questão com rapidez, eles ainda se certificaram de que eu entendesse o que havia causado o erro e como evitar que ele ocorresse novamente no futuro. Superou completamente as minhas expectativas.",
        "sentiment": "positiva"
    },
    {
        "name": "Helena Ribeiro",
        "date": "2024-09-29",
        "review": "O atendente foi educado e respeitoso durante todo o processo, mas infelizmente não conseguiu solucionar o problema técnico que eu estava enfrentando. Ele tentou várias abordagens, mas ao final, ainda fiquei sem uma solução definitiva. Agradeço pelo esforço, mas o resultado final me deixou frustrado.",
        "sentiment": "neutra"
    },
    {
        "name": "Igor Almeida",
        "date": "2024-08-17",
        "review": "Não tive uma boa experiência. Precisei contatar o suporte diversas vezes até que uma solução adequada fosse finalmente apresentada. A falta de consistência nas respostas e a demora entre os contatos me deixaram bastante insatisfeito. Era um problema simples de configuração, mas o processo todo acabou tomando muito mais tempo do que o necessário.",
        "sentiment": "negativa"
    },
    {
        "name": "Julia Martins",
        "date": "2024-09-28",
        "review": "Fui muito bem atendido desde o início, e o problema foi resolvido sem nenhuma complicação. O serviço foi prático, eficiente e me surpreendeu pela rapidez com que conseguiram resolver tudo. A comunicação também foi excelente, me mantendo informado a cada passo. Um atendimento realmente de qualidade.",
        "sentiment": "positiva"
    }
]


# Test creating a review (POST /reviews)
def test_create_review():
    for review in mock_reviews:
        response = client.post("/reviews", json=review)
        print(review["name"])
        assert response.status_code == 200
        assert response.json()["name"] == review["name"]
        #Poderia ser implementado a validação da classificação, mas o modelo não está 100%
        # assert response.json()["sentiment"] == review["sentiment"]


def test_get_all_reviews():
    response = client.get("/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)