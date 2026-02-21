<template>
  <div class="home">
    <h1>{{ $t('home.hero_title') }}</h1>
    <p>{{ $t('home.hero_subtitle') }}</p>
    <button class="btn-primary">{{ $t('home.book_now') }}</button>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  text-align: center;
}

p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.btn-primary {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s;
}

.btn-primary:hover {
  transform: scale(1.05);
}
</style>
