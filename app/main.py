from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Review
from app.schemas import ReviewCreate, ReviewResponse
from app.db import SessionLocal
from app.sentiment_analyze import analyze_sentiment_pt, analyze_sentiment
app = FastAPI()

# Dependência de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@app.post("/reviews", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova avaliação.

    Este endpoint recebe os dados de uma nova avaliação e os armazena no banco de dados,
    incluindo a análise de sentimento do texto da avaliação.

    Args:
        review (`ReviewCreate`): Os dados da nova avaliação a serem criados.
        
    Returns:
        ReviewResponse: Os dados da avaliação criada, incluindo seu ID e o sentimento analisado.
        
            - id (int): O ID da avaliação gerada.
            
            - name (str): Nome da pessoa que fez a avaliação.
            
            - date (str): Data em que a avaliação foi feita (formato 'YYYY-MM-DD').
            
            - review (str): Texto da avaliação.
            
            - sentiment (str): O sentimento da avaliação ('positiva', 'negativa', 'neutra').

    Raises:
        SQLAlchemyError: Erros relacionados ao banco de dados podem ser levantados se a operação falhar.
    """
    new_review = Review(name=review.name, date=review.date, review=review.review, sentiment=analyze_sentiment(review.review)[0])
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@app.get("/reviews", response_model=list[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    """
    Retorna todas as avaliações analisadas.

    Este endpoint recupera todas as avaliações de clientes armazenadas no banco de dados e retorna uma lista com as avaliações e suas respectivas classificações de sentimento (positiva, negativa, neutra).

    Returns:
        List[`ReviewResponse`]: Uma lista de objetos `ReviewResponse` contendo as avaliações dos clientes e suas classificações de sentimento.
    
    Example:
        Um exemplo de requisição bem-sucedida para esse endpoint via cURL:
        
        ```bash
        curl -X 'GET' \
        'http://127.0.0.1:8000/reviews' \
        -H 'accept: application/json'
        ```

        Resposta esperada (exemplo):
        ```json
        [
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
        ]
        ```

    Raises:
        HTTPException: Não há exceções esperadas diretamente desse endpoint, pois ele retorna uma lista vazia caso não haja dados no banco de dados.
    """
    reviews = db.query(Review).all()
    return reviews

@app.get("/reviews/{id}", response_model=ReviewResponse)
def get_review(id: int, db: Session = Depends(get_db)):
    """Obtém uma avaliação pelo ID.

    Este endpoint recupera uma avaliação específica do banco de dados, usando o ID fornecido.

    Args:
    
        id (int): O ID da avaliação requisitada.

    Returns:
        ReviewResponse: Os dados da avaliação.

    Raises:
        HTTPException: Exceção com código de status 404 se a avaliação não for encontrada.
    """
    review = db.query(Review).get(id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

