from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Review
from app.schemas import ReviewCreate, ReviewResponse
from app.db import SessionLocal
from app.sentiment_analyze import analyze_sentiment_pt
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
    """Cria uma nova avaliação.

    Este endpoint recebe os dados de uma nova avaliação e os armazena no banco de dados,
    incluindo a análise de sentimento do texto da avaliação.

    Args:
        review (ReviewCreate): Os dados da nova avaliação a serem criados.
        
            - name (str): Nome da pessoa que fez a avaliação.
            
            - date (date): Data em que a avaliação foi feita (formato 'YYYY-MM-DD').
            
            - review (str): Texto da avaliação.
        
        # db (Session, optional): A sessão do banco de dados. O padrão é obter uma nova sessão.

    Returns:
        ReviewResponse: Os dados da avaliação criada, incluindo seu ID e o sentimento analisado.
        
            - id (int): O ID da avaliação gerada.
            
            - name (str): Nome da pessoa que fez a avaliação.
            
            - date (date): Data em que a avaliação foi feita (formato 'YYYY-MM-DD').
            
            - review (str): Texto da avaliação.
            
            - sentiment (str): O sentimento da avaliação ('positiva', 'negativa', 'neutra').

    Raises:
        SQLAlchemyError: Erros relacionados ao banco de dados podem ser levantados se a operação falhar.
    """
    new_review = Review(name=review.name, date=review.date, review=review.review, sentiment=analyze_sentiment_pt(review.review)[0])
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

