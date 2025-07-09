<template>
  <div>
    <h2>Event Details</h2>
    <button @click="goToEventEdit" style="margin-bottom: 1rem;">Edit Event</button>
    <div v-if="eventDetails">
      <h3>Arenas</h3>
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
              <th>Name</th>
              <th>Number</th>
              <th>Color</th>
              <th>Length (m)</th>
              <th>Image</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="poleLoc in arenaObj.poles" :key="poleLoc.id">
              <td>{{ poleLoc.pole.name_en }}</td>
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
              <td colspan="5" style="text-align:center; color:gray;">No poles for this arena</td>
            </tr>
          </tbody>
        </table>

        <!-- WINGS TABLE -->
        <table border="1" cellpadding="6" style="min-width:400px;">
          <thead>
            <tr>
              <th>Name</th>
              <th>Number</th>
              <th>Color</th>
              <th>Image</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="wingLoc in arenaObj.wings" :key="wingLoc.id">
              <td>{{ wingLoc.wing.name_en }}</td>
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
              <td colspan="4" style="text-align:center; color:gray;">No wings for this arena</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else>Loading...</div>
  </div>
</template>

<script>
import { fetchEventDetails } from '@/api/api';

export default {
  name: "EventDetails",
  props: ['id'],
  data() {
    return { eventDetails: null }
  },
  mounted() {
    fetchEventDetails(this.id)
      .then(res => { this.eventDetails = res.data; })
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
    }
  }
}
</script>
