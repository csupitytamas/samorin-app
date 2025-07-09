<template>
  <div id="app">
    <nav>
      <router-link to="/events/list">Events List</router-link> |
      <router-link to="/events/create">Create Event</router-link>  |
      <router-link to="/wishlist">Wishlist</router-link> |
      <router-link to="/archived-events">Archived Events</router-link> |
      <router-link to="/admin">Admin Dashboard</router-link> |
      <router-link to="/profile">Profile</router-link> |

    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
