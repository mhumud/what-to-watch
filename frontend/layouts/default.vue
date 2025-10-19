<template>
  <div>
    <nav class="navbar">
      <div class="container">
        <div class="nav-content">
          <NuxtLink to="/" class="nav-brand">🎬 StreamRecs</NuxtLink>
          <ul class="nav-links">
            <li><NuxtLink to="/">Home</NuxtLink></li>
            <li><NuxtLink to="/search">Search & Rate</NuxtLink></li>
            <li><NuxtLink to="/recommendations">Recommendations</NuxtLink></li>
            <li><NuxtLink to="/settings">Settings</NuxtLink></li>
          </ul>
        </div>
      </div>
    </nav>
    
    <main class="container" style="padding-top: 2rem; padding-bottom: 4rem;">
      <slot />
    </main>
  </div>
</template>

<script setup>
</script>
