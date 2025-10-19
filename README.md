# StreamRecs - Personalized Streaming Recommendations

A full-stack web application that provides personalized movie and TV show recommendations based on your ratings, streaming platform availability, and current trends.

## Features

- 🎬 **Search & Rate**: Search movies and TV shows from IMDB (via OMDb API) and rate them on a 1-10 scale
- 🎯 **Smart Recommendations**: Get personalized suggestions based on your ratings and preferences
- 📺 **Platform Management**: Specify which streaming platforms you have access to (Netflix, Prime Video, Apple TV, Disney+)
- 🔍 **Advanced Filtering**: Filter recommendations by genre, type (movie/show), and runtime
- ⭐ **IMDB Integration**: See IMDB ratings alongside your personal ratings
- 📊 **Watch History**: Track what you've already watched

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **OMDb API**: Movie data from IMDB

### Frontend
- **Nuxt 3**: Vue.js framework with SSR support
- **Vue 3**: Progressive JavaScript framework
- Modern CSS with custom design system

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or higher
- Node.js 18 or higher
- PostgreSQL 15 or higher (or use Docker)
- Git

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd what-to-watch
```

### 2. Set Up the Database

#### Option A: Using Docker (Recommended)

```bash
docker-compose up -d
```

This will start a PostgreSQL database on port 5432.

#### Option B: Local PostgreSQL

If you have PostgreSQL installed locally:

```bash
# Create database and user
psql -U postgres
CREATE DATABASE streamdb;
CREATE USER streamuser WITH PASSWORD 'streampass';
GRANT ALL PRIVILEGES ON DATABASE streamdb TO streamuser;
\q
```

### 3. Set Up the Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

Edit the `.env` file and add your OMDb API key:

```env
DATABASE_URL=postgresql://streamuser:streampass@localhost:5432/streamdb
OMDB_API_KEY=your_omdb_api_key_here
```

**Get a free OMDb API key**: Visit [https://www.omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)

### 4. Start the Backend Server

```bash
# Make sure you're in the backend directory with venv activated
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### 5. Set Up the Frontend

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

## Usage Guide

### Initial Setup

1. **Configure Platforms**: Navigate to Settings and enable the streaming platforms you have access to.

2. **Rate Movies**: Go to "Search & Rate" and search for movies or TV shows you've watched. Rate them on a scale of 1-10.

3. **Get Recommendations**: Visit the "Recommendations" page to see personalized suggestions based on your ratings.

### Features Walkthrough

#### Home Page
- View your rating statistics
- See recently rated content
- Quick access to all features

#### Search & Rate
- Search for any movie or TV show
- View detailed information including plot, cast, and IMDB rating
- Submit your personal rating (1-10 scale)
- Update existing ratings

#### Recommendations
- Get personalized recommendations based on:
  - Your rating patterns and genre preferences
  - IMDB ratings
  - Popular/trending content
- Filter by:
  - **Genre**: Action, Comedy, Drama, Horror, Sci-Fi, etc.
  - **Type**: Movies only, TV shows only, or both
  - **Length**: Filter by maximum runtime
- Each recommendation shows:
  - IMDB rating
  - Predicted rating based on your preferences
  - Genre and runtime information

#### Settings
- Enable/disable streaming platforms
- View your active platform subscriptions

## API Endpoints

### Platforms
- `GET /api/platforms` - Get all streaming platforms
- `PUT /api/platforms/{id}` - Update platform status

### Search & Movies
- `GET /api/search?query={title}` - Search movies and TV shows
- `GET /api/movie/{imdb_id}` - Get detailed movie information

### Ratings
- `GET /api/ratings` - Get all user ratings
- `POST /api/ratings` - Create or update a rating
- `PUT /api/ratings/{imdb_id}/watched` - Mark as watched
- `DELETE /api/ratings/{imdb_id}` - Delete a rating

### Recommendations
- `GET /api/recommendations` - Get personalized recommendations
  - Query params: `genre`, `type`, `max_runtime`, `limit`

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application and endpoints
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── database.py          # Database connection and session
│   ├── config.py            # Configuration settings
│   ├── omdb_service.py      # OMDb API integration
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
│
├── frontend/
│   ├── pages/
│   │   ├── index.vue        # Home page
│   │   ├── search.vue       # Search and rating page
│   │   ├── recommendations.vue  # Recommendations page
│   │   └── settings.vue     # Platform settings
│   ├── components/
│   │   └── MovieCard.vue    # Reusable movie card component
│   ├── layouts/
│   │   └── default.vue      # Default layout with navigation
│   ├── assets/
│   │   └── css/
│   │       └── main.css     # Global styles
│   ├── nuxt.config.ts       # Nuxt configuration
│   ├── app.vue              # Root component
│   └── package.json         # Node dependencies
│
├── docker-compose.yml       # Docker configuration for PostgreSQL
└── README.md               # This file
```

## How the Recommendation Algorithm Works

The recommendation system uses a hybrid approach:

1. **Genre Preference Learning**: Analyzes your ratings to identify which genres you prefer
2. **Weighted Scoring**: Combines your genre preferences (70%) with IMDB ratings (30%)
3. **Trending Content**: Includes popular and highly-rated movies/shows
4. **Filtering**: Applies your selected filters (genre, type, length)
5. **Smart Ranking**: Sorts recommendations by predicted rating

The more movies you rate, the better the recommendations become!

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run with auto-reload
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database Migrations

The application automatically creates tables on startup. To reset the database:

```bash
# Using Docker
docker-compose down -v
docker-compose up -d

# Using local PostgreSQL
dropdb streamdb
createdb streamdb
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://streamuser:streampass@localhost:5432/streamdb
OMDB_API_KEY=your_omdb_api_key_here
```

### Frontend
The frontend uses Nuxt's runtime config. API base URL defaults to `http://localhost:8000` in development.

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running: `docker-compose ps` or `pg_isready`
- Check credentials in `.env` file
- Verify port 5432 is not in use by another process

### OMDb API Issues
- Verify your API key is valid
- Check rate limits (free tier: 1,000 requests/day)
- Ensure you have an active internet connection

### Frontend CORS Issues
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

### Port Already in Use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

## Production Deployment

### Backend
1. Set production environment variables
2. Use a production-grade WSGI server (e.g., Gunicorn)
3. Set up proper database with backups
4. Enable HTTPS

### Frontend
1. Build the application: `npm run build`
2. Deploy the `.output` directory
3. Set production API URL in environment variables

## Future Enhancements

- Multi-user support with authentication
- Integration with streaming platform APIs for real-time availability
- Social features (share recommendations, compare tastes)
- Watch history tracking with dates
- Advanced analytics and insights
- Mobile app
- Email notifications for new recommendations

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OMDb API for movie data
- FastAPI for the excellent Python framework
- Nuxt.js team for the amazing Vue.js framework
- PostgreSQL for the robust database system