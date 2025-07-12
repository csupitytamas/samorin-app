<template>
  <div id="app">
    <router-view />
    <NavBar />
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import '@/styles/theme.css'
export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  padding-bottom: 80px; /* hely a fix NavBar számára */
  box-sizing: border-box;
}
</style>
