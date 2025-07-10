<template>
  <div>
    <h2>Wishlists for Event "{{ eventName }}"</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="arenaBlock in wishlistsByArena" :key="arenaBlock.arena.id" style="margin-bottom: 2.5rem;">
        <h3>{{ arenaBlock.arena.name }}</h3>
        <div v-if="arenaBlock.wishlists.length === 0" style="color:gray;">No wishlists for this arena</div>
        <div v-for="wishlist in arenaBlock.wishlists" :key="wishlist.id" style="border:1px solid #e2e8f0; border-radius:10px; margin-bottom:13px; padding:13px 14px; background:#f8fbff;">
          <div style="margin-bottom:3px;">
            <b>User:</b>
            <span>{{ wishlist.created_by || 'anonymous' }}</span>
            <span v-if="wishlist.created_at" style="margin-left: 14px; color: #777;">
              <b>Created:</b> {{ formatDateTime(wishlist.created_at) }}
            </span>
          </div>
          <span v-if="wishlist.note" style="color:#6b7280; margin-left:16px;">Note: {{ wishlist.note }}</span>
          <div style="margin-top:4px;">
            <b>Pole items:</b>
            <span v-if="!wishlist.pole_items || wishlist.pole_items.length === 0" style="color:#aaa;">—</span>
            <span v-else>
              <span v-for="pi in wishlist.pole_items" :key="pi.pole" style="margin-right:12px;">
                {{ getPoleName(pi.pole) }} (x{{ pi.quantity }})
              </span>
            </span>
          </div>
          <div>
            <b>Wing items:</b>
            <span v-if="!wishlist.wing_items || wishlist.wing_items.length === 0" style="color:#aaa;">—</span>
            <span v-else>
              <span v-for="wi in wishlist.wing_items" :key="wi.wing" style="margin-right:12px;">
                {{ getWingName(wi.wing) }} (x{{ wi.quantity }})
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchEventWishlists, fetchPoles, fetchWings } from '@/api/api'
export default {
  name: "EventWishlists",
  props: ['eventId'],
  data() {
    return {
      wishlistsByArena: [],
      eventName: '',
      loading: true,
      poles: [],
      wings: []
    }
  },
  async mounted() {
    const eventId = this.eventId || this.$route.params.eventId
    try {
      const [arenaWishlists, poleRes, wingRes] = await Promise.all([
        fetchEventWishlists(eventId),
        fetchPoles(),
        fetchWings()
      ]);
      this.wishlistsByArena = arenaWishlists.data.arenas
      this.eventName = arenaWishlists.data.event_name || ''
      this.poles = poleRes.data
      this.wings = wingRes.data
    } catch (err) { /* ... */ } finally { this.loading = false }
  },
  methods: {
    getPoleName(id) {
      const p = this.poles.find(p => p.id === id)
      return p ? p.name_en : '—'
    },
    getWingName(id) {
      const w = this.wings.find(w => w.id === id)
      return w ? w.name_en : '—'
    },
    formatDateTime(dt) {
      if (!dt) return '';
      const d = new Date(dt);
      return d.toLocaleString('hu-HU', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit'
      });
    }
  }
}
</script>
