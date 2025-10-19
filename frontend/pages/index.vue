<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Welcome to StreamRecs</h1>
      <p class="page-description">Your personalized streaming recommendation system</p>
    </div>

    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
      <div class="card">
        <h2 style="margin-bottom: 1rem;">🎯 How it works</h2>
        <ol style="padding-left: 1.5rem; line-height: 2;">
          <li>Select your streaming platforms in Settings</li>
          <li>Search and rate movies/shows you've watched</li>
          <li>Get personalized recommendations based on your taste</li>
          <li>Filter by genre, type, and length</li>
        </ol>
      </div>

      <div class="card">
        <h2 style="margin-bottom: 1rem;">📊 Your Stats</h2>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else style="display: flex; flex-direction: column; gap: 1rem;">
          <div style="display: flex; justify-content: space-between;">
            <span>Movies Rated:</span>
            <strong>{{ stats.moviesRated }}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span>Shows Rated:</span>
            <strong>{{ stats.showsRated }}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span>Active Platforms:</span>
            <strong>{{ stats.activePlatforms }}</strong>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <span>Average Rating:</span>
            <strong>{{ stats.avgRating }}</strong>
          </div>
        </div>
      </div>

      <div class="card">
        <h2 style="margin-bottom: 1rem;">🚀 Quick Actions</h2>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <NuxtLink to="/search" class="btn btn-primary">Search & Rate Movies</NuxtLink>
          <NuxtLink to="/recommendations" class="btn btn-secondary">View Recommendations</NuxtLink>
          <NuxtLink to="/settings" class="btn btn-secondary">Configure Platforms</NuxtLink>
        </div>
      </div>
    </div>

    <div v-if="recentRatings.length > 0" style="margin-top: 3rem;">
      <h2 style="margin-bottom: 1.5rem;">Recently Rated</h2>
      <div class="grid">
        <MovieCard
          v-for="rating in recentRatings"
          :key="rating.imdb_id"
          :movie="rating"
          @click="viewDetails(rating.imdb_id)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const loading = ref(true)
const stats = ref({
  moviesRated: 0,
  showsRated: 0,
  activePlatforms: 0,
  avgRating: '0.0'
})
const recentRatings = ref([])

onMounted(async () => {
  await fetchStats()
  await fetchRecentRatings()
  loading.value = false
})

async function fetchStats() {
  try {
    const [ratingsRes, platformsRes] = await Promise.all([
      fetch(`${apiBase}/api/ratings`),
      fetch(`${apiBase}/api/platforms`)
    ])
    
    const ratings = await ratingsRes.json()
    const platforms = await platformsRes.json()
    
    const movies = ratings.filter(r => r.type === 'movie')
    const shows = ratings.filter(r => r.type === 'series')
    
    const avgRating = ratings.length > 0
      ? (ratings.reduce((sum, r) => sum + r.user_rating, 0) / ratings.length).toFixed(1)
      : '0.0'
    
    stats.value = {
      moviesRated: movies.length,
      showsRated: shows.length,
      activePlatforms: platforms.filter(p => p.enabled).length,
      avgRating
    }
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
}

async function fetchRecentRatings() {
  try {
    const response = await fetch(`${apiBase}/api/ratings`)
    const ratings = await response.json()
    recentRatings.value = ratings.slice(-6).reverse()
  } catch (error) {
    console.error('Failed to fetch recent ratings:', error)
  }
}

function viewDetails(imdbId) {
  navigateTo(`/movie/${imdbId}`)
}
</script>
