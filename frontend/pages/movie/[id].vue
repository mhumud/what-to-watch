<template>
  <div>
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading movie details...</p>
    </div>

    <div v-else-if="error" class="empty-state">
      <h3>Error loading movie</h3>
      <p>{{ error }}</p>
      <NuxtLink to="/" class="btn btn-primary" style="margin-top: 1rem;">
        Go Home
      </NuxtLink>
    </div>

    <div v-else-if="movie">
      <div style="margin-bottom: 2rem;">
        <NuxtLink to="/" class="btn btn-secondary btn-small">← Back</NuxtLink>
      </div>

      <div class="card">
        <div style="display: grid; grid-template-columns: 300px 1fr; gap: 2rem; margin-bottom: 2rem;">
          <div>
            <img
              v-if="movie.poster && movie.poster !== 'N/A'"
              :src="movie.poster"
              :alt="movie.title"
              style="width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);"
            />
            <div v-else style="width: 100%; height: 450px; background-color: #2a2a2a; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
              <span style="font-size: 4rem;">🎬</span>
            </div>
          </div>

          <div>
            <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">{{ movie.title }}</h1>
            <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1.5rem;">
              <span style="color: var(--text-secondary); font-size: 1.2rem;">{{ movie.year }}</span>
              <span style="color: var(--text-secondary); font-size: 1.2rem;">•</span>
              <span style="text-transform: capitalize; color: var(--text-secondary); font-size: 1.2rem;">{{ movie.type }}</span>
              <span v-if="movie.rated" style="color: var(--text-secondary); font-size: 1.2rem;">•</span>
              <span v-if="movie.rated" style="color: var(--text-secondary); font-size: 1.2rem;">{{ movie.rated }}</span>
            </div>

            <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
              <div v-if="movie.imdb_rating" class="rating-badge" style="font-size: 1rem; padding: 0.5rem 1rem;">
                <span class="star">⭐</span>
                <span>IMDB: {{ movie.imdb_rating }}/10</span>
              </div>
              <div v-if="movie.user_rating" class="rating-badge" style="background-color: var(--primary-color); font-size: 1rem; padding: 0.5rem 1rem;">
                <span>❤️</span>
                <span>Your Rating: {{ movie.user_rating }}/10</span>
              </div>
              <div v-if="movie.watched" class="rating-badge" style="background-color: #2d7a2d; font-size: 1rem; padding: 0.5rem 1rem;">
                <span>✓</span>
                <span>Watched</span>
              </div>
            </div>

            <div style="margin-bottom: 1.5rem;">
              <p v-if="movie.runtime" style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                <strong>Runtime:</strong> {{ movie.runtime }}
              </p>
              <p v-if="movie.genre" style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                <strong>Genre:</strong> {{ movie.genre }}
              </p>
              <p v-if="movie.director" style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                <strong>Director:</strong> {{ movie.director }}
              </p>
              <p v-if="movie.actors" style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                <strong>Cast:</strong> {{ movie.actors }}
              </p>
              <p v-if="movie.released" style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                <strong>Released:</strong> {{ movie.released }}
              </p>
            </div>

            <div v-if="movie.plot" style="margin-bottom: 2rem;">
              <h3 style="margin-bottom: 0.5rem;">Plot</h3>
              <p style="color: var(--text-secondary); line-height: 1.8;">{{ movie.plot }}</p>
            </div>

            <div style="border-top: 1px solid var(--border-color); padding-top: 2rem;">
              <h3 style="margin-bottom: 1rem;">Your Rating</h3>
              
              <div class="form-group">
                <label class="form-label">Rate this {{ movie.type }} (1-10)</label>
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

              <div style="display: flex; gap: 1rem; align-items: center; margin-top: 1.5rem;">
                <button @click="submitRating" class="btn btn-primary">
                  {{ movie.user_rating ? 'Update Rating' : 'Submit Rating' }}
                </button>
                
                <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                  <input
                    v-model="watched"
                    type="checkbox"
                    style="width: 20px; height: 20px; cursor: pointer;"
                    @change="toggleWatched"
                  />
                  <span>Mark as watched</span>
                </label>
                
                <button
                  v-if="movie.user_rating"
                  @click="deleteRating"
                  class="btn btn-secondary"
                  style="margin-left: auto;"
                >
                  Delete Rating
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const loading = ref(true)
const error = ref(null)
const movie = ref(null)
const userRating = ref(5)
const watched = ref(false)

onMounted(async () => {
  await fetchMovieDetails()
})

async function fetchMovieDetails() {
  loading.value = true
  error.value = null
  
  try {
    const imdbId = route.params.id
    const response = await fetch(`${apiBase}/api/movie/${imdbId}`)
    
    if (!response.ok) {
      throw new Error('Movie not found')
    }
    
    movie.value = await response.json()
    
    if (movie.value.user_rating) {
      userRating.value = movie.value.user_rating
    } else {
      userRating.value = 5
    }
    
    watched.value = movie.value.watched || false
  } catch (err) {
    error.value = err.message
    console.error('Failed to load movie details:', err)
  } finally {
    loading.value = false
  }
}

async function submitRating() {
  try {
    const ratingData = {
      imdb_id: movie.value.imdb_id,
      title: movie.value.title,
      year: movie.value.year,
      type: movie.value.type,
      poster: movie.value.poster,
      genre: movie.value.genre,
      runtime: movie.value.runtime,
      plot: movie.value.plot,
      imdb_rating: movie.value.imdb_rating,
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
      await fetchMovieDetails()
      alert('Rating saved successfully!')
    }
  } catch (error) {
    console.error('Failed to submit rating:', error)
    alert('Failed to save rating. Please try again.')
  }
}

async function toggleWatched() {
  if (!movie.value.user_rating) {
    alert('Please rate this movie first before marking it as watched.')
    watched.value = false
    return
  }
  
  try {
    const response = await fetch(
      `${apiBase}/api/ratings/${movie.value.imdb_id}/watched?watched=${watched.value}`,
      { method: 'PUT' }
    )
    
    if (response.ok) {
      movie.value.watched = watched.value
    }
  } catch (error) {
    console.error('Failed to update watched status:', error)
    alert('Failed to update watched status. Please try again.')
  }
}

async function deleteRating() {
  if (!confirm('Are you sure you want to delete this rating?')) {
    return
  }
  
  try {
    const response = await fetch(`${apiBase}/api/ratings/${movie.value.imdb_id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      alert('Rating deleted successfully!')
      router.push('/')
    }
  } catch (error) {
    console.error('Failed to delete rating:', error)
    alert('Failed to delete rating. Please try again.')
  }
}
</script>

<style scoped>
@media (max-width: 768px) {
  .card > div {
    grid-template-columns: 1fr !important;
  }
}
</style>
