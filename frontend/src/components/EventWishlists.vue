  <template>
  <div v-for="arenaBlock in wishlistsByArena"
       :key="arenaBlock.arena.id"
       class="box-border centered"
  >
    <h3>{{ arenaBlock.arena.name }}</h3>
    <div v-if="arenaBlock.wishlists.length === 0" class="muted">
      {{ t('noWishlistsForArena') }}
    </div>

   <div v-for="wishlist in arenaBlock.wishlists"
       :key="wishlist.id"
       class="wishlist-card white-bg"
  >
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
  <div class="wishlist-items">
      <div>
        <b>{{ t('poleItems') }}:</b>
        <div v-if="!wishlist.pole_items?.length" class="muted">—</div>
        <div v-else>
          <div v-for="pi in wishlist.pole_items" :key="pi.pole" class="wishlist-line">
            {{ getPoleName(pi.pole) }} ({{ pi.quantity }})
          </div>
        </div>
      </div>
      <div>
        <b>{{ t('wingItems') }}:</b>
        <div v-if="!wishlist.wing_items?.length" class="muted">—</div>
        <div v-else>
          <div v-for="wi in wishlist.wing_items" :key="wi.wing" class="wishlist-line">
            {{ getWingName(wi.wing) }} ({{ wi.quantity }})
          </div>
        </div>
      </div>
    </div>
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
      eventName: '',
      loading: true,
      poles: [],
      wings: []
    }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return (key, params) => {
        let translation = translations[this.lang]?.[key] || key;
        if (params) {
          Object.keys(params).forEach(k => {
            translation = translation.replace(`{${k}}`, params[k])
          });
        }
        return translation;
      }
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
    } catch (err) { /* hibakezelés */ } finally { this.loading = false }
  },
  methods: {
    getPoleName(id) {
      const p = this.poles.find(p => p.id === id)
      return p ? (this.lang === 'hu' ? p.name_hu : p.name_en) : '—'
    },
    getWingName(id) {
      const w = this.wings.find(w => w.id === id)
      return w ? (this.lang === 'hu' ? w.name_hu : w.name_en) : '—'
    },
    formatDateTime(dt) {
      if (!dt) return '';
      const d = new Date(dt);
      return d.toLocaleString(this.lang === 'hu' ? 'hu-HU' : 'en-US', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit'
      });
    }
  }
}
</script>
