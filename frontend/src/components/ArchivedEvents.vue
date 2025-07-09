<template>
  <div>
    <h2>Archived Events</h2>
   <ul>
      <li v-for="event in events" :key="event.id">
        <router-link :to="{ name: 'archived-event-details', params: { id: event.id } }">
          {{ event.event_name }} ({{ event.event_start }} - {{ event.event_end }})
        </router-link>
      </li>
      <li v-if="events.length === 0" style="color:gray;">No archived events</li>
    </ul>
  </div>
</template>
<script>
import { fetchArchivedEvents } from '@/api/api';
export default {
  name: 'ArchivedEvents',
  data() {
    return { events: [] }
  },
  mounted() {
    fetchArchivedEvents()
      .then(res => { this.events = res.data; })
      .catch(() => { this.events = []; });
  }
}
</script>