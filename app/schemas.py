from pydantic import BaseModel
from datetime import date

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