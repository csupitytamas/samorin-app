<template>
  <div v-if="event">
    <h2>Archived Event Details</h2>
    <p><b>Name:</b> {{ event.event_name }}</p>
    <p><b>Start:</b> {{ event.event_start }}</p>
    <p><b>End:</b> {{ event.event_end }}</p>
    <p><b>Closed at:</b> {{ event.closed_at }}</p>

    <h3>Arenas</h3>
    <div v-for="arena in event.arenas" :key="arena.id" style="margin-bottom:2rem;">
      <b>{{ arena.name }}</b>
      <div>
        <span>Poles:</span>
        <ul>
          <li v-for="pole in arena.poles" :key="pole.id">
            {{ pole.pole_name }} - {{ pole.color }} - {{ pole.length }}m ({{ pole.quantity }})
          </li>
          <li v-if="arena.poles.length === 0" style="color:gray;">No poles</li>
        </ul>
      </div>
      <div>
        <span>Wings:</span>
        <ul>
          <li v-for="wing in arena.wings" :key="wing.id">
            {{ wing.wing_name }} - {{ wing.color }} ({{ wing.quantity }})
          </li>
          <li v-if="arena.wings.length === 0" style="color:gray;">No wings</li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else>
    Loading...
  </div>
</template>

<script>
import { fetchArchivedEventDetails } from '@/api/api';
export default {
  name: 'ArchivedEventDetails',
  props: ['id'],
  data() {
    return { event: null }
  },
  mounted() {
    fetchArchivedEventDetails(this.id)
      .then(res => { this.event = res.data; })
      .catch(() => { this.event = null });
  }
}
</script>