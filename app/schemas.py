from pydantic import BaseModel
from datetime import date

# Modelo para criar uma nova avaliação (input)
class ReviewCreate(BaseModel):
    name: str
    date: date
    review: str

# Modelo para a resposta da avaliação (output)
class ReviewResponse(BaseModel):
    id: int
    name: str
    date: date
    review: str
    sentiment: str