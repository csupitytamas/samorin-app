<template>
  <div>
    <h2>{{ t('eventDetails') }}</h2>
    <button @click="goToEventEdit" style="margin-bottom: 1rem;">{{ t('editEvent') }}</button>
    <button
      v-if="eventDetails && eventDetails.arenas && eventDetails.arenas.length > 0"
      @click="goToEventWishlists"
      style="margin-bottom: 2rem; margin-left:12px; padding:5px 20px; border-radius:7px; border:1px solid #bbb; background:#e9f5fd; color:#185eb8; font-weight:bold;"
    >
      {{ t('viewAllWishlists') }}
    </button>
    <div v-if="eventDetails">
      <h3>{{ t('arenas') }}</h3>
      <div v-for="arenaObj in eventDetails.arenas" :key="arenaObj.arena.id" style="margin-bottom: 2rem;">
        <h4>
          <a @click.prevent="goToArenaEdit(arenaObj.arena.id)" href="#" style="cursor:pointer; color:blue; text-decoration:underline;">
            {{ arenaObj.arena.name }}
          </a>
        </h4>

        <!-- POLES TABLE -->
        <table border="1" cellpadding="6" style="margin-bottom:1rem; min-width:500px;">
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
                  style="max-width: 70px; max-height: 70px; object-fit: contain;"
                />
              </td>
            </tr>
            <tr v-if="arenaObj.poles.length === 0">
              <td colspan="5" style="text-align:center; color:gray;">{{ t('noPolesForArena') }}</td>
            </tr>
          </tbody>
        </table>

        <!-- WINGS TABLE -->
        <table border="1" cellpadding="6" style="min-width:400px;">
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
                  style="max-width: 70px; max-height: 70px; object-fit: contain;"
                />
              </td>
            </tr>
            <tr v-if="arenaObj.wings.length === 0">
              <td colspan="4" style="text-align:center; color:gray;">{{ t('noWingsForArena') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else>{{ t('loading') }}</div>
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
    return { eventDetails: null }
  },
  computed: {
    ...mapState(['lang']),
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
    goToArenaEdit(arenaId) {
      this.$router.push({name: 'arena-edit', params: {arenaId}});
    },
    goToEventEdit() {
      this.$router.push({name: 'event-edit', params: {eventId: this.id}});
    },
    goToEventWishlists() {
      if (
        this.eventDetails &&
        this.eventDetails.arenas &&
        this.eventDetails.arenas.length > 0 &&
        this.eventDetails.arenas[0].arena &&
        this.eventDetails.arenas[0].arena.event
      ) {
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
