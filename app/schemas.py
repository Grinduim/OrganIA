from pydantic import BaseModel
from datetime import date
from typing import List
# Modelo para criar uma nova avaliação (input)
class ReviewCreate(BaseModel):
    """Modelo de dados para a criação de uma nova avaliação.

    Attributes:
        name (str): O nome da pessoa que fez a avaliação.
        date (date): A data em que a avaliação foi feita, no formato 'YYYY-MM-DD'.
        review (str): O texto da avaliação.
    """
    name: str
    date: date
    review: str

# Modelo para a resposta da avaliação (output)
class ReviewResponse(BaseModel):
    """Modelo de dados para a resposta da avaliação criada.

    Attributes:
        id (int): O ID da avaliação gerada no banco de dados.
        name (str): O nome da pessoa que fez a avaliação.
        date (date): A data em que a avaliação foi feita, no formato 'YYYY-MM-DD'.
        review (str): O texto da avaliação.
        sentiment (str): O sentimento analisado da avaliação ('positiva', 'negativa', 'neutra').
    """
    id: int
    name: str
    date: date
    review: str
    sentiment: str
    
    class Config:
        from_attributes=True
        
class ReviewReport(BaseModel):
    """Modelo de dados para o relatório de avaliações, incluindo contagem de sentimentos.

    Attributes:
        reviews (List[ReviewResponse]): Uma lista de avaliações realizadas no período especificado.
        positiva (int): Contagem de avaliações com sentimento positivo.
        neutra (int): Contagem de avaliações com sentimento neutro.
        negativa (int): Contagem de avaliações com sentimento negativo.
    """
    reviews: List[ReviewResponse]
    positiva: int
    neutra: int
    negativa: int