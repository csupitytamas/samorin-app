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

      <div v-for="wishlist in wishlists"
           :key="wishlist.id"
           class="wishlist-card white-bg">

        <div class="wishlist-header">
          <div class="wishlist-user">
            <b>{{ t('arena') }}:</b>
            <span class="strong">{{ wishlist.arena_name }}</span>
          </div>
          <button class="arena-button"
                  style="background: var(--accent-color); color: var(--bg-color);"
                  @click="editWishlist(wishlist.id)">
            {{ t('edit') }}
          </button>

        </div>
        <div class="wishlist-date" v-if="wishlist.created_at">
            <b>{{ t('created') }}:</b>
            <span class="strong">{{ formatDateTime(wishlist.created_at) }}</span>
        </div>
        <div v-if="wishlist.note" class="wishlist-note">
          <i>{{ t('note') }}:</i> {{ wishlist.note }}
        </div>

    <div class="wishlist-items">
      <div>
        <b>{{ t('poleItems') }}:</b>
        <div v-if="!wishlist.pole_items?.length" class="muted">—</div>
        <div v-else>
          <div v-for="pole in wishlist.pole_items"
               :key="pole.id"
               class="wishlist-line">
            {{ lang === 'hu' ? pole.pole_name_hu : pole.pole_name_en }}
            ({{ pole.pole_color }}, {{ pole.pole_length }}m) – x{{pole.quantity }}
            <img
            v-if="pole.pole_picture"
            :src="fullImageUrl(pole.pole_picture)"
            class="mini-pole-img"
            alt="Pole"
            @click="showImage(fullImageUrl(pole.pole_picture))"
          />
          </div>
        </div>
      </div>
      <div style="margin-top:0.5rem;">
        <b>{{ t('wingItems') }}:</b>
        <div v-if="!wishlist.wing_items?.length" class="muted">—</div>
        <div v-else>
          <div v-for="wing in wishlist.wing_items"
               :key="wing.id"
               class="wishlist-line">
            {{ lang === 'hu' ? wing.wing_name_hu : wing.wing_name_en }}
            ({{ wing.wing_color }}) –  x{{wing.quantity }}
            <img
              v-if="wing.wing_picture"
              :src="fullImageUrl(wing.wing_picture)"
              class="mini-pole-img"
              alt="Wing"
              @click="showImage(fullImageUrl(wing.wing_picture))"
            />
          </div>
          </div>
       </div>
      </div>
     </div>
    </div>
    <div v-if="fullscreenImage" class="image-modal" @click.self="fullscreenImage = null">
      <img :src="fullscreenImage" alt="Full image" />
      <button class="modal-close-btn" @click="fullscreenImage = null">{{ t('close') }}</button>
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
        fullscreenImage: null,
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
    formatDateTime(datetime) {
      if (!datetime) return ''
      return new Date(datetime).toLocaleString()
    },
     showImage(url) { this.fullscreenImage = url },
    fullImageUrl(path) {
    if (!path) return ""
    if (path.startsWith("http")) return path
    return "http://13.48.70.78:8000" + path
  }
  }
}
</script>

<style scoped>
.wishlist-line {
  margin-left: 1rem;
  margin-top: 0.3rem;
}
</style>