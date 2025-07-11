<template>
  <nav class="navbar">
    <ul class="navbar-list">
      <li v-if="canSeeEvents"><router-link to="/events/list">{{ t('events') }}</router-link></li>
      <li v-if="isAdmin"><router-link to="/events/create">{{ t('eventCreate') }}</router-link></li>
      <li v-if="canSeeArchivedEvents"><router-link to="/archived-events">{{ t('archivedEvents') }}</router-link></li>
      <li v-if="canCreateWishlist"><router-link to="/wishlist">{{ t('wishlistCreate') }}</router-link></li>
      <li v-if="isLoggedIn"><router-link to="/profile">{{ t('profile') }}</router-link></li>
      <li v-if="isAdmin"><router-link to="/admin">{{ t('adminDashboard') }}</router-link></li>

    </ul>

  </nav>
</template>

<script setup>
import { useStore} from 'vuex'
import usePermissions from '@/composables/usePermissions.js'
import translations from '@/translations'

// Jogosultságok
const {
  isLoggedIn,
  isAdmin,
  canSeeEvents,
  canSeeArchivedEvents,
  canCreateWishlist,
} = usePermissions()

// Nyelv
const store = useStore()
function t(key) {
  return translations[store.state.lang]?.[key] || key
}

</script>

<style scoped>
.navbar-list {
  display: flex;
  list-style: none;
  gap: 18px;
  padding: 0;
}

button.active {
  font-weight: bold;
  text-decoration: underline;
}
</style>