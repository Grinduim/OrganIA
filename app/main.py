import datetime
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.models import Review
from app.schemas import ReviewReport, ReviewResponse, ReviewCreate
from sqlalchemy_pagination import paginate
from app.db import SessionLocal
from app.sentiment_analyze import analyze_sentiment
from sqlalchemy.exc import SQLAlchemyError
import logging

app = FastAPI()
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/reviews", response_model=ReviewResponse)
def create_review(review: ReviewCreate,
                  db: Session = Depends(get_db)) -> ReviewResponse:
    """
    Cria uma nova avaliação.

    Este endpoint recebe os dados de uma nova avaliação e os armazena no banco de dados,
    incluindo a análise de sentimento do texto da avaliação.

    Args:
        review (`ReviewCreate`): Os dados da nova avaliação a serem criados.

    Returns:
        `ReviewResponse`: Os dados da avaliação criada, incluindo seu ID e o
         sentimento analisado.

    Raises:
        SQLAlchemyError: Erros relacionados ao banco de dados podem ser levantados se a
        operação falhar.
    """
    try:
        new_review = Review(name=review.name, date=review.date, review=review.review,
                            sentiment=analyze_sentiment(review.review)[0])
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erro ao criar avaliação: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar avaliação")


# @app.get("/reviews", response_model=list[ReviewResponse])
# def get_reviews(db: Session = Depends(get_db)) -> list[ReviewResponse]:
#     """
#     Retorna todas as avaliações analisadas.

#     Este endpoint recupera todas as avaliações de clientes armazenadas no banco de
#     dados e retorna uma lista com as avaliações e suas respectivas classificações de
#     sentimento (positiva, negativa, neutra).

#     Returns:
#         List[`ReviewResponse`]: Uma lista de objetos `ReviewResponse` contendo as
#         avaliações dos clientes e suas classificações de sentimento.

#     Example:
#         Um exemplo de requisição bem-sucedida para esse endpoint via cURL:

#         ```bash
#         curl -X "GET" \
#         "http://127.0.0.1:8000/reviews" \
#         -H "accept: application/json"
#         ```

#         Resposta esperada (exemplo):
#         ```json
#         [
#             {
#                 "id": 1,
#                 "name": "Ana Silva",
#                 "date": "2024-08-07",
#                 "review": "O atendimento foi rápido e eficiente...",
#                 "sentiment": "neutra"
#             },
#             {
#                 "id": 2,
#                 "name": "Bruno Souza",
#                 "date": "2024-09-21",
#                 "review": "Estou extremamente satisfeito com o suporte!",
#                 "sentiment": "positiva"
#             }
#         ]
#         ```

#     Raises:
#         HTTPException: Não há exceções esperadas diretamente desse endpoint, pois ele
#         retorna uma lista vazia caso não haja dados no banco de dados.
#     """
#     reviews = db.query(Review).all()
#     return reviews


@app.get("/reviews", response_model=dict)
def get_reviews(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1),
                db: Session = Depends(get_db)) -> dict:
    """
    Retorna todas as avaliações analisadas com paginação.

    Este endpoint recupera todas as avaliações de clientes armazenadas no banco de
    dados e retorna uma lista paginada com as avaliações e suas respectivas
    classificações de sentimento (positiva, negativa, neutra).

    Args:
        page (int): Número da página a ser recuperada.
        per_page (int): Número de avaliações por página.
        db (Session): Instância de sessão do banco de dados injetada.

    Returns:
        dict: Um dicionário contendo os seguintes campos:
            - items (list): Lista de objetos `ReviewResponse` com as avaliações.
            - total (int): Número total de avaliações.
            - page (int): Número da página atual.
            - total_pages (int): Número total de páginas.

    Example:
        Um exemplo de requisição bem-sucedida para esse endpoint via cURL:

        ```bash
        curl -X "GET" \
        "http://127.0.0.1:8000/reviews?page=1&per_page=10" \
        -H "accept: application/json"
        ```

        Resposta esperada (exemplo):

        ```json
        {
            "items": [
                {
                    "id": 1,
                    "name": "Ana Silva",
                    "date": "2024-08-07",
                    "review": "O atendimento foi rápido e eficiente...",
                    "sentiment": "neutra"
                },
                {
                    "id": 2,
                    "name": "Bruno Souza",
                    "date": "2024-09-21",
                    "review": "Estou extremamente satisfeito com o suporte!",
                    "sentiment": "positiva"
                }
            ],
            "total": 2,
            "page": 1,
            "total_pages": 1
        }
        ```

    Raises:
        HTTPException: Em caso de falha inesperada na query do banco de dados.
    """
    reviews_query = db.query(Review)
    paginated_reviews = paginate(reviews_query, page, per_page)
    return {
        "items": [ReviewResponse.from_orm(review)
                  for review in paginated_reviews.items],
        "total": paginated_reviews.total,
        "page": page,
        "total_pages": paginated_reviews.pages
    }


@app.get("/reviews/report", response_model=ReviewReport)
def get_report(start_date: str, end_date: str,
               db: Session = Depends(get_db)) -> ReviewReport:
    """
    Gera um relatório das avaliações realizadas entre as datas especificadas.

    Este endpoint retorna um relatório com todas as avaliações realizadas em
    um intervalo de tempo.
    As avaliações são classificadas em positiva, neutra ou negativa, e o relatório
    inclui a contagem de cada uma dessas categorias.

    Args:
        start_date (str): A data inicial do intervalo no formato 'YYYY-MM-DD'. |
        end_date (str): A data final do intervalo no formato 'YYYY-MM-DD'.

    Returns:
        `ReviewReport`: Um objeto contendo a lista de avaliações e a contagem de
        sentimentos (positiva, neutra, negativa).

    Raises:
        HTTPException: Se ocorrer algum erro ao gerar o relatório, uma exceção HTTP 500
        será lançada com a mensagem de erro correspondente.

    Example:
        Um exemplo de requisição para o endpoint `/reviews/report`:

        ```bash
        curl -X "GET" \
          "http://127.0.0.1:8000/reviews/
          report?start_date=2024-09-01&end_date=2024-09-30" \
          -H "accept: application/json"
        ```

        Resposta esperada:
        ```json
        {
          "reviews": [
            {
              "id": 1,
              "name": "Ana Silva",
              "date": "2024-08-07",
              "review": "O atendimento foi rápido e eficiente...",
              "sentiment": "neutra"
            }
          ],
          "positiva": 0,
          "neutra": 1,
          "negativa": 0
        }
        ```
    """
    logger.info(f"Generating report for period: {start_date} to {end_date}")
    try:
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        reviews = db.query(Review).filter(Review.date.between(start, end)).all()
        review_items = [ReviewResponse.from_orm(review) for review in reviews]
        return {
            "reviews": review_items,
            "positiva": len([r for r in review_items if r.sentiment == "positiva"]),
            "neutra": len([r for r in review_items if r.sentiment == "neutra"]),
            "negativa": len([r for r in review_items if r.sentiment == "negativa"]),
        }
    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {e}")


@app.get("/reviews/{id}", response_model=ReviewResponse)
def get_review(id: int, db: Session = Depends(get_db)) -> ReviewResponse:
    """
    Obtém uma avaliação pelo ID.

    Este endpoint recupera uma avaliação específica do banco de dados,
    usando o ID fornecido.

    Args:
        id (int): O ID da avaliação requisitada.

    Returns:
        `ReviewResponse`: Os dados da avaliação.

    Raises:
        HTTPException: Exceção com código de status 404 se
        a avaliação não for encontrada.
    """
    review = db.query(Review).get(id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

