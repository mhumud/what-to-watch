from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base

class StreamingPlatform(Base):
    __tablename__ = "streaming_platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    imdb_id = Column(String, unique=True, index=True)
    title = Column(String)
    year = Column(String)
    type = Column(String)  # movie or series
    poster = Column(String)
    genre = Column(String)
    runtime = Column(String)
    plot = Column(Text)
    imdb_rating = Column(Float)
    user_rating = Column(Float)  # 1-10
    watched = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TrendingCache(Base):
    __tablename__ = "trending_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    imdb_id = Column(String, unique=True, index=True)
    title = Column(String)
    year = Column(String)
    type = Column(String)
    poster = Column(String)
    popularity_score = Column(Float, default=0)
    cached_at = Column(DateTime(timezone=True), server_default=func.now())
