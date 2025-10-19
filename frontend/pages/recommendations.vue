<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Recommendations</h1>
      <p class="page-description">Personalized picks based on your taste</p>
    </div>

    <div class="filter-bar">
      <div class="form-group">
        <label class="form-label">Genre</label>
        <select v-model="filters.genre" class="form-select" @change="fetchRecommendations">
          <option value="">All Genres</option>
          <option value="Action">Action</option>
          <option value="Comedy">Comedy</option>
          <option value="Drama">Drama</option>
          <option value="Horror">Horror</option>
          <option value="Sci-Fi">Sci-Fi</option>
          <option value="Thriller">Thriller</option>
          <option value="Romance">Romance</option>
          <option value="Adventure">Adventure</option>
          <option value="Fantasy">Fantasy</option>
          <option value="Crime">Crime</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Type</label>
        <select v-model="filters.type" class="form-select" @change="fetchRecommendations">
          <option value="">Movies & Shows</option>
          <option value="movie">Movies Only</option>
          <option value="series">Shows Only</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Max Runtime (minutes)</label>
        <select v-model="filters.maxRuntime" class="form-select" @change="fetchRecommendations">
          <option value="">Any Length</option>
          <option value="90">Under 90 min</option>
          <option value="120">Under 2 hours</option>
          <option value="150">Under 2.5 hours</option>
          <option value="180">Under 3 hours</option>
        </select>
      </div>

      <div class="form-group">
        <button @click="clearFilters" class="btn btn-secondary" style="margin-top: 1.8rem;">
          Clear Filters
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Finding your perfect matches...</p>
    </div>

    <div v-else-if="recommendations.length > 0">
      <p style="margin-bottom: 1rem; color: var(--text-secondary);">
        {{ recommendations.length }} recommendations found
      </p>
      <div class="grid">
        <div
          v-for="rec in recommendations"
          :key="rec.imdb_id"
          class="movie-card"
          @click="viewDetails(rec.imdb_id)"
        >
          <img
            v-if="rec.poster && rec.poster !== 'N/A'"
            :src="rec.poster"
            :alt="rec.title"
            class="movie-poster"
          />
          <div v-else class="movie-poster" style="display: flex; align-items: center; justify-content: center; background-color: #2a2a2a;">
            <span style="font-size: 3rem;">🎬</span>
          </div>
          <div class="movie-info">
            <div class="movie-title">{{ rec.title }}</div>
            <div class="movie-meta">
              <span>{{ rec.year }}</span>
              <span style="text-transform: capitalize;">{{ rec.type }}</span>
            </div>
            <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
              <div class="rating-badge">
                <span class="star">⭐</span>
                <span>{{ rec.imdb_rating || 'N/A' }}</span>
              </div>
              <div class="rating-badge" style="background-color: var(--primary-color);">
                <span>🎯</span>
                <span>{{ rec.predicted_rating }}</span>
              </div>
            </div>
            <div v-if="rec.genre" style="font-size: 0.85rem; color: var(--text-secondary);">
              {{ rec.genre }}
            </div>
            <div v-if="rec.runtime" style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.3rem;">
              ⏱️ {{ rec.runtime }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <h3>No recommendations yet</h3>
      <p>Rate some movies and TV shows to get personalized recommendations</p>
      <NuxtLink to="/search" class="btn btn-primary" style="margin-top: 1rem;">
        Start Rating
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const loading = ref(true)
const recommendations = ref([])
const filters = ref({
  genre: '',
  type: '',
  maxRuntime: ''
})

onMounted(async () => {
  await fetchRecommendations()
})

async function fetchRecommendations() {
  loading.value = true
  
  try {
    const params = new URLSearchParams()
    if (filters.value.genre) params.append('genre', filters.value.genre)
    if (filters.value.type) params.append('type', filters.value.type)
    if (filters.value.maxRuntime) params.append('max_runtime', filters.value.maxRuntime)
    
    const response = await fetch(`${apiBase}/api/recommendations?${params}`)
    recommendations.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch recommendations:', error)
    recommendations.value = []
  } finally {
    loading.value = false
  }
}

function clearFilters() {
  filters.value = {
    genre: '',
    type: '',
    maxRuntime: ''
  }
  fetchRecommendations()
}

function viewDetails(imdbId) {
  navigateTo(`/movie/${imdbId}`)
}
</script>
