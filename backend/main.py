from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
from database import engine, get_db, init_db
from omdb_service import omdb_service

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Streaming Recommendations API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database with default streaming platforms"""
    db = next(get_db())
    
    # Create default platforms if they don't exist
    default_platforms = ["Netflix", "Prime Video", "Apple TV", "Disney+"]
    for platform_name in default_platforms:
        existing = db.query(models.StreamingPlatform).filter(
            models.StreamingPlatform.name == platform_name
        ).first()
        if not existing:
            platform = models.StreamingPlatform(name=platform_name, enabled=False)
            db.add(platform)
    
    db.commit()
    db.close()

# Streaming Platforms Endpoints
@app.get("/api/platforms", response_model=List[schemas.Platform])
def get_platforms(db: Session = Depends(get_db)):
    """Get all streaming platforms"""
    platforms = db.query(models.StreamingPlatform).all()
    return platforms

@app.put("/api/platforms/{platform_id}")
def update_platform(
    platform_id: int,
    enabled: bool,
    db: Session = Depends(get_db)
):
    """Enable or disable a streaming platform"""
    platform = db.query(models.StreamingPlatform).filter(
        models.StreamingPlatform.id == platform_id
    ).first()
    
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    platform.enabled = enabled
    db.commit()
    db.refresh(platform)
    return platform

# Search Endpoint
@app.get("/api/search")
def search_movies(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """Search movies and TV shows from OMDb"""
    results = omdb_service.search_movies(query, page)
    
    # Check which movies the user has already rated
    if results["results"]:
        imdb_ids = [r["imdbID"] for r in results["results"]]
        rated_movies = db.query(models.Rating).filter(
            models.Rating.imdb_id.in_(imdb_ids)
        ).all()
        rated_dict = {r.imdb_id: r.user_rating for r in rated_movies}
        
        # Add user rating to results
        for result in results["results"]:
            result["userRating"] = rated_dict.get(result["imdbID"])
    
    return results

# Movie Details Endpoint
@app.get("/api/movie/{imdb_id}")
def get_movie_details(imdb_id: str, db: Session = Depends(get_db)):
    """Get detailed information about a movie or TV show"""
    details = omdb_service.get_movie_details(imdb_id)
    
    if not details:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Check if user has rated this movie
    rating = db.query(models.Rating).filter(
        models.Rating.imdb_id == imdb_id
    ).first()
    
    response = details.model_dump()
    response["user_rating"] = rating.user_rating if rating else None
    response["watched"] = rating.watched if rating else False
    
    return response

# Ratings Endpoints
@app.get("/api/ratings", response_model=List[schemas.RatingResponse])
def get_ratings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all user ratings"""
    ratings = db.query(models.Rating).offset(skip).limit(limit).all()
    return ratings

@app.post("/api/ratings", response_model=schemas.RatingResponse)
def create_or_update_rating(
    rating: schemas.RatingCreate,
    db: Session = Depends(get_db)
):
    """Create or update a rating for a movie or TV show"""
    # Check if rating already exists
    existing = db.query(models.Rating).filter(
        models.Rating.imdb_id == rating.imdb_id
    ).first()
    
    if existing:
        existing.user_rating = rating.user_rating
        existing.title = rating.title
        existing.year = rating.year
        existing.type = rating.type
        existing.poster = rating.poster
        existing.genre = rating.genre
        existing.runtime = rating.runtime
        existing.plot = rating.plot
        existing.imdb_rating = rating.imdb_rating
        db.commit()
        db.refresh(existing)
        return existing
    
    new_rating = models.Rating(**rating.model_dump())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

@app.put("/api/ratings/{imdb_id}/watched")
def mark_as_watched(
    imdb_id: str,
    watched: bool,
    db: Session = Depends(get_db)
):
    """Mark a movie or TV show as watched"""
    rating = db.query(models.Rating).filter(
        models.Rating.imdb_id == imdb_id
    ).first()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    rating.watched = watched
    db.commit()
    db.refresh(rating)
    return rating

@app.delete("/api/ratings/{imdb_id}")
def delete_rating(imdb_id: str, db: Session = Depends(get_db)):
    """Delete a rating"""
    rating = db.query(models.Rating).filter(
        models.Rating.imdb_id == imdb_id
    ).first()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(rating)
    db.commit()
    return {"message": "Rating deleted"}

# Recommendations Endpoint
@app.get("/api/recommendations")
def get_recommendations(
    genre: Optional[str] = None,
    type: Optional[str] = None,
    max_runtime: Optional[int] = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get personalized recommendations based on user ratings and preferences"""
    
    # Get user's ratings to calculate preferences
    user_ratings = db.query(models.Rating).all()
    
    if not user_ratings:
        # If no ratings, return popular movies
        return get_popular_recommendations(db, genre, type, max_runtime, limit)
    
    # Calculate user's genre preferences
    genre_scores = {}
    for rating in user_ratings:
        if rating.genre:
            genres = [g.strip() for g in rating.genre.split(",")]
            for g in genres:
                if g not in genre_scores:
                    genre_scores[g] = []
                genre_scores[g].append(rating.user_rating)
    
    # Calculate average rating per genre
    genre_avg = {g: sum(scores) / len(scores) for g, scores in genre_scores.items()}
    
    # Get popular movies and score them
    popular_ids = omdb_service.get_popular_movies()
    recommendations = []
    
    watched_ids = {r.imdb_id for r in user_ratings if r.watched}
    rated_ids = {r.imdb_id for r in user_ratings}
    
    # Also include rated but unwatched items as potential recommendations
    all_candidate_ids = set(popular_ids)
    for rating in user_ratings:
        if not rating.watched:
            all_candidate_ids.add(rating.imdb_id)
    
    for imdb_id in all_candidate_ids:
        # Skip if already watched
        if imdb_id in watched_ids:
            continue
        
        # Check if already in database
        existing = db.query(models.Rating).filter(
            models.Rating.imdb_id == imdb_id
        ).first()
        
        if existing and not existing.watched:
            movie_data = existing
        else:
            # Fetch from OMDb
            details = omdb_service.get_movie_details(imdb_id)
            if not details:
                continue
            
            movie_data = models.Rating(
                imdb_id=details.imdb_id,
                title=details.title,
                year=details.year,
                type=details.type,
                poster=details.poster,
                genre=details.genre,
                runtime=details.runtime,
                plot=details.plot,
                imdb_rating=details.imdb_rating,
                user_rating=0,
                watched=False
            )
        
        # Calculate predicted rating based on genre preferences
        predicted_rating = 7.0  # Default baseline
        if movie_data.genre and genre_avg:
            movie_genres = [g.strip() for g in movie_data.genre.split(",")]
            matching_scores = [genre_avg[g] for g in movie_genres if g in genre_avg]
            if matching_scores:
                predicted_rating = sum(matching_scores) / len(matching_scores)
        
        # Boost by IMDB rating
        if movie_data.imdb_rating and movie_data.imdb_rating > 0:
            predicted_rating = (predicted_rating * 0.7) + (movie_data.imdb_rating * 0.3)
        
        # Apply filters
        if genre and movie_data.genre:
            if genre.lower() not in movie_data.genre.lower():
                continue
        
        if type and movie_data.type != type:
            continue
        
        if max_runtime and movie_data.runtime:
            try:
                runtime_min = int(movie_data.runtime.split()[0])
                if runtime_min > max_runtime:
                    continue
            except:
                pass
        
        recommendations.append({
            "id": movie_data.id if hasattr(movie_data, 'id') and movie_data.id else 0,
            "imdb_id": movie_data.imdb_id,
            "title": movie_data.title,
            "year": movie_data.year,
            "type": movie_data.type,
            "poster": movie_data.poster,
            "genre": movie_data.genre,
            "runtime": movie_data.runtime,
            "plot": movie_data.plot,
            "imdb_rating": movie_data.imdb_rating,
            "predicted_rating": round(predicted_rating, 1),
            "watched": movie_data.watched if hasattr(movie_data, 'watched') else False
        })
    
    # Sort by predicted rating
    recommendations.sort(key=lambda x: x["predicted_rating"], reverse=True)
    
    return recommendations[:limit]

def get_popular_recommendations(db, genre, type, max_runtime, limit):
    """Get popular movies when user has no ratings"""
    popular_ids = omdb_service.get_popular_movies()
    recommendations = []
    
    for imdb_id in popular_ids:
        details = omdb_service.get_movie_details(imdb_id)
        if not details:
            continue
        
        # Apply filters
        if genre and details.genre:
            if genre.lower() not in details.genre.lower():
                continue
        
        if type and details.type != type:
            continue
        
        if max_runtime and details.runtime:
            try:
                runtime_min = int(details.runtime.split()[0])
                if runtime_min > max_runtime:
                    continue
            except:
                pass
        
        recommendations.append({
            "id": 0,
            "imdb_id": details.imdb_id,
            "title": details.title,
            "year": details.year,
            "type": details.type,
            "poster": details.poster,
            "genre": details.genre,
            "runtime": details.runtime,
            "plot": details.plot,
            "imdb_rating": details.imdb_rating,
            "predicted_rating": details.imdb_rating or 7.0,
            "watched": False
        })
    
    recommendations.sort(key=lambda x: x["predicted_rating"], reverse=True)
    return recommendations[:limit]

@app.get("/")
def root():
    return {"message": "Streaming Recommendations API"}
