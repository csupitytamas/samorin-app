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
          <!-- IN szekció csak ha van ilyen elem -->
          <div v-if="getItems(wishlist, 'in').length > 0">
            <b>{{ t('inMode') }}</b>
            <div
              v-for="item in getItems(wishlist, 'in')"
              :key="'in-' + item.type + '-' + item.id"
              class="wishlist-item-card"
            >
              <img
                v-if="item.type === 'pole' ? item.pole_picture : item.wing_picture"
                :src="item.type === 'pole' ? fullImageUrl(item.pole_picture) : fullImageUrl(item.wing_picture)"
                class="mini-pole-img"
                :alt="item.type"
                @click="showImage(item.type === 'pole' ? fullImageUrl(item.pole_picture) : fullImageUrl(item.wing_picture))"
              />
              <div>
                <span v-if="item.type === 'pole'">
                  {{ lang === 'hu' ? item.pole_name_hu : item.pole_name_en }}
                  ({{ item.pole_color }}, {{ item.pole_length }}m)
                </span>
                <span v-else>
                  {{ lang === 'hu' ? item.wing_name_hu : item.wing_name_en }}
                  ({{ item.wing_color }})
                </span>
                – ({{ item.quantity }})
                <span style="font-size:0.9em; color:#aaa;">
                  {{ t(item.type) }}
                </span>
              </div>
            </div>
          </div>
          <!-- OUT szekció csak ha van ilyen elem -->
          <div v-if="getItems(wishlist, 'out').length > 0" style="margin-top:1.2rem;">
            <b>{{ t('outMode') }}</b>
            <div
              v-for="item in getItems(wishlist, 'out')"
              :key="'out-' + item.type + '-' + item.id"
              class="wishlist-item-card"
            >
              <img
                v-if="item.type === 'pole' ? item.pole_picture : item.wing_picture"
                :src="item.type === 'pole' ? fullImageUrl(item.pole_picture) : fullImageUrl(item.wing_picture)"
                class="mini-pole-img"
                :alt="item.type"
                @click="showImage(item.type === 'pole' ? fullImageUrl(item.pole_picture) : fullImageUrl(item.wing_picture))"
              />
              <div>
                <span v-if="item.type === 'pole'">
                  {{ lang === 'hu' ? item.pole_name_hu : item.pole_name_en }}
                  ({{ item.pole_color }}, {{ item.pole_length }}m)
                </span>
                <span v-else>
                  {{ lang === 'hu' ? item.wing_name_hu : item.wing_name_en }}
                  ({{ item.wing_color }})
                </span>
                – ({{ item.quantity }})
                <span style="font-size:0.9em; color:#aaa;">
                  {{ t(item.type) }}
                </span>
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
    this.wishlists = await fetchWishlists()
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
    },
    // Ez végzi az egyesítést és mode szerinti szűrést!
    getItems(wishlist, mode) {
      return [
        ...(wishlist.pole_items || []).map(i => ({ ...i, type: 'pole' })),
        ...(wishlist.wing_items || []).map(i => ({ ...i, type: 'wing' }))
      ].filter(i => i.mode === mode)
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