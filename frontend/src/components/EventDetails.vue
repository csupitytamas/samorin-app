<template>
  <div class="container centered">
    <h2>{{ t('eventDetails') }}</h2>

    <!-- Csak adminnak -->
    <button v-if="isAdmin" @click="goToEventEdit">{{ t('editEvent') }}</button>

    <!-- Chief és Crew látja a wishlisteket -->
    <button
      v-if="(isAdmin || isChief || isCrew) && eventDetails && eventDetails.arenas && eventDetails.arenas.length > 0"
      @click="goToEventWishlists"
    >
      {{ t('viewAllWishlists') }}
    </button>

    <div v-if="eventDetails">
      <h3>{{ t('arenas') }}</h3>
      <div v-for="arenaObj in eventDetails.arenas" :key="arenaObj.arena.id" class="box-border">
        <h4>
          <a v-if="(isAdmin || isCrew)"
             @click.prevent="goToArenaEdit(arenaObj.arena.id)"
             href="#"
             class="arena-button">
            {{ arenaObj.arena.name }}
          </a>
          <span v-else>{{ arenaObj.arena.name }}</span>
        </h4>

        <!-- POLES TABLE -->
        <table class="styled-table">
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
            <tr v-for="poleLoc in arenaObj.poles" :key="poleLoc.id">
              <td>{{ lang === 'hu' ? poleLoc.pole.name_hu : poleLoc.pole.name_en }}</td>
              <td>{{ poleLoc.quantity }}</td>
              <td>{{ poleLoc.pole.color }}</td>
              <td>{{ poleLoc.pole.length }}</td>
              <td>
                <img
                  v-if="poleLoc.pole.picture"
                  :src="fullImageUrl(poleLoc.pole.picture)"
                  alt="Pole image"
                  class="table-image"
                  @click.stop="showImage(fullImageUrl(poleLoc.pole.picture))"
                  style="cursor: zoom-in;"
                />
              </td>
            </tr>
            <tr v-if="arenaObj.poles.length === 0">
              <td colspan="5" class="muted">{{ t('noPolesForArena') }}</td>
            </tr>
          </tbody>
        </table>

        <!-- WINGS TABLE -->
        <table class="styled-table">
          <thead>
            <tr>
              <th>{{ t('name') }}</th>
              <th>{{ t('number') }}</th>
              <th>{{ t('color') }}</th>
              <th>{{ t('image') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="wingLoc in arenaObj.wings" :key="wingLoc.id">
              <td>{{ lang === 'hu' ? wingLoc.wing.name_hu : wingLoc.wing.name_en }}</td>
              <td>{{ wingLoc.quantity }}</td>
              <td>{{ wingLoc.wing.color }}</td>
              <td>
                <img
                  v-if="wingLoc.wing.picture"
                  :src="fullImageUrl(wingLoc.wing.picture)"
                  alt="Wing image"
                  class="table-image"
                  @click.stop="showImage(fullImageUrl(wingLoc.wing.picture))"
                  style="cursor: zoom-in;"
                />
              </td>
            </tr>
            <tr v-if="arenaObj.wings.length === 0">
              <td colspan="4" class="muted">{{ t('noWingsForArena') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else>{{ t('loading') }}</div>

    <!-- Modal overlay a képekhez -->
    <div v-if="fullscreenImage" class="image-modal" @click.self="fullscreenImage = null">
      <img :src="fullscreenImage" alt="Full image" />
      <button class="modal-close-btn" @click="fullscreenImage = null">Close</button>
    </div>
  </div>
</template>

<script>
import { fetchEventDetails } from '@/api/api';
import { mapState } from 'vuex'
import translations from '@/translations'

export default {
  name: "EventDetails",
  props: ['id'],
  data() {
    return {
      eventDetails: null,
      fullscreenImage: null
    }
  },
  computed: {
    ...mapState(['lang']),
    isAdmin() { return this.$store.getters.isAdmin },
    isChief() { return this.$store.getters.isChief },
    isCrew() { return this.$store.getters.isCrew },
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  mounted() {
    fetchEventDetails(this.id)
      .then(res => {
        this.eventDetails = res.data;
      })
      .catch(err => { console.error(err); });
  },
  methods: {
    fullImageUrl(path) {
      if (!path) return "";
      if (path.startsWith('http')) return path;
      return "http://localhost:8000" + path;
    },
    showImage(url) {
      this.fullscreenImage = url;
    },
    goToArenaEdit(arenaId) {
      this.$router.push({name: 'arena-edit', params: {arenaId}});
    },
    goToEventEdit() {
      this.$router.push({name: 'event-edit', params: {eventId: this.id}});
    },
    goToEventWishlists() {
      if (this.eventDetails?.arenas?.[0]?.arena?.event) {
        const eventId = this.eventDetails.arenas[0].arena.event;
        this.$router.push({
          name: 'event-wishlists',
          params: { eventId: String(eventId) }
        });
      } else {
        console.log("No eventId found in eventDetails!");
      }
    }
  }
}
</script>

<style scoped>
.image-modal {
  position: fixed;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.image-modal img {
  max-width: 90%;
  max-height: 80vh;
  border-radius: 0.5rem;
  box-shadow: 0 0 1rem rgba(0, 209, 178, 0.5);
}

.modal-close-btn {
  margin-top: 1rem;
  background: var(--accent-color);
  color: var(--bg-color);
  padding: 0.5rem 1rem;
  border: none;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: var(--font-size-m);
}

.modal-close-btn:hover {
  background: #00b89f;
}
</style>