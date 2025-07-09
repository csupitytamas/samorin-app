<template>
  <div class="profile">
    <h2>Profile</h2>
    <div v-if="profile">
      <p><strong>Username:</strong> {{ profile.username }}</p>
      <p><strong>Email:</strong> {{ profile.email }}</p>
      <p><strong>Role:</strong> {{ profile.role }}</p>
    </div>

    <div v-if="wishlists.length">
      <h3>My Wishlists</h3>
    <ul>
      <li v-for="wishlist in wishlists" :key="wishlist.id">
        <strong>{{ wishlist.arena_name }}</strong>
        <ul>
          <li v-if="wishlist.pole_items && wishlist.pole_items.length">
          <b>Pole items:</b>
          <ul>
            <li v-for="pole in wishlist.pole_items" :key="pole.id">
              {{ pole.pole_name }} ({{ pole.pole_color }}) – {{ pole.quantity }} db
            </li>
          </ul>
        </li>
        <li v-if="wishlist.wing_items && wishlist.wing_items.length">
          <b>Wing items:</b>
          <ul>
            <li v-for="wing in wishlist.wing_items" :key="wing.id">
              {{ wing.wing_name }} ({{ wing.wing_color }}) – {{ wing.quantity }} db
            </li>
          </ul>
        </li>
        </ul>
      </li>
    </ul>
    </div>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
      // vagy "@/api", ha ott van!
import { fetchProfile, fetchWishlists, logoutUser } from "@/api/api"

export default {
  name: "ProfilePage",
  data() {
    return {
      profile: null,
      wishlists: [],
    }
  },
  async mounted() {
    // Lekérjük a profil adatokat
    this.profile = await fetchProfile()
    // Csak akkor töltjük le a wishlisteket, ha chief vagy admin a user:
    if (["chief", "admin"].includes(this.profile.role)) {
      this.wishlists = await fetchWishlists()
    }
  },
  methods: {
    logout() {
      logoutUser()
      this.$router.push({ name: "login" })
    },
  },
}
</script>

<style>
.profile {
  max-width: 700px;
  margin: 2rem auto;
}
</style>
