<template>
  <div>
    <div v-for="arenaBlock in wishlistsByArena" :key="arenaBlock.arena.id" class="box-border centered">
      <h3>{{ arenaBlock.arena.name }}</h3>

      <div v-if="arenaBlock.wishlists.length === 0" class="muted">
        {{ t('noWishlistsForArena') }}
      </div>

      <div v-for="wishlist in arenaBlock.wishlists" :key="wishlist.id" class="wishlist-card white-bg">

        <div class="wishlist-header">
          <div class="wishlist-user">
            <b>{{ t('creater') }}:</b>
            <span class="strong">{{ wishlist.created_by || t('anonymous') }}</span>
          </div>
          <div v-if="wishlist.created_at" class="wishlist-date">
            <b>{{ t('created') }}:</b>
            <span class="strong">{{ formatDateTime(wishlist.created_at) }}</span>
          </div>
        </div>

        <div v-if="wishlist.note" class="wishlist-note">
          {{ wishlist.note }}
        </div>

<div v-if="hasInItems(wishlist)" class="wishlist-table-wrapper">
  <h4>{{ t('warehouseIn') }}</h4>
  <table class="wishlist-table" v-if="hasInItems(wishlist)">
    <thead>
      <tr>
        <th>{{ t('name') }}</th>
        <th>{{ t('number') }}</th>
        <th>{{ t('color') }}</th>
        <th>{{ t('length') }}</th>
        <th>{{ t('image') }}</th>
      </tr>
    </thead>
    <tbody>
      <template v-for="pi in wishlist.pole_items">
        <tr v-if="pi.mode === 'in'" :key="'pole-in-'+pi.id">
          <td>{{ getPoleName(pi.pole) }}</td>
          <td>{{ pi.quantity }}</td>
          <td>{{ getPoleColor(pi.pole) }}</td>
          <td>{{ getPoleLength(pi.pole) }}</td>
          <td>
            <img
              v-if="pi.pole && getPoleImage(pi.pole)"
              :src="getPoleImage(pi.pole)"
              @click.stop="showImage(getPoleImage(pi.pole))"
            />
          </td>
        </tr>
      </template>
      <template v-for="wi in wishlist.wing_items">
        <tr v-if="wi.mode === 'in'" :key="'wing-in-'+wi.id">
          <td>{{ getWingName(wi.wing) }}</td>
          <td>{{ wi.quantity }}</td>
          <td>{{ getWingColor(wi.wing) }}</td>
          <td>—</td>
          <td>
            <img
              v-if="wi.wing && getWingImage(wi.wing)"
              :src="getWingImage(wi.wing)"
              @click.stop="showImage(getWingImage(wi.wing))"
            />
          </td>
        </tr>
      </template>
    </tbody>
  </table>
  <div v-else class="muted">{{ t('noInItems') }}</div>
</div>
<div v-if="hasOutItems(wishlist)" class="wishlist-table-wrapper">
  <h4>{{ t('warehouseOut') }}</h4>
<table class="wishlist-table" v-if="hasOutItems(wishlist)">
    <thead>
      <tr>
        <th>{{ t('name') }}</th>
        <th>{{ t('number') }}</th>
        <th>{{ t('color') }}</th>
        <th>{{ t('length') }}</th>
        <th>{{ t('image') }}</th>
      </tr>
    </thead>
    <tbody>
      <template v-for="pi in wishlist.pole_items">
        <tr v-if="pi.mode === 'out'" :key="'pole-out-'+pi.id">
          <td>{{ getPoleName(pi.pole) }}</td>
          <td>{{ pi.quantity }}</td>
          <td>{{ getPoleColor(pi.pole) }}</td>
          <td>{{ getPoleLength(pi.pole) }}</td>
          <td>
            <img
              v-if="pi.pole && getPoleImage(pi.pole)"
              :src="getPoleImage(pi.pole)"
              @click.stop="showImage(getPoleImage(pi.pole))"
            />
          </td>
        </tr>
      </template>
      <template v-for="wi in wishlist.wing_items">
        <tr v-if="wi.mode === 'out'" :key="'wing-out-'+wi.id">
          <td>{{ getWingName(wi.wing) }}</td>
          <td>{{ wi.quantity }}</td>
          <td>{{ getWingColor(wi.wing) }}</td>
          <td>—</td>
          <td>
            <img
              v-if="wi.wing && getWingImage(wi.wing)"
              :src="getWingImage(wi.wing)"
              @click.stop="showImage(getWingImage(wi.wing))"
            />
          </td>
        </tr>
      </template>
    </tbody>
  </table>
  <div v-else class="muted">{{ t('noInItems') }}</div>
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
import { fetchEventWishlists, fetchPoles, fetchWings } from '@/api/api'
import { mapState } from 'vuex'
import translations from '@/translations'

export default {
  name: "EventWishlists",
  props: ['eventId'],
  data() {
    return {
      wishlistsByArena: [],
      poles: [],
      wings: [],
      fullscreenImage: null,
      loading: true
    }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return (key, params) => {
        let translation = translations[this.lang]?.[key] || key;
        if (params) {
          Object.keys(params).forEach(k => {
            translation = translation.replace(`{${k}}`, params[k]);
          });
        }
        return translation;
      }
    }
  },
  async mounted() {
    const eventId = this.eventId || this.$route.params.eventId;
    try {
      const [arenaWishlists, poleRes, wingRes] = await Promise.all([
        fetchEventWishlists(eventId),
        fetchPoles(),
        fetchWings()
      ]);
      this.wishlistsByArena = arenaWishlists.data.arenas;
      this.poles = poleRes.data;
      this.wings = wingRes.data;
    } catch (err) { console.error(err); }
    finally { this.loading = false }
  },
  methods: {
     showImage(url) {
      this.fullscreenImage = url;
    },
    hasInItems(wishlist) {
      return wishlist.pole_items.some(pi => pi.mode === 'in') || wishlist.wing_items.some(wi => wi.mode === 'in');
    },
    hasOutItems(wishlist) {
      return wishlist.pole_items.some(pi => pi.mode === 'out') || wishlist.wing_items.some(wi => wi.mode === 'out');
    },
    getPoleName(id) {
      const p = this.poles.find(p => p.id === id);
      return p ? (this.lang === 'hu' ? p.name_hu : p.name_en) : '—';
    },
    getPoleColor(id) {
      const p = this.poles.find(p => p.id === id);
      return p?.color || '—';
    },
    getPoleLength(id) {
      const p = this.poles.find(p => p.id === id);
      return p?.length || '—';
    },
    getPoleImage(id) {
      const p = this.poles.find(p => p.id === id);
      return p?.picture ? this.fullImageUrl(p.picture) : '';
    },
    getWingName(id) {
      const w = this.wings.find(w => w.id === id);
      return w ? (this.lang === 'hu' ? w.name_hu : w.name_en) : '—';
    },
    getWingColor(id) {
      const w = this.wings.find(w => w.id === id);
      return w?.color || '—';
    },
    getWingImage(id) {
      const w = this.wings.find(w => w.id === id);
      return w?.picture ? this.fullImageUrl(w.picture) : '';
    },
    formatDateTime(dt) {
      if (!dt) return '';
      const d = new Date(dt);
      return d.toLocaleString(this.lang === 'hu' ? 'hu-HU' : 'en-US', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit'
      });
    },
    fullImageUrl(path) {
      if (!path) return "";
      if (path.startsWith('http')) return path;
      return "http://13.48.70.78:8000" + path;
    }
  }
}
</script>
