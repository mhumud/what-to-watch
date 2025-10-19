<template>
  <div class="movie-card">
    <img
      v-if="movie.poster && movie.poster !== 'N/A'"
      :src="movie.poster"
      :alt="movie.title"
      class="movie-poster"
    />
    <div v-else class="movie-poster" style="display: flex; align-items: center; justify-content: center; background-color: #2a2a2a;">
      <span style="font-size: 3rem;">🎬</span>
    </div>
    <div class="movie-info">
      <div class="movie-title">{{ movie.title }}</div>
      <div class="movie-meta">
        <span>{{ movie.year }}</span>
        <span style="text-transform: capitalize;">{{ movie.type }}</span>
      </div>
      <div v-if="movie.user_rating" class="rating-badge" style="background-color: var(--primary-color); margin-top: 0.5rem;">
        <span class="star">⭐</span>
        <span>Your rating: {{ movie.user_rating }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  movie: {
    type: Object,
    required: true
  }
})
</script>
