<template>
  <div class="profile">
    <h2>{{ t('profile') }}</h2>

    <div v-if="profile">
      <p><strong>{{ t('username') }}:</strong> {{ profile.username }}</p>
      <p><strong>{{ t('email') }}:</strong> {{ profile.email }}</p>
      <div style="margin-bottom: 1.5em;">
        <label for="lang"><b>{{ t('language') }}:</b></label>
        <select id="lang" :value="lang" @change="setLang($event.target.value)" style="margin-left: 8px;">
          <option value="en">English</option>
          <option value="hu">Magyar</option>
        </select>
      </div>
      <button @click="logout">{{ t('logout') }}</button>
    </div>

    <div v-if="wishlists.length">
      <h3>{{ t('myWishlists') }}</h3>
      <ul>
        <li v-for="wishlist in wishlists" :key="wishlist.id">
          <strong>{{ wishlist.arena_name }}</strong>
          <div v-if="wishlist.note">
            <i>{{ t('note') }}:</i> {{ wishlist.note }}
          </div>
          <button @click="editWishlist(wishlist.id)">{{ t('edit') }}</button>
          <ul>
            <li v-if="wishlist.pole_items && wishlist.pole_items.length">
              <b>{{ t('poleItems') }}:</b>
              <ul>
                <li v-for="pole in wishlist.pole_items" :key="pole.id">
                {{ lang === 'hu' ? pole.pole_name_hu : pole.pole_name_en }} ({{ pole.pole_color }}, {{ pole.pole_length }}m) – {{ pole.quantity }} db
              </li>
              </ul>
            </li>
            <li v-if="wishlist.wing_items && wishlist.wing_items.length">
              <b>{{ t('wingItems') }}:</b>
              <ul>
                <li v-for="wing in wishlist.wing_items" :key="wing.id">
                  {{ lang === 'hu' ? wing.wing_name_hu : wing.wing_name_en }} ({{ wing.wing_color }}) – {{ wing.quantity }} db
                </li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import {mapState, mapActions} from 'vuex'
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
        this.$store.dispatch('logout')  // store user-t is törli!
        this.$router.push({ name: "login" })
      },
      editWishlist(id) {
        this.$router.push({ name: "wishlist-edit", params: { id } })
      },
    }
}
</script>

<style>
.profile {
  max-width: 700px;
  margin: 2rem auto;
}
</style>
