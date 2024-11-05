from typing import Optional, List
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[int] = None
    title: str= Field(min_length=5, max_length=30 )
    overview: str=Field(min_length=5, max_length=200 )
    year: int = Field(le=2030)
    rating: float = Field(le=10, ge=1)
    category: str =Field(min_length=3, max_length=20)

    model_config={
        "json_schema_extra":{
        "examples":[{
            "id": 1,
            "title": "Nombre de la pelicula",
            "overview": "Descripción de la pelicula",
            "year": 2024,
            "rating": 9.8,
            "category": "Acción"
        }]
        }
    }
