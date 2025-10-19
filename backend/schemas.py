from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PlatformBase(BaseModel):
    name: str
    enabled: bool = True

class PlatformCreate(PlatformBase):
    pass

class Platform(PlatformBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    imdb_id: str
    title: str
    year: str
    type: str
    poster: Optional[str] = None
    genre: Optional[str] = None
    runtime: Optional[str] = None
    plot: Optional[str] = None
    imdb_rating: Optional[float] = None
    user_rating: float = Field(..., ge=1, le=10)

class RatingUpdate(BaseModel):
    user_rating: Optional[float] = Field(None, ge=1, le=10)
    watched: Optional[bool] = None

class RatingResponse(BaseModel):
    id: int
    imdb_id: str
    title: str
    year: str
    type: str
    poster: Optional[str]
    genre: Optional[str]
    runtime: Optional[str]
    plot: Optional[str]
    imdb_rating: Optional[float]
    user_rating: float
    watched: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class MovieSearch(BaseModel):
    imdb_id: str = Field(..., alias="imdbID")
    title: str = Field(..., alias="Title")
    year: str = Field(..., alias="Year")
    type: str = Field(..., alias="Type")
    poster: str = Field(..., alias="Poster")
    
    class Config:
        populate_by_name = True

class MovieDetail(BaseModel):
    imdb_id: str
    title: str
    year: str
    rated: Optional[str]
    released: Optional[str]
    runtime: Optional[str]
    genre: Optional[str]
    director: Optional[str]
    actors: Optional[str]
    plot: Optional[str]
    poster: Optional[str]
    imdb_rating: Optional[float]
    type: str
    
class RecommendationResponse(BaseModel):
    id: int
    imdb_id: str
    title: str
    year: str
    type: str
    poster: Optional[str]
    genre: Optional[str]
    runtime: Optional[str]
    plot: Optional[str]
    imdb_rating: Optional[float]
    predicted_rating: float
    watched: bool
    
    class Config:
        from_attributes = True
