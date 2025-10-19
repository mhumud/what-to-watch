import requests
from typing import List, Optional
from config import settings
from schemas import MovieSearch, MovieDetail

class OMDBService:
    BASE_URL = "http://www.omdbapi.com/"
    
    def __init__(self):
        self.api_key = settings.omdb_api_key
    
    def search_movies(self, query: str, page: int = 1) -> dict:
        """Search movies and TV shows by title"""
        params = {
            "apikey": self.api_key,
            "s": query,
            "page": page
        }
        
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        
        if data.get("Response") == "True":
            return {
                "results": data.get("Search", []),
                "total_results": int(data.get("totalResults", 0))
            }
        return {"results": [], "total_results": 0}
    
    def get_movie_details(self, imdb_id: str) -> Optional[MovieDetail]:
        """Get detailed information about a movie or TV show"""
        params = {
            "apikey": self.api_key,
            "i": imdb_id,
            "plot": "full"
        }
        
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        
        if data.get("Response") == "True":
            imdb_rating = data.get("imdbRating")
            if imdb_rating and imdb_rating != "N/A":
                try:
                    imdb_rating = float(imdb_rating)
                except:
                    imdb_rating = None
            else:
                imdb_rating = None
                
            return MovieDetail(
                imdb_id=data.get("imdbID"),
                title=data.get("Title"),
                year=data.get("Year"),
                rated=data.get("Rated") if data.get("Rated") != "N/A" else None,
                released=data.get("Released") if data.get("Released") != "N/A" else None,
                runtime=data.get("Runtime") if data.get("Runtime") != "N/A" else None,
                genre=data.get("Genre") if data.get("Genre") != "N/A" else None,
                director=data.get("Director") if data.get("Director") != "N/A" else None,
                actors=data.get("Actors") if data.get("Actors") != "N/A" else None,
                plot=data.get("Plot") if data.get("Plot") != "N/A" else None,
                poster=data.get("Poster") if data.get("Poster") != "N/A" else None,
                imdb_rating=imdb_rating,
                type=data.get("Type")
            )
        return None
    
    def get_popular_movies(self) -> List[str]:
        """Get a list of popular movie IDs. This is a curated list since OMDb doesn't have a trending endpoint."""
        # These are some popular/trending movies and shows
        # In a real app, you'd want to update this periodically or use TMDb API
        popular_ids = [
            "tt15398776",  # Oppenheimer
            "tt1160419",   # Dune
            "tt6718170",   # The Super Mario Bros. Movie
            "tt14230458",  # Barbie
            "tt10366206",  # John Wick: Chapter 4
            "tt0816692",   # Interstellar
            "tt1375666",   # Inception
            "tt0468569",   # The Dark Knight
            "tt0109830",   # Forrest Gump
            "tt0137523",   # Fight Club
            "tt0111161",   # The Shawshank Redemption
            "tt0068646",   # The Godfather
            "tt0071562",   # The Godfather Part II
            "tt0110912",   # Pulp Fiction
            "tt0120737",   # The Lord of the Rings: The Fellowship of the Ring
            "tt0167260",   # The Lord of the Rings: The Return of the King
            "tt0133093",   # The Matrix
            "tt0080684",   # Star Wars: Episode V
            "tt0099685",   # Goodfellas
            "tt0073486",   # One Flew Over the Cuckoo's Nest
        ]
        return popular_ids

omdb_service = OMDBService()
