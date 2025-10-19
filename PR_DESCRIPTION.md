# Pull Request: Add Personalized Streaming Recommendation Webapp

## Summary

This PR implements a full-stack web application for personalized movie and TV show recommendations. The application allows users to:

- ✅ Specify streaming platforms (Netflix, Prime Video, Apple TV, Disney+)
- ✅ Search movies and TV shows from IMDB via OMDb API
- ✅ Rate content on a 1-10 scale within the webapp
- ✅ View personalized recommendations based on ratings, trending content, and available platforms
- ✅ Filter recommendations by genre, type (movie/show), and length
- ✅ See IMDB ratings alongside predicted ratings

## Technical Implementation

### Backend (FastAPI + PostgreSQL + SQLAlchemy)
- RESTful API with comprehensive endpoints
- PostgreSQL database with proper schema design
- OMDb API integration for IMDB movie data
- Smart recommendation algorithm using genre preference analysis
- Support for filtering and pagination

### Frontend (Nuxt 3 + Vue 3)
- Modern, responsive UI with custom design system
- Four main pages: Home, Search & Rate, Recommendations, Settings
- Real-time updates and smooth user experience
- Advanced filtering with genre, type, and runtime options

### Infrastructure
- Docker Compose for PostgreSQL setup
- Environment configuration for both frontend and backend
- Comprehensive documentation in README

## Key Features

1. **Platform Management**: Users can enable/disable their streaming platforms in settings
2. **Search & Rate**: Full-text search with detailed movie information and rating modal
3. **Smart Recommendations**: Hybrid algorithm combining user preferences (70%) and IMDB ratings (30%)
4. **Advanced Filtering**: Filter by genre, type, and maximum runtime
5. **Watch Tracking**: Mark content as watched to refine recommendations

## File Structure

- `backend/` - FastAPI application with SQLAlchemy ORM
- `frontend/` - Nuxt 3 application with Vue 3
- `docker-compose.yml` - PostgreSQL database setup
- `README.md` - Comprehensive setup and usage documentation

## Test Plan

To test this PR:

### 1. Setup Database
```bash
docker-compose up -d
```

### 2. Configure Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OMDb API key (get free key from https://www.omdbapi.com/apikey.aspx)
uvicorn main:app --reload
```

Backend will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

### 3. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

### 4. Test Features
- Navigate to Settings and enable streaming platforms (e.g., Netflix, Disney+)
- Go to "Search & Rate" and search for movies (try "Inception", "The Matrix", "Breaking Bad")
- Rate at least 5-10 movies/shows with varying scores (use your actual opinions!)
- Visit Recommendations page - should see personalized suggestions
- Test filters:
  - Genre filter (try Action, Drama, Comedy)
  - Type filter (Movies Only, Shows Only)
  - Runtime filter (Under 2 hours, etc.)
- Verify IMDB ratings are displayed for each movie
- Check that predicted ratings (🎯) make sense based on your rated content

### 5. API Testing
- Visit http://localhost:8000/docs for interactive API documentation
- Test endpoints directly via Swagger UI:
  - GET /api/platforms
  - GET /api/search?query=inception
  - GET /api/recommendations
  - POST /api/ratings

## Requirements Fulfilled

All original requirements have been implemented:

- ✅ **Requirement 1**: Streaming platform specification (Netflix, Prime Video, Apple TV, Disney+)
- ✅ **Requirement 2**: IMDB search and rating functionality (1-10 scale)
- ✅ **Requirement 3**: Personalized recommendations considering ratings, trending data, and watch history
- ✅ **Requirement 4**: Filtering by genre, type (movie/show), and length
- ✅ **Requirement 5**: IMDB rating display for all recommendations
- ✅ **Technology**: Vue/Nuxt frontend as preferred
- ✅ **Database**: PostgreSQL with SQLAlchemy ORM
- ✅ **Documentation**: Comprehensive README with setup instructions

## Screenshots

The application includes:
- 🏠 **Home Page**: Dashboard with user stats and quick actions
- 🔍 **Search & Rate**: Movie search with detailed modal and rating slider
- 🎯 **Recommendations**: Filtered list with predicted ratings and IMDB scores
- ⚙️ **Settings**: Platform management with toggle switches

## Notes

- The OMDb API has a free tier limit of 1,000 requests/day
- The recommendation algorithm improves as you rate more content
- Trending movies are currently a curated list (can be enhanced with live trending API)
- All database tables are created automatically on first run

## Future Enhancements

Potential improvements for future iterations:
- Multi-user support with authentication
- Real-time streaming platform availability via TMDb API
- Social features (compare tastes with friends)
- Advanced analytics dashboard
- Mobile app version
- Email notifications for new recommendations
