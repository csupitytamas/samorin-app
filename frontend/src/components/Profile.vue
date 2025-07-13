<template>
  <div class="container">
    <h2>{{ t('profile') }}</h2>

    <div v-if="profile" class="box">
      <p><strong>{{ t('username') }}:</strong> {{ profile.username }}</p>
      <p><strong>{{ t('email') }}:</strong> {{ profile.email }}</p>
      <div style="margin-bottom: 1.5em;">
        <label for="lang"><b>{{ t('language') }}:</b></label>
        <select id="lang" :value="lang" @change="setLang($event.target.value)"
          style="margin-left: 8px; background:var(--bg-color); color:var(--text-color); border:1px solid rgba(255,255,255,0.15); border-radius:var(--border-radius); padding:var(--padding-s);">
          <option value="en">English</option>
          <option value="hu">Magyar</option>
        </select>
      </div>
      <button @click="logout">{{ t('logout') }}</button>
    </div>

    <div v-if="wishlists.length" class="box-border">
      <h3>{{ t('myWishlists') }}</h3>
      <div v-for="wishlist in wishlists" :key="wishlist.id" class="wishlist-card">
        <div class="wishlist-header">
          <strong>{{ wishlist.arena_name }}</strong>
          <button class="arena-button" style="background: var(--accent-color); color: var(--bg-color);"
                  @click="editWishlist(wishlist.id)">
        {{ t('edit') }}
      </button>
        </div>
        <div v-if="wishlist.note" class="wishlist-note">
          <i>{{ t('note') }}:</i> {{ wishlist.note }}
        </div>
        <div class="wishlist-items">
          <div v-if="wishlist.pole_items && wishlist.pole_items.length">
            <b>{{ t('poleItems') }}:</b>
            <ul>
              <li v-for="pole in wishlist.pole_items" :key="pole.id" class="wishlist-line">
                {{ lang === 'hu' ? pole.pole_name_hu : pole.pole_name_en }}
                ({{ pole.pole_color }}, {{ pole.pole_length }}m) – {{ pole.quantity }} db
              </li>
            </ul>
          </div>
          <div v-if="wishlist.wing_items && wishlist.wing_items.length" style="margin-top:0.5rem;">
            <b>{{ t('wingItems') }}:</b>
            <ul>
              <li v-for="wing in wishlist.wing_items" :key="wing.id" class="wishlist-line">
                {{ lang === 'hu' ? wing.wing_name_hu : wing.wing_name_en }}
                ({{ wing.wing_color }}) – {{ wing.quantity }} db
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import translations from '@/translations'
import { fetchProfile, fetchWishlists, logoutUser } from "@/api/api"

export default {
  name: "ProfilePage",
  data() {
    return {
      profile: null,
      wishlists: [],
    }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  async mounted() {
    this.profile = await fetchProfile()
    if (["chief", "admin"].includes(this.profile.role)) {
      this.wishlists = await fetchWishlists()
    }
  },
  methods: {
    ...mapActions(['setLang']),
    logout() {
      logoutUser()
      this.$store.dispatch('logout')
      this.$router.push({ name: "login" })
    },
    editWishlist(id) {
      this.$router.push({ name: "wishlist-edit", params: { id } })
    },
  }
}
</script>

<style scoped>
.wishlist-line {
  margin-left: 1rem;
  margin-top: 0.3rem;
}
</style>