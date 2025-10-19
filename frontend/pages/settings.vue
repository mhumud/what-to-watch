<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Settings</h1>
      <p class="page-description">Configure your streaming platforms</p>
    </div>

    <div class="card" style="max-width: 800px; margin-bottom: 2rem;">
      <h2 style="margin-bottom: 1rem;">Streaming Platforms</h2>
      <p style="color: var(--text-secondary); margin-bottom: 2rem;">
        Select the streaming platforms you have access to. This helps us provide better recommendations.
      </p>

      <div v-if="loading" class="loading">Loading platforms...</div>
      
      <div v-else class="platforms-grid">
        <div
          v-for="platform in platforms"
          :key="platform.id"
          :class="['platform-card', { enabled: platform.enabled }]"
        >
          <div>
            <div class="platform-name">{{ platform.name }}</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.3rem;">
              {{ platform.enabled ? 'Active' : 'Inactive' }}
            </div>
          </div>
          <label class="toggle-switch">
            <input
              type="checkbox"
              :checked="platform.enabled"
              @change="togglePlatform(platform)"
            />
            <span class="toggle-slider"></span>
          </label>
        </div>
      </div>
    </div>

    <div class="card" style="max-width: 800px;">
      <h2 style="margin-bottom: 1rem;">About</h2>
      <p style="color: var(--text-secondary); line-height: 1.8;">
        <strong>StreamRecs</strong> is a personalized streaming recommendation system that helps you discover 
        movies and TV shows based on your taste. Rate content you've watched, and we'll suggest what to 
        watch next based on your preferences, IMDB ratings, and current trends.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const loading = ref(true)
const platforms = ref([])

onMounted(async () => {
  await fetchPlatforms()
})

async function fetchPlatforms() {
  loading.value = true
  
  try {
    const response = await fetch(`${apiBase}/api/platforms`)
    platforms.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch platforms:', error)
  } finally {
    loading.value = false
  }
}

async function togglePlatform(platform) {
  try {
    const response = await fetch(`${apiBase}/api/platforms/${platform.id}?enabled=${!platform.enabled}`, {
      method: 'PUT'
    })
    
    if (response.ok) {
      platform.enabled = !platform.enabled
    }
  } catch (error) {
    console.error('Failed to toggle platform:', error)
  }
}
</script>
