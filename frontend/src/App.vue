<template>
  <div id="app">
    <nav>
      <router-link to="/events/list">Events List</router-link> |
      <router-link to="/events/create">Create Event</router-link> |
      <router-link to="/arenas/create">Create Arena</router-link> |
      <router-link to="/arenas/edit/">Edit Arena</router-link> |
      <router-link to="/arenas/dashboard/">Arena Dashboard</router-link> |
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Ide jöhet a stílus */
</style>