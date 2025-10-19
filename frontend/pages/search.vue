<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Search & Rate</h1>
      <p class="page-description">Find movies and TV shows to rate</p>
    </div>

    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search movies and TV shows..."
        class="form-input"
        @keyup.enter="search"
      />
      <button @click="search" class="btn btn-primary">Search</button>
    </div>

    <div v-if="searching" class="loading">
      <div class="spinner"></div>
      <p>Searching...</p>
    </div>

    <div v-else-if="searchResults.length > 0">
      <p style="margin-bottom: 1rem; color: var(--text-secondary);">
        Found {{ totalResults }} results
      </p>
      <div class="grid">
        <MovieCard
          v-for="movie in searchResults"
          :key="movie.imdbID"
          :movie="formatMovie(movie)"
          @click="openRatingModal(movie)"
        />
      </div>
    </div>

    <div v-else-if="hasSearched" class="empty-state">
      <h3>No results found</h3>
      <p>Try a different search term</p>
    </div>

    <div v-else class="empty-state">
      <h3>Search for movies and TV shows</h3>
      <p>Enter a title above to get started</p>
    </div>

    <!-- Rating Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ selectedMovie?.Title }}</h2>
          <button @click="closeModal" class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="loadingDetails" class="loading">Loading details...</div>
          <div v-else-if="movieDetails">
            <div style="display: grid; grid-template-columns: 250px 1fr; gap: 2rem; margin-bottom: 2rem;">
              <img
                v-if="movieDetails.poster && movieDetails.poster !== 'N/A'"
                :src="movieDetails.poster"
                :alt="movieDetails.title"
                style="width: 100%; border-radius: 8px;"
              />
              <div style="flex: 1;">
                <p style="margin-bottom: 1rem;">
                  <strong>Year:</strong> {{ movieDetails.year }}<br/>
                  <strong>Genre:</strong> {{ movieDetails.genre }}<br/>
                  <strong>Runtime:</strong> {{ movieDetails.runtime }}<br/>
                  <strong>Director:</strong> {{ movieDetails.director }}<br/>
                  <strong>Actors:</strong> {{ movieDetails.actors }}
                </p>
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">
                  {{ movieDetails.plot }}
                </p>
                <div class="rating-badge">
                  <span class="star">⭐</span>
                  <span>IMDB: {{ movieDetails.imdb_rating || 'N/A' }}</span>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Your Rating (1-10)</label>
              <div class="rating-input">
                <input
                  v-model.number="userRating"
                  type="range"
                  min="1"
                  max="10"
                  step="0.5"
                  style="flex: 1;"
                />
                <span class="rating-number">{{ userRating }}</span>
              </div>
            </div>

            <div style="display: flex; gap: 1rem;">
              <button @click="submitRating" class="btn btn-primary">
                {{ movieDetails.user_rating ? 'Update Rating' : 'Submit Rating' }}
              </button>
              <button @click="closeModal" class="btn btn-secondary">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const searchQuery = ref('')
const searchResults = ref([])
const totalResults = ref(0)
const searching = ref(false)
const hasSearched = ref(false)

const showModal = ref(false)
const selectedMovie = ref(null)
const movieDetails = ref(null)
const loadingDetails = ref(false)
const userRating = ref(5)

async function search() {
  if (!searchQuery.value.trim()) return
  
  searching.value = true
  hasSearched.value = true
  
  try {
    const response = await fetch(`${apiBase}/api/search?query=${encodeURIComponent(searchQuery.value)}`)
    const data = await response.json()
    
    searchResults.value = data.results || []
    totalResults.value = data.total_results || 0
  } catch (error) {
    console.error('Search failed:', error)
    searchResults.value = []
    totalResults.value = 0
  } finally {
    searching.value = false
  }
}

function formatMovie(movie) {
  return {
    imdb_id: movie.imdbID,
    title: movie.Title,
    year: movie.Year,
    type: movie.Type,
    poster: movie.Poster,
    user_rating: movie.userRating
  }
}

async function openRatingModal(movie) {
  selectedMovie.value = movie
  showModal.value = true
  loadingDetails.value = true
  
  try {
    const response = await fetch(`${apiBase}/api/movie/${movie.imdbID}`)
    movieDetails.value = await response.json()
    
    if (movieDetails.value.user_rating) {
      userRating.value = movieDetails.value.user_rating
    } else {
      userRating.value = 5
    }
  } catch (error) {
    console.error('Failed to load movie details:', error)
  } finally {
    loadingDetails.value = false
  }
}

function closeModal() {
  showModal.value = false
  selectedMovie.value = null
  movieDetails.value = null
}

async function submitRating() {
  try {
    const ratingData = {
      imdb_id: movieDetails.value.imdb_id,
      title: movieDetails.value.title,
      year: movieDetails.value.year,
      type: movieDetails.value.type,
      poster: movieDetails.value.poster,
      genre: movieDetails.value.genre,
      runtime: movieDetails.value.runtime,
      plot: movieDetails.value.plot,
      imdb_rating: movieDetails.value.imdb_rating,
      user_rating: userRating.value
    }
    
    const response = await fetch(`${apiBase}/api/ratings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(ratingData)
    })
    
    if (response.ok) {
      closeModal()
      // Refresh search results to show updated rating
      await search()
    }
  } catch (error) {
    console.error('Failed to submit rating:', error)
  }
}
</script>
